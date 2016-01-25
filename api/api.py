# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-23
"""
from weiboapi.http.request2 import *
from weiboapi.http import para
import re
import json
import traceback


p = re.compile('\((.*)\)')


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
            return True
        else:
            return False         
    except:
        traceback.print_exc()
        return False


def post(text):
    """
    Making a post.
    text: the content of the post.
    """
    data = handle_post_request(text)
    if not data:
        return False
    print(data)
    json_data = json.loads(data)
    if json_data["code"] == "100000":
        return True
    else:
        return False
