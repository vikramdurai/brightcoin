from model import *
from flask import Flask
import json

app = Flask(__name__)
addr = newAddress()

@app.route("/")
def index():
    resp = {
        "chain": [i.__dict__ for i in bc.chain],
    }
    return json.dumps(resp)

@app.route("/tx/history")
def tx_history():
    resp = {
        "tx": txHistory(),
    }
    return json.dumps(resp)

@app.route("/tx/new/<receiver>:<amount>")
def tx_new(receiver, amount):
    addr.pay(findAddress(receiver), int(amount))
    resp = {
        "msg": "Transaction registered. Please wait until verification.",
        "pending": bc.pending,
    }
    return json.dumps(resp)

@app.route("/mine/<msg>")
def mine(msg):
    addr.mine(msg)
    resp = {
        "msg": "New block mined!",
        "block": bc.chain[-1].__dict__,
    }
    return json.dumps(resp)

if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")