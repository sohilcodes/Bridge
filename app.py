from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "52741a2f115d3ab8668cc836c9c516ab"
PANEL_URL = "https://n1panel.com/api/v2"

@app.route('/order', methods=['GET'])
def order():

    service = request.args.get("service")
    link = request.args.get("link")
    quantity = request.args.get("qty")

    data = {
        "key": API_KEY,
        "action": "add",
        "service": service,
        "link": link,
        "quantity": quantity
    }

    res = requests.post(PANEL_URL, data=data).json()

    return jsonify(res)

app.run(host="0.0.0.0", port=10000)
