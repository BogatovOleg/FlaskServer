from flask import Flask

application = Flask(__name__)
app = application


@application.route('/')
def hello_world():
    return 'Hi, its my Alice Prog:)'
