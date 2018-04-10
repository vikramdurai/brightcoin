from model import *
from flask import Flask
from os import environ
import json

app = Flask(__name__)
addr = newAddress()
# port = 8080
port = int(environ["DOCKER_RUN_PORT"])
service
print("using port", port)

@app.route("/")
def index():
    resp = {
        "chain": [i.__dict__ for i in bc.chain],
    }
    return json.dumps(resp)

@app.route("/self")
def self_addr():
    resp = {
        "self": addr.__dict__
    }
    return json.dumps(resp)

@app.route("/peers")
def show_peers():
    resp = {
        "peers": [findAddress(i).__dict__ for i in addr.peers]
    }
    return json.dumps(resp)

@app.route("/peers/add_peer/<peer_ip>")
def add_peer(peer_ip):
    addr.add_peer(peer_ip, port)
    resp = {
        "peers": [findAddress(i).__dict__ for i in addr.peers]
    }
    return json.dumps(resp)

@app.route("/tx/history")
def tx_history():
    resp = {
        "tx": txHistory(),
    }
    return json.dumps(resp)

@app.route("/tx/new/<receiver>:<amount>")
def tx_new(peer_name, amount):
    if peer_name not in addr.peers:
        resp = {
            "msg": "No such peer found. please add a peer at /peers/add_peer/"
        }
        return json.dumps(resp)
    addr.pay(findAddress(peer_name), int(amount))
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
    app.run(debug=True, port=port, host="0.0.0.0")