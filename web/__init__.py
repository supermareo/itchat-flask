# coding=utf-8


from flask import Flask, redirect, url_for, render_template, session, make_response, jsonify
from flask_cors import CORS
from flask_restful import Api
import uuid
from web.utils import itchat_util

app = Flask(__name__)
app.secret_key = 'secret'
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
    uid = str(uuid.uuid1())
    itchat_util.login(uid)
    return render_template('index.html', uid=uid)


@app.route('/summary/<uid>')
def summary(uid):
    return render_template('chat.html', uid=uid)


@app.route('/api/qr/<uid>')
def qr(uid):
    print('qr', uid)
    qr = itchat_util.get_qr(uid)
    success = False
    if (qr != 'None'):
        success = True
    response = make_response(jsonify({
        'success': success,
        "data": qr
    }))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/api/login_status/<uid>')
def login_status(uid):
    print('login_status', uid)
    data = itchat_util.get_login_status(uid)
    response = make_response(jsonify({
        'success': True,
        'status': data['status'],
        'qr': data['qr']
    }))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/api/self/<uid>')
def get_self_info(uid):
    print('get_self_info', uid)
    data = itchat_util.get_self_info(uid)
    response = make_response(jsonify({
        'success': True,
        'data': data
    }))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/api/sex/<uid>')
def get_sex_info(uid):
    print('get_sex_info', uid)
    data = itchat_util.get_sex_info(uid)
    response = make_response(jsonify({
        'success': True,
        'data': data
    }))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/api/contacts/<uid>')
def get_contacts(uid):
    print('get_contacts', uid)
    data = itchat_util.get_friends(uid)
    response = make_response(jsonify({
        'success': True,
        'data': data
    }))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# api.add_resource(Qr, '/api/qr')
# api.add_resource(LoginStatus, '/api/login_status')
