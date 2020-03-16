#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/15 9:03
# @Author  : liuhui
# @Detail  : mock录制回放
import json
from case.mock_ops import *

script_template = '''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/14 23:28
# @Author  : liuhui
# @Detail  : mock录制回放演示

import requests
from case.mock_ops import mock_url, nginx_url, mock_start

class TestOrderClass:

    def setup(self):
        print('setup')
        mock_start()
        # 清空mapping文件
        path = '/__admin/mappings'
        requests.delete(mock_url + path)
        
        # 新增目标服务proxy规则
        body = {{"request": {{"urlPattern": "^/{bypass_service}/.*"}}, "response": {{"proxyBaseUrl": nginx_url}}}}
        response = requests.post(mock_url + path, json=body)
        assert response.status_code == 201
        
        # 新增mock服务mapping
        {add_mapping_scripts}
    def teardown(self):
        print('teardown')
        # 清空mapping文件
        path = '/__admin/mappings'
        requests.delete(mock_url + path)
        
        # 恢复初始转发状态
        body = {{"request": {{"method": "ANY"}}, "response": {{"proxyBaseUrl": nginx_url}}}}
        response = requests.post(mock_url + path, json=body)
        assert response.status_code == 201
        
    def test(self):
        {api_test_scripts}
'''

# 新增mapping模板
add_mapping_template = '''
        body = {mapping}
        response = requests.post(mock_url + path, json=body)
        assert response.status_code == 201
'''
# 接口测试模板
api_test_template = '''
        path = '{path}'
        response = requests.get(mock_url + path)
        # {rsp_body}
        assert response.status_code == 200, u'url={{}},req_body={{}},rsp_status_code={{}},rsp_body={{}}'.format(
            response.request.url, response.request.body, response.status_code, response.text)\n'''


# 处理中文显示问题
def deal_mapping_data(mapping):
    try:
        response_body = mapping['response']['body']
        mapping['response']['body'] = json.dumps(json.loads(response_body), ensure_ascii=False)
    except Exception:
        pass


# 生成自动化脚本
def gen_test_script(bypass_service, mappings, case_name):
    add_mapping_scripts, api_test_scripts = '', ''

    for mapping in mappings:
        uuid, name = mapping.get('uuid'), mapping.get('name')
        proxy_base_url = mapping.get('response', {}).get('proxyBaseUrl')
        service_name = name.split('_')[0]
        # 过滤掉proxy规则
        if not proxy_base_url:
            deal_mapping_data(mapping)
            # 非bypass_service写入mapping文件
            if service_name != bypass_service:
                add_mapping_scripts += add_mapping_template.format(mapping=mapping)
            # bypass_service为测试服务，请求写入api_test_scripts
            else:
                method, url = mapping.get('request', {}).get('method'), mapping.get('request', {}).get('url')
                rsp_body = mapping.get('response', {}).get('body', {})
                api_test_scripts += api_test_template.format(path=url, rsp_body=json.loads(rsp_body))

    case_script = script_template.format(bypass_service=bypass_service, add_mapping_scripts=add_mapping_scripts,
                                         api_test_scripts=api_test_scripts)
    with open(case_name, 'w+', encoding='utf-8') as f:
        f.write(case_script)


if __name__ == '__main__':
    # 分步执行
    # 1、开始录制
    # mock_start()

    # 2、结束录制并获取mappings文件
    mappings = mock_stop()
    # 生成自动化脚本
    gen_test_script('order-service', mappings, 'case_002.py')
