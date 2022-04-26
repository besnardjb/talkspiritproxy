from flask import Flask
from flask import request, abort
import json
import time
import re
import requests

app = Flask(__name__)

forward_url = None
forward_ident = {"title" : "TalkSpirit Proxy",
                 "name" : "TalkSpirit Proxy",
                 "url" : "",
                 "icon" : "" }

def replace_urls(text):
    urls = re.findall(r"<([^\|]+)\|([^>]+)>", text)
    out_text = text
    for url in urls:
        out_text = out_text.replace("<{}|{}>".format(url[0], url[1]), "{} ({})".format(url[1], url[0]))
    return out_text

def forward_request(msg):
    global forward_url
    fmsg = {}
    # Unfold Main message
    thread_id = time.time()

    fmsg["title"] = forward_ident["title"]
    fmsg["content"] = replace_urls(msg["text"])
    fmsg["thread_id"] = str(thread_id)

    fmsg["contact"] = {
        "display_name": forward_ident["name"],
        "url": forward_ident["url"],
        "icon": forward_ident["icon"]
    }

    print(fmsg)
    response = requests.post(forward_url, json=fmsg)
    print(response.text)

    if "attachments" in msg:
        del fmsg["title"]

        for att in msg["attachments"]:
            fmsg["content"] = replace_urls(att["text"])
            print(fmsg)
            response = requests.post(forward_url, json=fmsg)
            print(response.text)


def handle_request(data):
    if not "payload" in data:
        return '404'
    
    try:
        msg = json.loads(data["payload"])
        forward_request(msg)
        return '200'
    except Exception as e:
        raise e


@app.route("/", methods=['POST'])
def indx():
    if request.method == 'POST':
        return handle_request(request.form)

    return '200'

def tsproxy(listen, forward, ident):
    global forward_url
    global forward_ident
    forward_url = forward
    if ident:
        forward_ident = ident
    app.run(host='0.0.0.0', port=listen)