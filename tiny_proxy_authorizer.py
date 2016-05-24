from flask import Flask, request, get_flashed_messages, redirect, flash
from subprocess import call
import json

import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.route('/')
def index():
    authorized_list = get_authorized_list()

    user_ip = request.remote_addr

    to_flash = "<b>"
    messages = get_flashed_messages()
    if messages:
        for message in messages:
            to_flash += message
            to_flash += "<br/><br/>"
    to_flash += "</b>"

    if user_ip in authorized_list["authorized"]:
        return to_flash + "Your IP (%s) is already authorized on this proxy.<br /><br /> Click <a href=\"/deauthorize\">here</a> to de-authorize this IP." % user_ip
    else:
        return to_flash + "<html><body><a href=\"/authorize\">Authorize this IP (%s)</a></body></html>" % user_ip

@app.route('/authorize')
def authorize():
    addr_auth(request.remote_addr, authorize=True)
    flash("This IP has been authorized.")
    return redirect("/")

@app.route('/deauthorize')
def deauthorize():
    addr_auth(request.remote_addr, authorize=False)
    flash("This IP has been de-authorized.")
    return redirect("/")

def addr_auth(addr, authorize=True):
    authorized_list = get_authorized_list()

    if authorize:
        authorized_list["authorized"].append(addr)
    else:
        authorized_list["authorized"].remove(addr)

    write_authorized_list(authorized_list)
    write_proxy_conf()

def get_authorized_list():
    with open("authorized.json") as data_file:
        return json.load(data_file)

def write_authorized_list(data_dict):
    with open("authorized.json", 'w') as data_file:
        json.dump(data_dict, data_file)

def write_proxy_conf():
    with open("tinyproxy.conf.default") as conf_file:
        default_conf = conf_file.read()

    authorized_list = get_authorized_list()

    with open("/etc/tinyproxy.conf", 'w') as conf_write:
        conf_write.write(default_conf)

        for address in authorized_list["authorized"]:
            conf_write.write("Allow %s\n" % address)

    call("/etc/init.d/tinyproxy restart".split(" "))

if __name__ == '__main__':
    app.run(host="0.0.0.0")
