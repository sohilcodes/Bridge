from flask import Flask, request, jsonify
import requests
import time
import threading

app = Flask(__name__)
import os
API_KEY = os.environ.get("API_KEY")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

PANEL_URL = "https://n1panel.com/api/v2"

orders = []  # 🔥 store orders

# ✅ ORDER CREATE
@app.route('/order', methods=['GET'])
def order():

    service = request.args.get("service")
    link = request.args.get("link")
    quantity = request.args.get("qty")
    user_id = request.args.get("user")

    data = {
        "key": API_KEY,
        "action": "add",
        "service": service,
        "link": link,
        "quantity": quantity
    }

    res = requests.post(PANEL_URL, data=data).json()

    if "order" in res:

        order_id = res["order"]

        # 🔥 SAVE ORDER FOR TRACKING
        orders.append({
            "order_id": order_id,
            "user_id": user_id
        })

        return jsonify({"order": order_id})

    return jsonify(res)

# ✅ STATUS CHECK LOOP
def check_orders():

    while True:

        for o in orders:

            order_id = o["order_id"]
            user_id = o["user_id"]

            data = {
                "key": API_KEY,
                "action": "status",
                "order": order_id
            }

            res = requests.post(PANEL_URL, data=data).json()

            if res.get("status") == "Completed":

                # 🔥 SEND MESSAGE TO USER
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    data={
                        "chat_id": user_id,
                        "text": f"🎉 Your order {order_id} is completed!"
                    }
                )

                orders.remove(o)

        time.sleep(30)

# START THREAD
threading.Thread(target=check_orders).start()

@app.route('/')
def home():
    return "Running 🚀"

app.run(host="0.0.0.0", port=10000)
