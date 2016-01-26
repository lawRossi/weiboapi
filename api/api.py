# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-23
"""
from weiboapi.http.request import *
from weiboapi.http import para
import re
import json
import traceback
from weiboapi.extractor.weibo_extractor import WeiboExtractor
from .weibo import Weibo


p = re.compile('\((.*)\)')
weibo_extractor = WeiboExtractor(Weibo)


def get_json(data):
    json_data = p.search(data).group(1)
    json_data = json.loads(json_data)
    return json_data


def extract_url(data):
    start_pos = data.find('location.replace')
    end_pos = data.find('\');})')
    s = data[start_pos:end_pos]
    start_pos = s.find('http:')
    url = s[start_pos:]
    return url


def get_prelogin_parameters(username):
    """
    Getting parameters that are needed to login.
    username: the uername to login.
    """
    data = handle_prelogin_request(username)
    if not data:
        return False

    data = get_json(data)

    para.servertime = data['servertime']
    para.nonce = data['nonce']
    para.publickey = data['pubkey']
    para.rsakv = data['rsakv']
    return True


def login(username, password):
    """
    Logging in sina weibo using username and password
    """
    if not get_prelogin_parameters(username):
        return False

    if not handle_session_request():
        return False

    data = handle_login_request(username, password)
    if not data:
        return False
    try:
        url = extract_url(data)
        if not url:
            return False
        
        data = handle_url_request(url)
        if not data:
            return False
        json_data = get_json(data)
        if(json_data['result']):
            para.uid = json_data['userinfo']['uniqueid']
            return True
        else:
            return False         
    except:
        traceback.print_exc()
        return False


def check_code(data):
    json_data = json.loads(data)
    if json_data["code"] == "100000":
        return True
    else:
        return False

def post(content):
    """
    Making a post.
    content: the content of the post.
    """
    data = handle_post_request(content)
    if not data:
        return False
    return check_code(data)


def comment(mid, rid, content):
    data = handle_comment_request(mid, rid, content)
    if not data:
        return False
    print(data)
    return check_code(data)


def get_weibos(uid, domain='100505', page=1):
    weibos = []
    data = handle_get_weibos_request(uid, domain, page)
    if not data:
        return None

    weibos.extend(weibo_extractor.extract_weibos(data, True))

    return weibos
