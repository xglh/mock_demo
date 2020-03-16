from flask import Flask
import json, time, requests
from serivce_demo.config import *

app = Flask(__name__)


@app.route('/order-service/order/detail/<order_id>', methods=['GET'])
def order_detail(order_id):
    user_id = 'u001'
    product_id = 'p001'

    url = '{}/user-service/user/detail/{}'.format(getaway_url, user_id)
    response = requests.get(url)
    user_name = response.json()['data']['userName']

    url = '{}/ms-service/product/detail/{}'.format(getaway_url, product_id)
    response = requests.get(url)
    product_name = response.json()['data']['productName']

    rsp_body = {
        "code": 0,
        "msg": "success",
        "data": {
            "orderId": order_id,
            "userName": user_name,
            "productName": product_name,
        }
    }
    return json.dumps(rsp_body), 200, {'Content-Type': 'application/json;charset=utf-8'}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=True)
