# TinyProxyAuthorizer
TinyProxyAuthorizer is a Flask app for self serve IP whitelisting.

*Setup*

1) Install the following packages (install line is for aptitude, modify as necessary):

apt-get install python python-pip python-virtualenv git screen

2) Clone the repo:

git clone https://github.com/PerryBhandal/TinyProxyAuthorizer.git

3) CD into the script directory:

cd tiny_proxy_authorizer

4) Copy authorized.json.default to authorized.json

cp authorized.json.default authorized.json

5) Create a virtual environment, activate it then install all dependencies.

virtualenv venv; source venv/bin/activate; pip install -r requirements/production.txt

6) Ensure your VENV is activated, then start the application in a detachable screen on a user that has write privileges on /etc/tinyproxy.conf

./start_authorizer.sh
