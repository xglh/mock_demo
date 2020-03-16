#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/14 23:06
# @Author  : liuhui
# @Detail  : mock操作
import requests
import json

mock_url = 'http://localhost:9000'
nginx_url = 'http://localhost:80'


def check_mock_record_status():
    # 检查mock服务状态
    path = '/__admin/recordings/status'
    response = requests.get(mock_url + path)
    rsp_json = response.json()
    mock_status = rsp_json.get('status')
    result = True if mock_status == 'Recording' else False
    return result


# 初始化mock服务，mock地址指向nginx网关，并开启露珠
def mock_start():
    is_recording = check_mock_record_status()
    # 清空mapping文件
    path = '/__admin/mappings'
    requests.delete(mock_url + path)
    if not is_recording:
        # 将请求转发到nginx网关,并开始录制
        path = '/__admin/recordings/start'
        body = {
            "targetBaseUrl": nginx_url
        }
        requests.post(mock_url + path, json=body)
    else:
        path = '/__admin/mappings'
        # 新增目标服务proxy规则
        body = {"request": {"method": "ANY"}, "response": {"proxyBaseUrl": nginx_url}}
        requests.post(mock_url + path, json=body)

    # 检查mock服务状态
    path = '/__admin/recordings/status'
    response = requests.get(mock_url + path)
    rsp_json = response.json()
    mock_status = rsp_json.get('status')
    print('mock录制状态为:{}'.format(mock_status))


# 停止录制并获取mapping文件
def mock_stop():
    # 停止录制并获取mapping文件
    path = '/__admin/recordings/stop'
    response = requests.post(mock_url + path)
    mappings = response.json().get('mappings', [])

    # 检查mock服务状态
    path = '/__admin/recordings/status'
    response = requests.get(mock_url + path)
    rsp_json = response.json()
    mock_status = rsp_json.get('status')
    print('mock录制状态为:{}'.format(mock_status))
    return mappings


# mock服务
def mock_service(bypass_service):
    '''
    mock服务
    :param bypass_service: 过滤掉的服务，正常使用
    :param mappings: 原始录制的mappings文件
    :return:
    '''
    # 需要mock的服务列表

    mappings = mock_stop()
    mock_start()
    path = '/__admin/mappings'
    # 清空mock文件
    requests.delete(mock_url + path)

    # 重置转发规则
    body = {
        "request": {
            "urlPattern": "^/{}/.*".format(bypass_service)
        },
        "response": {
            "proxyBaseUrl": nginx_url
        }
    }

    requests.post(mock_url + path, json=body)

    for mapping in mappings:
        uuid, name = mapping.get('uuid'), mapping.get('name')
        proxy_base_url = mapping.get('response', {}).get('proxyBaseUrl')
        service_name = name.split('_')[0]
        # 过滤掉proxy规则
        if not proxy_base_url and service_name != bypass_service:
            # 写入被mock的服务请求
            requests.post(mock_url + path, json=mapping)

    # 检查mock服务状态
    path = '/__admin/recordings/status'
    response = requests.get(mock_url + path)
    rsp_json = response.json()
    mock_status = rsp_json.get('status')
    print('mock录制状态为:{}'.format(mock_status))


if __name__ == '__main__':
    mock_start()
