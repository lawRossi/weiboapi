# -*- coding:utf-8 -*-
"""
:Author: Rossi
:Date: 2016-01-23

This module contains all useful Sina Weibo api functions.
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
    """
    Extracting json data from the given string.
    """
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
    Logging in sina weibo using username and password.
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
    """
    Checking the response code. If the request is handled correctly,
    the code would be '100000'.
    """
    json_data = json.loads(data)
    if json_data["code"] == "100000":
        return True
    else:
        return False


def post(content):
    """
    Making a post.
    :param str content: the content of the post.
    """
    data = handle_post_request(content)
    if not data:
        return False
    return check_code(data)


def comment(mid, content):
    """
    Posting a comment.
    mid: the id of the Weibo on which the is comment posted.
    content: the content of the comment.
    """
    data = handle_comment_request(mid, content)
    if not data:
        return False
    return check_code(data)


def get_weibos(uid, domain=None, page=1):
    """
    Retriving the specified page of Weibo posts of a specified account.
    :param str uid: the id of the target account.
    :param str domain: the domain of the account.
    :param int page: specified page of the posts.
    """
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
    """
    Retriving a unique Weibo post using the given url.
    """
    data = handle_url_request(url)
    if not data:
        return None
    weibos = weibo_extractor.extract_weibos(data, True, single=True)
    if len(weibos) == 1:
        return weibos[0]
    else:
        return None


def get_comments(mid, page):
    """
    Retriving the specified page of comments of the specified Weibo post.
    mid: the id of the Weibo post
    page: specified page
    """
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
    """
    Retriving the information of the specified account.
    uid: the id of the account.
    """
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
    """
    Retriving the domain of an account.
    uid: the id of the account.
    """
    data = handle_homepage_request(uid)
    if not data:
        return None
    return extract_domain(data)


def get_relation(uid, domain=None, page=1, _type="followee"):
    """
    Retriving the relations of an account.
    uid: the id of the account.
    domain: the domain of the account.
    page: the specified page.
    _type: the type of the relations (followee or follower)
    """
    if not domain:
        domain = get_domain(uid)
    data = handle_get_relation_request(uid, domain, page, _type)
    if not data:
        return

    return extract_relation(data)


def get_user_info(uid, domain="100505"):
    """
    Retriving the information of the user of an account.
    uid: the id of the account.
    domain: the domain of the account.
    """
    data = handle_get_user_info_request(uid, domain)
    if not data:
        return
    return extract_user_info(data)


def is_verified(uid):
    """
    Checking whether an account is verified.
    """
    data = handle_homepage_request(uid)
    if not data:
        return
    if data.find("verify_area") != -1:
        return True
    return False
