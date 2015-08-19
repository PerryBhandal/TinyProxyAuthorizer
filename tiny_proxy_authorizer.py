from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    authorized_list = get_authorized_list()

    user_ip = request.remote_addr

    if user_ip in authorized_list["authorized"]:
        return "Your IP (%s) is already authorized on this proxy." % user_ip
    else:
        return "<html><body><a href=\"/authorize\">Authorize this IP (%s)</a></body></html>" % user_ip

@app.route('/authorize')
def authorize():
    authorized_list = get_authorized_list()
    authorized_list["authorized"].append(request.remote_addr)
    write_authorized_list(authorized_list)
    write_proxy_conf()
    return "This IP has been authorized."

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

if __name__ == '__main__':
    app.run(debug=True)
