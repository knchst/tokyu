import os
import json
import requests
import time
from flask import Flask
from flask import jsonify
from slackclient import SlackClient

app = Flask(__name__)

@app.route('/')
def index():
    r = requests.get('http://www.tokyu.co.jp/unten/unten2.json')
    unten2_json = r.json()
    check_dt = unten2_json['check_dt']

    # { message: "平常運転", className:"no" }, // 0
    # { message: "遅れ", className:"d" }, // 1
    # { message: "運転見合せ", className:"sd" } // 2

    if check_dt.find("0") == -1:
        ts = int(time.time())
        color = "warning"
        fallback = unten2_json['unten_dt']
        attachments = '[{ "footer": "東急電鉄", "footer_icon": "https://www.google.com/s2/favicons?domain=http://www.tokyu.co.jp", "ts": %d, "author_icon": "http://www.tokyu.co.jp/unten/img/line_ic03.gif", "author_name": "田園都市線", "color": "%s", "fallback": "%s", "text": "%s\\n詳細は<http://www.tokyu.co.jp/unten/unten.php|こちら>から確認できます" }]' % (ts, color, fallback, fallback)

        sc = SlackClient("xoxp-285677563351-284750146325-292155930135-0c15855c6af39e018569e716c76d7741")
        sc.api_call(
          "chat.postMessage",
          channel="#notification",
          attachments=json.loads(attachments)
        )

    return jsonify(unten2_json)
