# 一.安装依赖包

## 1.python3.x

```shell
python packages_install.py -p=3
```

## 2.python2.x

### 1.argparse版本

```shell
python packages_install.py -p=1,3,4,5,6,7,8
```



### 2.click版本

```shell
python packages_install.py -p=1,2,3,4,5,6,7,8
```

# 二.CONSUL操作

## 1.argparse版本

### 1.查询配置信息（示例）

```shell
python consul_estimate_argparse.py -cec='根据具体环境修改' -ot=1 -cd=config-example,config-example:dev
```



### 2.设置配置信息（示例）

```shell
python consul_estimate_argparse.py -cec='根据具体环境修改' -ot=2 -cd=config-example,config-example:dev \
  -fp=configs/config-example/config-example-application.yml,configs/config-example/config-example-application-dev.yml
```



### 3.删除配置信息（示例）

```shell
python consul_estimate_argparse.py -cec='根据具体环境修改' -ot=3 -cd=config-example,config-example:dev
```



### 4.查看K/V信息（示例）

```shell
python consul_estimate_argparse.py -cec='根据具体环境修改' -ot=4 -cd=config-example,config-example:dev
```



### 5.查询现有配置列表信息（示例）

```shell
python consul_estimate_argparse.py -cec='根据具体环境修改' -ot=5
```





## 2.click版本

### 1.查询配置信息（示例）

```shell
python consul_estimate_click.py -cec='根据具体环境修改' -ot=1 -cd=config-example,config-example:dev -fp=''

```



### 2.设置配置信息（示例）

```shell
python consul_estimate_click.py -cec='根据具体环境修改' -ot=2 -cd=config-example,config-example:dev \
  -fp=configs/config-example/config-example-application.yml,configs/config-example/config-example-application-dev.yml

```



### 3.删除配置信息（示例）

```shell
python consul_estimate_click.py -cec='根据具体环境修改' -ot=3 -cd=config-example,config-example:dev -fp=''

```



### 4.查看K/V信息（示例）

```shell
python consul_estimate_click.py -cec='根据具体环境修改' -ot=4 -cd=config-example,config-example:dev -fp=''

```



### 5.查询现有配置列表信息（示例）

```shell
python consul_estimate_click.py -cec='根据具体环境修改' -ot=5 -cd='' -fp=''

```





