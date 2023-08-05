# featureview 使用说明文档

## 一、软件介绍

- 名称：featureview
- 用途：打开录制的 * .MF4 文件，读取并显示里面的变量信息。

## 二、 安装说明

### 2.1 测试电脑是否已安装 python3

首先需要确定电脑是否已经安装了 python3，请按如下步骤测试：
- 打开 cmd
- 输入: python -V
- 查看上一步的结果是否是 python2.* 。因为公司有的软件依赖于python2版本，所以这里必须显示为 python 版本为 2. *
- 输入： pip -V
- 查看上一步的结果是否显示关联到 python2. * 版本
- 输入：python3 -V
- 查看上一步的结果是否显示是python3.* ，如果正常，则说明已安装了python3版本
- 输入：pip3 -V
- 查看上一步的结果是否显示关联到 python3.* ，如果正常，则说明已安装了 pip3并且关联到python3

解释： pip 是python安装外部模块的管理程序。

如果已上都显示正确，可直接跳到 2.5，否则向下依次安装

### 2.2 安装 python3
注：不支持3.8版本，请下载3.7.4以上的子版本即可。
- 前往网址： https://www.python.org/downloads/ 下载python3.7.4的win10安装包。（其它版本未测试）
- 双击下载下来的安装包 python-3.7.4.exe 进行安装，安装过程中请勾选以下选项：
将python可执行程序添加到路径（add to PATH)；安装路径选择本用户，不要使用全局或重新选定路径；其它默认即可。

### 2.3 解决python2 与 python3 的兼容性问题

- 进入 python3 的安装路径文件夹中：C:\Users<user-name>\AppData\Local\Programs\Python\Python37-32， 其中 user-name 是使用帐户名 
- 复制本文件夹内的 python.exe，并粘贴在本文件夹内，并修改粘贴后文件名为 python3.exe.

### 2.4 测试 python3 安装是否成功

重新按照 2.1中的指令进行测试，如果一切正常则跳到2.5, 否则请联系我。

### 2.5 安新 featureview 模块

- 如果电脑联网的话，打开 cmd， 输入指令： pip3 install featureview
- 如果未联网，可联系我离线安装。

如果网络不好，导致pip3安装模块速度太慢，可以更换国内的清华开源镜像源后安装，参考网址：https://mirrors.tuna.tsinghua.edu.cn/help/pypi/

如果安装正常，可在路径：C:\Users<user-name>\AppData\Local\Programs\Python\Python37\Scripts 下找到一个文件名为：featureview* .exe ，双击即可打开软件，也可以将此文件创建桌面快捷方式使用。

## 三、软件打包指令
- python3 -m pip install --user --upgrade setuptools wheel
- python3 setup.py sdist bdist_wheel

打包后的文件在dist文件夹下

## 四、本文档说明

- 版本： v1.0
- 作者： Andy.Yang
- 部门： Radar.Feature

- 版本： v1.1
- 作者： Jiahui.Lu
- 部门： Radar.Feature

## 五、版本更新说明
- 1.0.4 改动了xy.py & data_process.py 来适配新的格式的数据
- 1.0.3 将install_requires中的依赖项版本固定
- 1.0.2 修改了setup.py中install_requires，增加了版本要求
- 1.0.1 修复了一个Bug。由于上一个版本中 requirements.txt 未指定依赖包的版本，导致依赖包更新时某些API被弃用。本次在此文件中指定了开发时的版本
- 1.0.0 在当前版本下测试正常