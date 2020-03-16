
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
        body = {"request": {"urlPattern": "^/order-service/.*"}, "response": {"proxyBaseUrl": nginx_url}}
        response = requests.post(mock_url + path, json=body)
        assert response.status_code == 201
        
        # 新增mock服务mapping
        
        body = {'id': '83de67bb-4b29-488b-a450-f915b61d0ed7', 'name': 'user-service_user_detail_u001', 'request': {'url': '/user-service/user/detail/u001', 'method': 'GET'}, 'response': {'status': 200, 'body': '{"code": 0, "msg": "success", "data": {"userId": "u001", "userName": "光头强_mock"}}', 'headers': {'Server': 'nginx/1.17.4', 'Date': 'Mon, 16 Mar 2020 09:46:34 GMT', 'Content-Type': 'application/json;charset=utf-8', 'Connection': 'keep-alive'}}, 'uuid': '83de67bb-4b29-488b-a450-f915b61d0ed7', 'persistent': True}
        response = requests.post(mock_url + path, json=body)
        assert response.status_code == 201

        body = {'id': 'd3780cf9-ca46-4965-b283-49c5ca047e41', 'name': 'ms-service_product_detail_p001', 'request': {'url': '/ms-service/product/detail/p001', 'method': 'GET'}, 'response': {'status': 200, 'body': '{"code": 0, "msg": "success", "data": {"productId": "p001", "productName": "火花塞_mock"}}', 'headers': {'Server': 'nginx/1.17.4', 'Date': 'Mon, 16 Mar 2020 09:46:34 GMT', 'Content-Type': 'application/json;charset=utf-8', 'Connection': 'keep-alive'}}, 'uuid': 'd3780cf9-ca46-4965-b283-49c5ca047e41', 'persistent': True}
        response = requests.post(mock_url + path, json=body)
        assert response.status_code == 201

        path = '/__admin/mappings/save'
        response = requests.post(mock_url + path, json=body)
        assert response.status_code == 200

        path = '/__admin/mappings/reset'
        response = requests.post(mock_url + path, json=body)
        assert response.status_code == 200

    def teardown(self):
        print('teardown')
        # 清空mapping文件
        path = '/__admin/mappings'
        requests.delete(mock_url + path)
        #
        # # 恢复初始转发状态
        body = {"request": {"method": "ANY"}, "response": {"proxyBaseUrl": nginx_url}}
        response = requests.post(mock_url + path, json=body)
        assert response.status_code == 201

        path = '/__admin/mappings/save'
        response = requests.post(mock_url + path, json=body)
        assert response.status_code == 200

        path = '/__admin/mappings/reset'
        response = requests.post(mock_url + path, json=body)
        assert response.status_code == 200
        
    def test(self):
        path = '/order-service/order/detail/r001'
        response = requests.get(mock_url + path)
        print(1111,response.json())
        # {'code': 0, 'msg': 'success', 'data': {'orderId': 'r001', 'userName': '光头强', 'productName': '火花塞'}}
        assert response.status_code == 200, u'url={},req_body={},rsp_status_code={},rsp_body={}'.format(
            response.request.url, response.request.body, response.status_code, response.text)

