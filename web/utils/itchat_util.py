# coding=utf-8
import base64
import os
import threading
import time
import re
from collections import Counter
import jieba

import itchat

load_friends_status_map = {}
instance_map = {}
qr_map = {}
uuid_map = {}
login_status_map = {}
friends_map = {}
avatar_map = {}
self_info_map = {}
sex_info_map = {}
avatars_info_map = {}
locations_info_map = {}
word_cloud_map = {}


def update_status(uid, status):
    login_status_map[uid] = status
    if 'LOGIN_SUCCESS' == status:
        threading.Thread(target=load_friends, args=(uid,)).start()


def qr_callback(uuid, status, qrcode, uid):
    print('qr_callback uuid=', uuid, 'status=', status, type(status), 'uid=', uid, 'qrcode=', qrcode)
    if '201' == status:
        # 二维码已扫描
        update_status(uid, 'QR_SCAN')
    elif '200' == status:
        # 登录成功
        update_status(uid, 'LOGIN_SUCCESS')
    else:
        # 获取到二维码
        update_status(uid, 'GET_QR')

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


def load_friends(uid):
    print('load friends of', uid)
    if uid in friends_map:
        print('friends of', uid, 'already exists')
        load_friends_status_map[uid] = 'COMPLETE'
        return
    load_friends_status_map[uid] = 'START'
    instance = instance_map[uid]
    friends = instance.get_friends(update=True)[1:]

    sex_info = [
        {'value': 0, 'name': '男'},
        {'value': 0, 'name': '女'},
        {'value': 0, 'name': '其它'}
    ]
    locations = {}
    sig_list = []
    for friend in friends:
        sex = friend['Sex']
        if sex == 1:
            sex_info[0]['value'] = sex_info[0]['value'] + 1
        elif sex == 2:
            sex_info[1]['value'] = sex_info[1]['value'] + 1
        else:
            sex_info[2]['value'] = sex_info[2]['value'] + 1

        province = friend['Province']
        if province.strip() == '':
            province = '其它'
        if not province in locations:
            locations[province] = 0
        locations[province] = locations[province] + 1

        signature = friend.get('Signature').strip().replace('emoji', '').replace('span', '').replace('class', '')
        rep = re.compile('1f\d+\w*|[<>/=]')
        signature = rep.sub('', signature)
        sig_list.append(signature)

    sex_info_map[uid] = sex_info
    provinces = []
    counts = []
    for province, count in locations.items():
        provinces.append(province)
        counts.append(count)
    locations_info_map[uid] = {
        'province': provinces,
        'count': counts
    }

    signatures = ''.join(sig_list)
    word_list = jieba.cut(signatures, cut_all=True)
    word_list = list(filter(lambda x: x.strip() != '', word_list))
    word_cloud_map[uid] = dict(Counter(word_list))

    load_friends_status_map[uid] = 'LOADED'
    download_avatars(instance, uid, friends)
    avatars = []
    for friend in friends:
        avatar = avatar_map[uid][friend["UserName"]]
        friend['avatar'] = avatar
        avatars.append(avatar)
    avatars_info_map[uid] = avatars
    friends_map[uid] = friends
    load_friends_status_map[uid] = 'COMPLETE'
    print('load friends of', uid, 'complete')
    return friends


def get_self_info(uid):
    if uid in self_info_map:
        return self_info_map[uid]
    print('load_friends_status', load_friends_status_map)
    while uid in load_friends_status_map and load_friends_status_map[uid] != 'LOADED' and load_friends_status_map[
        uid] != 'COMPLETE':
        time.sleep(1)
    print('load_friends_status', load_friends_status_map)
    self_info = instance_map[uid].search_friends()
    self_info['avatar'] = user_avatar_base64(uid, self_info)
    self_info_map[uid] = self_info
    return self_info


def get_sex_info(uid):
    while not uid in sex_info_map:
        time.sleep(1)
    return sex_info_map[uid]


def get_avatars(uid):
    while not uid in avatars_info_map:
        time.sleep(1)
    return avatars_info_map[uid]


def get_locations(uid):
    while not uid in locations_info_map:
        time.sleep(1)
    return locations_info_map[uid]


def get_word_cloud(uid):
    while not uid in word_cloud_map:
        time.sleep(1)
    return word_cloud_map[uid]


def get_friends(uid):
    while uid in load_friends_status_map and load_friends_status_map[uid] != 'COMPLETE':
        print('friends is loading...')
        time.sleep(1)
        continue
    return friends_map[uid]


def user_avatar_base64(uid, user):
    username = user["UserName"]
    if uid in avatar_map and username in avatar_map[uid]:
        return avatar_map[uid][username]
    instance = instance_map[uid]
    img = instance.get_head_img(userName=username)
    path = 'U_' + user['NickName'] + "(" + user['RemarkName'] + ").jpg"
    with open(path, 'wb') as f:
        f.write(img)
    with open(path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
    os.remove(path)
    return 'data:image/png;base64,' + s


def download_avatars(instance, uid, friends):
    if not uid in avatar_map:
        avatar_map[uid] = {}
    for friend in friends:
        username = friend["UserName"]
        if username in avatar_map[uid]:
            continue
        print('download avatar of', username)
        img = instance.get_head_img(userName=username)
        path = friend['NickName'] + "(" + friend['RemarkName'] + ").jpg"
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
