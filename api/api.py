# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-23
"""
from weiboapi.http.request import *
from weiboapi import para
import re
import json
import traceback
from weiboapi.extractor.weibo_extractor import WeiboExtractor
from .weibo import Weibo
from weiboapi.extractor.comment_extractor import CommentExtractor
from .comment import Comment
from weiboapi.extractor.account_extractor import AccountExtractor
from weiboapi.extractor.misc import *


p = re.compile('\((.*)\)')
weibo_extractor = WeiboExtractor(Weibo)
comment_extractor = CommentExtractor(Comment)
account_extractor = AccountExtractor()


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


def get_weibos(uid, domain=None, page=1):
    if not domain:
        domain = get_domain(uid)

    weibos = []
    new_weibos = request_weibos(uid, domain, page, 1)
    if not new_weibos:
        return weibos
    else:
        weibos.extend(new_weibos)

    end_id = weibos[0]["mid"]
    new_weibos = request_weibos(uid, domain, page, 2, end_id)
    if not new_weibos:
        return weibos
    else:
        weibos.extend(new_weibos)

    new_weibos = request_weibos(uid, domain, page, 3)
    if not new_weibos:
        return weibos
    else:
        weibos.extend(new_weibos)

    return weibos


def request_weibos(uid, domain, page, stage, end_id=None):
    if stage == 1:
        data = handle_get_weibos_request(uid, domain, page)
        if not data:
            return None
        weibos = weibo_extractor.extract_weibos(data, True)
        return check_weibos(weibos)

    elif stage == 2:
        data = handle_get_weibos_request(uid, domain, page, stage, end_id)
        if not data:
            return None
        json_data = json.loads(data)
        doc = json_data['data']
        weibos = weibo_extractor.extract_weibos(doc)
        return check_weibos(weibos)
    else:
        data = handle_get_weibos_request(uid, domain, page, stage)
        if not data:
            return None
        json_data = json.loads(data)
        doc = json_data['data']
        weibos = weibo_extractor.extract_weibos(doc)
        return check_weibos(weibos)


def check_weibos(weibos):
    if len(weibos) == 0:
        return None
    return weibos


def get_weibo(url):
    data = handle_url_request(url)
    if not data:
        return None
    weibos = weibo_extractor.extract_weibos(data, True, single=True)
    if len(weibos) == 1:
        return weibos[0]
    else:
        return None


def get_comments(mid, page):
    _time = util.get_systemtime()
    url = para.comment_url % (mid, page, _time)
    data = handle_url_request(url)
    if not data:
        return None

    json_data = json.loads(data)
    data = json_data["data"]
    doc = data["html"]
    comments = comment_extractor.extract_comments(doc)
    return comments


def get_account(uid):
    data = handle_namecard_request(uid)
    if not data:
        return None
    json_data = re.findall('(\({.*}\))', data)[0]
    json_data = json.loads(json_data[1:-1])
    doc = json_data["data"]
    account = account_extractor.extract_account(doc)
    if account:
        account["uid"] = uid
    return account


def get_domain(uid):
    url = "http://weibo.com/u/%s/home" % uid 
    data = handle_url_request(url)
    if not data:
        return None
    return extract_domain(data)
