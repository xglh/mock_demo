#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/14 23:28
# @Author  : liuhui
# @Detail  : mock服务演示
from case.mock_ops import *

if __name__ == '__main__':
    # 分步执行
    # 初始化服务并开始录制
    #mock_start()

    # mock服务
    mock_service('order-service')
