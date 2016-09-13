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
from weiboapi.extractor.weibo_extractor import HomepageWeiboExtractor
from .weibo import Weibo
from weiboapi.extractor.comment_extractor import CommentExtractor
from weiboapi.extractor.comment_extractor import extract_inbox_comment
from .comment import Comment
from weiboapi.extractor.account_extractor import AccountExtractor
from weiboapi.extractor.misc import *
from weiboapi.util.util import get_json
from weiboapi.util.util import check_code
from weiboapi.util.util import wrap_user_info


weibo_extractor = WeiboExtractor(Weibo)
homepage_weibo_extractor = HomepageWeiboExtractor(Weibo)
comment_extractor = CommentExtractor(Comment)
account_extractor = AccountExtractor()


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

    :param username str: the username to log in
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

    :param str username: the username to log in

    :param str password: the password of the username
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

        data = handle_request(url)
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


def post(content):
    """
    Making a post.

    :param str content: the content of the post.
    """
    data = handle_post_request(content)
    if not data:
        return False
    return check_code(data)


def repost(mid, content, comment=False):
    """
    Reposting a Weibo.
    """
    data = handle_repost_request(mid, content, comment)
    if not data:
        return False
    return check_code(data)


def comment(mid, content):
    """
    Posting a comment.

    :param str mid: the id of the Weibo on which the is comment posted.

    :param str content: the content of the comment.
    """
    data = handle_comment_request(mid, content)
    if not data:
        return False
    return check_code(data)


def reply_comment(mid, cid, ouid, nick, content):
    data = handle_reply_comment_request(mid, cid, ouid, nick, content)
    if not data:
        return False
    return check_code(data)


def get_inbox_comment():
    data = handle_get_inbox_comment_request()
    if not data:
        return None
    doc = util.check_html(data)
    return extract_inbox_comment(doc)


def get_inbox_count():
    data = handle_get_inbox_count_request()
    if not data:
        return None
    return extract_inbox_count(data)


def like(mid):
    data = handle_like_request(mid)
    if not data:
        return False
    return check_code(data)


def send_message(uid, content):
    data = handle_send_message_request(uid, content)
    if not data:
        return False

    return check_code(data)


def follow(uid, nick):
    data = handle_follow_request(uid, nick)
    if not data:
        return False
    return check_code(data)


def get_weibos(uid, domain=None, page=1, keyword=None):
    """
    Retriving the specified page of Weibo posts of a specified account.

    :param str uid: the id of the target account

    :param str domain: the domain of the account

    :param int page: specified page of the posts

    :return: a list of :class:`~weiboapi.api.weibo.Weibo` instances
    """
    if not domain:
        domain = get_domain(uid)

    weibos = []
    new_weibos = request_weibos(uid, domain, page, 1, keyword)
    if not new_weibos:
        return weibos
    else:
        weibos.extend(new_weibos)

    new_weibos = request_weibos(uid, domain, page, 2, keyword)
    if not new_weibos:
        return weibos
    else:
        weibos.extend(new_weibos)

    new_weibos = request_weibos(uid, domain, page, 3, keyword)
    if not new_weibos:
        return weibos
    else:
        weibos.extend(new_weibos)

    return weibos


def request_weibos(uid, domain, page, stage, keyword):
    if stage == 1:
        data = handle_get_weibos_request(uid, domain, page, keyword=keyword)
        if not data:
            return None
        weibos = weibo_extractor.extract_weibos(data, True)
        return check_weibos(weibos)

    elif stage == 2:
        data = handle_get_weibos_request(uid, domain, page, stage, keyword)
        if not data:
            return None
        json_data = json.loads(data)
        doc = json_data['data']
        weibos = weibo_extractor.extract_weibos(doc)
        return check_weibos(weibos)
    else:
        data = handle_get_weibos_request(uid, domain, page, stage, keyword)
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
    Retrieving a unique Weibo post using the given url.

    :param str url: the url of the Weibo to retrieve.

    :return: a :class:`weiboapi.api.weibo.Weibo` instance or `None`
    """
    data = handle_request(url)
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

    :param str mid: the id of the Weibo post

    :param int page: specified page

    :return: a list of :class:`~weiboapi.api.comment.Comment` instances
    """
    _time = util.get_systemtime()
    url = para.comment_url % (mid, page, _time)
    data = handle_request(url)
    if not data:
        return None

    json_data = json.loads(data)
    data = json_data["data"]
    doc = data["html"]
    comments = comment_extractor.extract_comments(doc)
    return comments


