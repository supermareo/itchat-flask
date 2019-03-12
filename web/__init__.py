# coding=utf-8


from flask import Flask, request, redirect, url_for, send_file, render_template, Blueprint
from flask_restful import Api
from flask_cors import CORS
from web.resource.helloworld import HelloWorld
from web.resource.index import Index

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 用于处理跨域问题

'''添加api资源'''
api = Api(app)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 首页
@app.route('/')
def index():
    return redirect(url_for('login'))


# 登录页
@app.route('/login')
def login():
    return render_template('index.html')


@app.route('/summary')
def chat():
    return render_template('chat.html')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# api.add_resource(Index, '/')


# api.add_resource(Index, '/index')
# api.add_resource(HelloWorld, '/api/index')
