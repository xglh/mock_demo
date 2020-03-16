#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/14 23:06
# @Author  : liuhui
# @Detail  :
import json

def gen_script_from_mappings(bypass_service):
    '''
    根据mappings文件生成脚本
    :param bypass_service:
    :return:
    '''
    pass

a = '{"code": 0, "msg": "success", "data": {"userId": "u001", "userName": "光头强"}}'
print(json.loads(a))