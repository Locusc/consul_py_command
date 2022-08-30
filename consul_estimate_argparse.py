# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022/8/24 15:07
@Author  : jay chan
@FileName: consul_estimate_argparse.py
"""
import sys

import argparse
import consul

"""
    基础配置信息: 默认为开发环境
"""


class BaseEnvConfig:

    def __init__(self):
        pass

    consul_host = 'xxx'
    consul_port = 80
    consul_token = 'xxx'
    consul_router_prefix = 'config/'
    consul_router_suffix = '/data'
    consul_data_center = 'xxx'


"""
    测试环境配置
"""


class TestEnvConfig(BaseEnvConfig):

    def __init__(self):
        super().__init__()

    consul_host = 'xxx'
    consul_port = 80
    consul_token = 'xxx'


"""
    UAT环境配置
"""


class UatEnvConfig(BaseEnvConfig):

    def __init__(self):
        super().__init__()

    consul_host = 'xxx'
    consul_port = 80
    consul_token = 'xxx'


"""
    生产环境配置
"""


class ProdEnvConfig(BaseEnvConfig):

    def __init__(self):
        super().__init__()

    consul_host = 'xxx'
    consul_port = 80
    consul_token = 'xxx'


global_config = {
    '1': BaseEnvConfig,
    '2': TestEnvConfig,
    '3': UatEnvConfig,
    '4': ProdEnvConfig
}


class ConsulOperation:
    """
        初始化consul信息
    """

    def __init__(self, **kwargs):
        self.consul_host = kwargs['host']

        self.consul_port = kwargs['port']

        self.consul_token = kwargs['token']

        self.consul_client = consul.Consul(self.consul_host, self.consul_port, token=self.consul_token, verify=True)

        self.operation_type_dict = {
            '1': self.obtain_config_data,
            '2': self.set_up_config_data,
            '3': self.delete_config_data,
            '4': self.obtain_kv_data,
            '5': self.obtain_config_list
        }

    """
        获取现有配置列表
    """

    def obtain_config_list(self, **kwargs):
        print("获取现有配置列表信息")
        try:
            _, res = self.consul_client.kv.get(kwargs['consul_config_directory'],
                                               dc=kwargs['consul_data_center'], keys=True)

            if res is None:
                print("现有配置列表为空")
                return

            print("获取到的现有配置列表信息如下:")
            for dc in res:
                print("%s\n" % dc)

        except Exception as e:
            print("获取现有配置列表信息: %s" % e)

    """
        根据路由地址获取consul的K/V信息
    """

    def obtain_kv_data(self, **kwargs):
        print("获取%s下的K/V信息" % kwargs['consul_config_directory'])

        try:
            _, res = self.consul_client.kv.get(kwargs['consul_config_directory'])

            if res is None:
                print("K/V信息为空")
                return

            print("获取到的K/V信息如下:")
            return res
        except Exception as e:
            print("获取K/V信息错误: %s" % e)

    """
        根据K/V信息获取配置
    """

    def obtain_config_data(self, **kwargs):

        res = self.obtain_kv_data(consul_config_directory=kwargs['consul_config_directory'])

        if res is None:
            return "该路径下配置信息为空"

        if sys.version_info > (3, 0):
            return str(res['Value'], encoding="utf-8")
        else:
            return str(res['Value'])

    """
        删除指定路径下的配置信息
    """

    def delete_config_data(self, **kwargs):
        print("删除%s下的配置信息" % kwargs['consul_config_directory'])
        try:
            res = self.consul_client.kv.delete(kwargs['consul_config_directory'])

            if res is True:
                return "删除配置信息成功"
            else:
                return "删除配置信息失败"
        except Exception as e:
            print("删除配置信息错误: %s" % e)

    """
        对应路径下设置配置信息
    """

    def set_up_config_data(self, **kwargs):
        print("路径%s下设置配置信息" % kwargs['consul_config_directory'])
        try:
            res = self.consul_client.kv.put(kwargs['consul_config_directory'], value=kwargs['text'])

            if res is True:
                return "设置配置信息成功"
            else:
                return "设置配置信息失败"
        except Exception as e:
            print("设置配置信息错误: %s" % e)


"""
    根据config_directory获取绝对路径
