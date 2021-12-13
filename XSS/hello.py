# Source : https://null-byte.wonderhowto.com/how-to/write-xss-cookie-stealer-javascript-steal-passwords-0180833/

from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello world!'