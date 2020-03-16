from flask import Flask
import json, time, requests

app = Flask(__name__)


@app.route('/ms-service/product/detail/<product_id>', methods=['GET'])
def order_detail(product_id):
    rsp_body = {
        "code": 0,
        "msg": "success",
        "data": {
            "productId": product_id,
            "productName": '火花塞',
        }
    }
    return json.dumps(rsp_body), 200, {'Content-Type': 'application/json;charset=utf-8'}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8003, debug=True)