"""


def absolute_directory(consul_env_instance, operation_type, config_directory):
    if operation_type == '5':
        return consul_env_instance.consul_router_prefix
    else:
        return '%s%s%s' % (consul_env_instance.consul_router_prefix,
                           config_directory,
                           consul_env_instance.consul_router_suffix)


"""
    非文件操作
"""


def non_file_operation(**kwargs):
    for i, cd in enumerate(str(kwargs['config_directory']).split(',')):
        print("\n----------------------------------------------------------\n")
        abs_directory = absolute_directory(kwargs['consul_env_instance'], kwargs['operation_type'], cd)

        consul_client_instance = kwargs['consul_client_instance']

        operation_type = kwargs['operation_type']

        result = consul_client_instance.operation_type_dict[operation_type](
            consul_config_directory=abs_directory, consul_data_center=kwargs['consul_data_center'])

        if result is not None:
            print(result)


"""
    文件操作
"""


def file_operation(**kwargs):
    for fp, cd in zip(str(kwargs['file_path']).split(','), str(kwargs['config_directory']).split(',')):
        print("\n----------------------------------------------------------\n")
        abs_directory = absolute_directory(kwargs['consul_env_instance'], kwargs['operation_type'], cd)

        consul_client_instance = kwargs['consul_client_instance']

        operation_type = kwargs['operation_type']

        try:
            with open(fp, 'rb') as file_stream:
                config_str = file_stream.read()
        except Exception as e:
            print("读取配置文件信息错误: %s" % e)
            return

        result = consul_client_instance.operation_type_dict[operation_type](text=config_str,
                                                                            consul_config_directory=abs_directory)
        if result is not None:
            print(result)


"""
    参数校验
"""


def params_validate(parse_args):
    if parse_args.ot == '1' or parse_args.ot == '3' or parse_args.ot == '4':
        if parse_args.cd is None:
            return 'execute command error (CONSUL操作类型: %s, -cd cannot be empty)' % parse_args.ot

    elif parse_args.ot == '2':
        if parse_args.cd is None:
            return 'execute command error (CONSUL操作类型: %s, -cd cannot be empty)' % parse_args.ot
        if parse_args.fp is None:
            return 'execute command error (CONSUL操作类型: %s, -fp cannot be empty)' % parse_args.ot


"""
    执行CONSUL操作
"""


def execute_action(parse_args):
    consul_env_instance = global_config[str(parse_args.cec)]()

    consul_client_instance = ConsulOperation(
        host=consul_env_instance.consul_host,
        port=consul_env_instance.consul_port,
        token=consul_env_instance.consul_token
    )

    if parse_args.ot == '1' or parse_args.ot == '3' or parse_args.ot == '4' or parse_args.ot == '5':
        non_file_operation(
            consul_env_instance=consul_env_instance,
            consul_client_instance=consul_client_instance,
            operation_type=parse_args.ot,
            config_directory=parse_args.cd,
            consul_data_center=consul_env_instance.consul_data_center
        )
    elif parse_args.ot == '2':
        file_operation(
            consul_env_instance=consul_env_instance,
            consul_client_instance=consul_client_instance,
            operation_type=parse_args.ot,
            config_directory=parse_args.cd,
            file_path=parse_args.fp
        )


"""
    Consul操作函数
    命令行示例:
    python consul_estimate_argparse.py
    -cec=1 
    -ot=1 
    -cd=config-example:dev
    -fp=config-example-application-dev.yml
"""


def consul_command():

    arg_parser = argparse.ArgumentParser(
        prog='consul_estimate_argparse.py',
        description='all operations from consul data center'
    )

    arg_parser.add_argument('-cec', default='1', choices=['1', '2', '3', '4'],
                     help='CONSUL环境, (1:DEFAULT, 2:TEST, 3:UAT, 4:PROD)')

    arg_parser.add_argument('-ot', default='1', choices=['1', '2', '3', '4', '5'],
                     help='CONSUL操作类型, (1:查询配置, 2:设置配置, 3:删除配置, 4:查询K/V信息, 5:配置列表)')

    arg_parser.add_argument('-cd',
                     help='CONSUL操作目录, 如:config-example或config-example:dev, 多个使用逗号分割')

    arg_parser.add_argument('-fp',
                     help='配置文件操作目录, 如:config-example-application.yml, 多个使用逗号分割')

    result = params_validate(arg_parser.parse_args())

    if result is not None:
        print(result)
        return

    execute_action(arg_parser.parse_args())


if __name__ == '__main__':
    consul_command()

