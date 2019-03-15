# coding=utf-8
import base64
import os
import threading

import itchat

instance_map = {

}

qr_map = {

}

uuid_map = {

}

login_status_map = {

}

friends_map = {

}

avatar_map = {

}


def qr_callback(uuid, status, qrcode, uid):
    print('qr_callback uuid=', uuid, 'status=', status, type(status), 'uid=', uid, 'qrcode=', qrcode)
    if '201' == status:
        # 二维码已扫描
        login_status_map[uid] = 'QR_SCAN'
        print('QR_SCAN', login_status_map)
    elif '200' == status:
        # 登录成功
        login_status_map[uid] = 'LOGIN_SUCCESS'
        print('LOGIN_SUCCESS', login_status_map)
    else:
        # 获取到二维码
        login_status_map[uid] = 'GET_QR'

    path = '/data/' + uid + '.png'
    uuid_map[uid] = uuid
    with open(path, 'wb') as f:
        f.write(qrcode)
    with open(path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        qr_map[uid] = 'data:image/png;base64,' + s
        print(qr_map[uid])
    os.remove(path)


def login_callback(uid):
    print('login_callback', uid)


def do_login(uid):
    print('do_login, uid=', uid)
    # 开始登录
    login_status_map[uid] = 'START_LOGIN'
    new_instance = itchat.new_instance_dict(uid)
    instance_map[uid] = new_instance
    new_instance.auto_login(hotReload=True, statusStorageDir=uid + 'newInstance.pkl', qrCallback=qr_callback, uid=uid)


def login(uid):
    if uid in instance_map:
        return
    threads = []
    t1 = threading.Thread(target=do_login, args=(uid,))
    threads.append(t1)
    # t2 = threading.Thread(target=sync_login_status, args=(uid,))
    # threads.append(t2)
    for thread in threads:
        thread.start()
    print('login thread complete')


def get_qr(uid):
    if uid in qr_map:
        return qr_map[uid]
    return 'None'


def get_login_status(uid):
    if (not uid in instance_map):
        return {
            'status': 'NOT_LOGIN_YET',
            'qr': None
        }
    if (not uid in uuid_map):
        return {
            'status': 'NOT_LOGIN_YET',
            'qr': None
        }
    return {
        'status': login_status_map[uid],
        'qr': qr_map[uid]
    }


def get_friends(uid):
    instance = instance_map[uid]
    friends = instance.get_friends(update=True)
    download_avatars(uid, friends)
    for friend in friends:
        friend['avatar'] = avatar_map[friend["UserName"]]
    return friends


def download_avatars(uid, friends):
    for friend in friends:
        username = friend["UserName"]
        print('download avatar of', username)
        img = itchat.get_head_img(userName=username)
        path = '../avatars/' + friend['NickName'] + "(" + friend['RemarkName'] + ").jpg"
        with open(path, 'wb') as f:
            f.write(img)
        with open(path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
            avatar_map[uid][username] = 'data:image/png;base64,' + s
        os.remove(path)

# def sync_login_status(uid):
#     while True:
#         print('check_login start')
#         if (not uid in instance_map):
#             login_status_map[uid] = 'NOT_LOGIN_YET'
#             continue
#         if (not uid in uuid_map):
#             login_status_map[uid] = 'NOT_LOGIN_YET'
#             continue
#         instance = instance_map[uid]
#         status = instance.check_login(uuid_map[uid])
#         print('check_login start complete', status)
#         if '201' == status or 201 == status:
#             # 二维码已扫描
#             login_status_map[uid] = 'QR_SCAN'
#             continue
#         if '200' == status or 200 == status:
#             # 登录成功
#             login_status_map[uid] = 'LOGIN_SUCCESS'
#             break