def get_homepage():
    page = []
    data = handle_homepage_request(para.uid, 1)
    if not data:
        return page
    doc = util.check_html(data)
    weibos = homepage_weibo_extractor.extract_weibos(doc, first=True)
    weibos = check_weibos(weibos)
    if weibos:
        page.extend(weibos)
    else:
        return page

    data = handle_homepage_request(para.uid, 2)
    if not data:
        return page
    json_data = json.loads(data)
    doc = json_data["data"]
    weibos = homepage_weibo_extractor.extract_weibos(doc)
    weibos = check_weibos(weibos)
    if weibos:
        page.extend(weibos)
    else:
        return page

    data = handle_homepage_request(para.uid, 3)
    if not data:
        return page
    json_data = json.loads(data)
    doc = json_data["data"]
    weibos = homepage_weibo_extractor.extract_weibos(doc)
    weibos = check_weibos(weibos)
    if weibos:
        page.extend(weibos)
    else:
        return page
    return page


def get_homepage_topic():
    data = handle_homepage_request(para.uid, 1)
    if not data:
        return []
    doc = util.check_html(data)
    topics = extract_topic(doc)
    return topics


def get_account(uid):
    """
    Retriving the information of the specified account.

    :param str uid: the id of the account.
    """
    data = handle_namecard_request(uid)
    if not data:
        return None
    try:
        json_data = re.findall('(\({.*}\))', data)[0]
        json_data = json.loads(json_data[1:-1])
        doc = json_data["data"]
        account = account_extractor.extract_account(doc)
        if account:
            account["uid"] = uid
        return account
    except:
        return None


def get_own_account():
    return get_account(para.uid)


def get_domain(uid):
    """
    Retriving the domain of an account.
    """
    data = handle_homepage_request(uid)
    if not data:
        return None
    return extract_domain(data)


def get_relation(uid, page=1, _type="followee"):
    """
    Retriving the relations of an account.

    :param str uid: the id of the account.

    :param str domain: the domain of the account.

    :param int page: the specified page.

    :param str _type: the type of the relations (followee or follower)

    :return: a list of dict instances or `None`
    """
    data = handle_get_relation_request(uid, page, _type)
    if not data:
        return None

    return extract_relation(data)


def get_user_info(uid, domain="100505"):
    """
    Retriving the information of the user of an account.
    """
    data = handle_get_user_info_request(uid, domain)
    if not data:
        return None
    userinfo = extract_user_info(data)
    if userinfo:
        return wrap_user_info(userinfo)


def search_user(word=None, page=1, page_num=False, tag=None, auth=None,
                region=None, gender=None, age=None):
    """
    Searching with a word to get concerned accounts.

    :param str word: the word used to search

    :param int page: the page of the result

    :param bool page_num: specified whether the number of pages is returned
    """
    data = handle_search_user_request(
        word, page, tag, auth, region, gender, age)
    if not data:
        if page_num:
            return None, None
        return None
    else:
        return extract_user(data, page_num)


def search_weibo(word, page=1, page_num=False, region=None,
                 start_date=None, end_date=None):
    """
    Searching with a word to get concerned Weibos.

    :param str word: the word used to search

    :param int page: the page of the result

    :param bool page_num: specified whether the number of pages is returned
    """
    data = handle_search_weibo_request(
        word, page, region, start_date, end_date)
    if not data:
        if page_num:
            return None, None
        return None
    else:
        return extract_searched_weibo(data, page_num)


def search_count(word):
    data = handle_search_weibo_request(word)
    if not data:
        return 0
    else:
        return extract_search_result_count(data)
