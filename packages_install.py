# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022/8/29 10:51
@Author  : jay chan
@FileName: packages_install.py.py

安装consul相关包:
setuptools-28.8.0.tar.gz
click-6.6.tar.gz
python-consul-1.1.0.tar.gz
requests-2.18.4.tar.gz
urllib3-1.22.tar.gz
six-1.11.0.tar.gz
idna-2.6.tar.gz
certifi-2017.11.5.tar.gz
"""
import argparse
import commands

set_up_tools_p = {
    'tar': 'setuptools-28.8.0.tar.gz',
    'fn': 'setuptools-28.8.0'
}

click_p = {
    'tar': 'click-6.6.tar.gz',
    'fn': 'click-6.6'
}

python_consul_p = {
    'tar': 'python-consul-1.1.0.tar.gz',
    'fn': 'python-consul-1.1.0'
}

requests_p = {
    'tar': 'requests-2.18.4.tar.gz',
    'fn': 'requests-2.18.4'
}

urllib_p = {
    'tar': 'urllib3-1.22.tar.gz',
    'fn': 'urllib3-1.22'
}

six_p = {
    'tar': 'six-1.11.0.tar.gz',
    'fn': 'six-1.11.0'
}

idna_p = {
    'tar': 'idna-2.6.tar.gz',
    'fn': 'idna-2.6'
}

certifi_p = {
    'tar': 'certifi-2017.11.5.tar.gz',
    'fn': 'certifi-2017.11.5'
}

all_package_dict = {
    '1': set_up_tools_p,
    '2': click_p,
    '3': python_consul_p,
    '4': requests_p,
    '5': urllib_p,
    '6': six_p,
    '7': idna_p,
    '8': certifi_p
}

packages_prefix = 'packages/'

"""
    执行具体的安装命令
"""


def abs_execute_func(*args):
    status, output = commands.getstatusoutput(list(args)[0::][0])
    return tuple((args, status, output))


"""
    解压, 切换目录, 执行setup.py
"""


def abs_command(package_dict):
    tar_gz = '%s%s -C %s' % (packages_prefix, package_dict['tar'], packages_prefix)
    fn = '%s%s' % (packages_prefix, package_dict['fn'])
    return 'tar -zxvf %s && cd %s && python setup.py install' % (tar_gz, fn)


"""
    执行安装流程
"""


def shell_command_execute():
    var = argparse.ArgumentParser(
        prog='packages_install.py',
        description='packages install about python_consul'
    )

    var.add_argument('-p', '--packages', help='set the package to be installed')

    args = var.parse_args()

    if args.packages is None:
        print('execute command error (-p or --packages cannot be empty)')
        return

    for i, p in enumerate(str.split(args.packages, ',')):
        package_dict = all_package_dict[p]
        shell_command = abs_command(package_dict)

        print('execute command is: (%s)' % shell_command)
        result_tuple = abs_execute_func(shell_command)
        print('execute command status is: %s' % result_tuple[1])
        print('execute command output is: \n%s' % result_tuple[2])

        print('----------------------------------------')


if __name__ == '__main__':
    shell_command_execute()