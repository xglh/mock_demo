from flask import Flask
import json, time, requests

app = Flask(__name__)


@app.route('/user-service/user/detail/<user_id>', methods=['GET'])
def order_detail(user_id):
    rsp_body = {
        "code": 0,
        "msg": "success",
        "data": {
            "userId": user_id,
            "userName": '光头强',
        }
    }
    return json.dumps(rsp_body), 200, {'Content-Type': 'application/json;charset=utf-8'}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8002, debug=True)
