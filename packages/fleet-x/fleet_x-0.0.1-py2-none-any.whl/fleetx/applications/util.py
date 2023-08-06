# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import six
import paddle.fluid as fluid
from paddle.fluid.framework import Program, Parameter
from paddle.fluid import core


def load_program(program_input):
    with open(program_input + '/startup_program', "rb") as fin:
        program_desc_str = fin.read()
        new_startup = Program().parse_from_string(program_desc_str)

    with open(program_input + '/main_program', "rb") as fin:
        program_desc_str = fin.read()
        new_main = Program().parse_from_string(program_desc_str)

    para_list = []
    with open(program_input + '/para_info', 'r') as fin:
        for line in fin:
            current_para = {}
            para = line[:-1].split(":")
            current_para["name"] = para[0]
            if para[1] == 'True':
                current_para['trainable'] = True
            else:
                current_para['trainable'] = False
            para_list.append(current_para)
    input_list = []
    with open(program_input + '/input_names', 'r') as fin:
        for line in fin:
            current_input = line[:-1].split(":")[0].replace("var", "").strip()
            input_list.append(current_input)

    with open(program_input + '/loss_name', 'r') as fin:
        loss_name = fin.read()
    if os.path.exists(program_input + '/acc'):
        target = []
        with open(program_input + '/acc', 'r') as fin:
            for line in fin:
                for var in new_main.list_vars():
                    if var.name == line[:-1]:
                        target.append(var)
    else:
        print("Please save your target first")
        target = None
    unique_generator = fluid.unique_name.UniqueNameGenerator()
    with open(program_input + '/unique_name_guard', 'r') as fin:
        for line in fin:
            current_guard = line[:-1].split(":")
            unique_generator.ids[current_guard[0]] = int(current_guard[1])

    fluid.unique_name.switch(unique_generator)
    if os.path.exists(program_input + '/lr_name'):
        with open(program_input + '/lr_name', 'r') as fin:
            lr_name = fin.read()
    else:
        lr_name = None
    if os.path.exists(program_input + '/checkpoint'):
        checkpoints = []
        with open(program_input + '/checkpoint', 'r') as fin:
            for line in fin:
                ckpt_name = line[:-1]
                checkpoints.append(ckpt_name)
    else:
        checkpoints = None
    for item in para_list:
        main_para = new_main.global_block().var(item['name'])
        main_para.__class__ = Parameter
        main_para.regularizer = None
        main_para.optimize_attr = {'learning_rate': 1.0}
        main_para.trainable = item['trainable']
        main_para.is_distributed = False

        startup_para = new_startup.global_block().var(item['name'])
        startup_para.__class__ = Parameter
        startup_para.regularizer = None
        startup_para.optimize_attr = {'learning_rate': 1.0}
        startup_para.trainable = item['trainable']
        startup_para.is_distributed = False

    loss = None
    input_vars = []
    for input_name in input_list:
        for var in new_main.list_vars():
            if var.name == input_name:
                input_vars.append(var)
    for var in new_main.list_vars():
        if var.name == loss_name:
            loss = var
        if lr_name != None:
            if var.name == lr_name:
                lr = var

    fluid.framework.switch_main_program(new_main)
    fluid.framework.switch_startup_program(new_startup)
    main_ops = fluid.default_main_program().global_block().ops
    for main_op in main_ops:
        main_out_names = main_op.output_names
        for item in main_out_names:
            var_name = main_op.output(item)
            var = fluid.framework._get_var(str(var_name[0]))
            var.op = main_op
    startup_ops = fluid.default_startup_program().global_block().ops
    for startup_op in startup_ops:
        out_names = startup_op.output_names
        for item in out_names:
            var_name = startup_op.output(item)
            var = fluid.framework._get_var(str(var_name[0]))
            var.op = startup_op
    return input_vars, loss, new_startup, new_main, unique_generator, checkpoints, target


def save_program(main_prog,
                 startup_prog,
                 program_path,
                 input_list,
                 hidden_vars,
                 loss,
                 generator_info,
                 target,
                 checkpoints=None,
                 learning_rate=None):
    if not os.path.exists(program_path):
        os.makedirs(program_path)
    main_program_str = main_prog.desc.serialize_to_string()
    startup_program_str = startup_prog.desc.serialize_to_string()
    params = main_prog.global_block().all_parameters()
    para_info = []
    with open(program_path + '/input_names', 'w') as fout:
        for input in input_list:
            fout.write("%s\n" % input)
    if hidden_vars != None:
        with open(program_path + '/hidden_vars', 'w') as fout:
            for var in hidden_vars:
                fout.write("%s:%s\n" % (var[0], var[1].name))
    with open(program_path + '/para_info', 'w') as fout:
        for item in params:
            fout.write("%s:%s\n" % (item.name, item.trainable))
    with open(program_path + '/startup_program', "wb") as fout:
        fout.write(startup_program_str)
    with open(program_path + '/main_program', "wb") as fout:
        fout.write(main_program_str)
    with open(program_path + '/loss_name', 'w') as fout:
        fout.write(loss.name)
    if type(learning_rate) == fluid.Variable:
        with open(program_path + '/lr_name', 'w') as fout:
            fout.write(learning_rate.name)
    with open(program_path + '/unique_name_guard', 'w') as fout:
        for id, value in generator_info.iteritems():
            fout.write("%s:%s\n" % (id, value))
    if checkpoints is not None:
        with open(program_path + '/checkpoint', 'w') as fout:
            for ckpt in checkpoints:
                fout.write("%s\n" % ckpt.name)
    with open(program_path + '/target', 'w') as fout:
        fout.write(target.name)


def linear_warmup_decay(learning_rate, warmup_steps, num_train_steps):
    """ Applies linear warmup of learning rate from 0 and decay to 0."""
    with fluid.default_main_program()._lr_schedule_guard():
        lr = fluid.layers.tensor.create_global_var(
            shape=[1],
            value=0.0,
            dtype='float32',
            persistable=True,
            name="scheduled_learning_rate")

        global_step = fluid.layers.learning_rate_scheduler._decay_step_counter(
        )

        with fluid.layers.control_flow.Switch() as switch:
            with switch.case(global_step < warmup_steps):
                warmup_lr = learning_rate * (global_step / warmup_steps)
                fluid.layers.tensor.assign(warmup_lr, lr)
            with switch.default():
                decayed_lr = fluid.layers.learning_rate_scheduler.polynomial_decay(
                    learning_rate=learning_rate,
                    decay_steps=num_train_steps,
                    end_learning_rate=0.0,
                    power=1.0,
                    cycle=False)
                fluid.layers.tensor.assign(decayed_lr, lr)

        return lr
