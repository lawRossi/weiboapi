# -*- coding: utf-8 -*-
"""
@Author: Rossi
2016-01-25
This module contains functions that deal with all http requests.
"""
from weiboapi.util import util
from weiboapi import para
try:
    from urllib import urlencode  # py2
except:
    from urllib.parse import urlencode  # py3

try:
    import urllib2 as request  # py2
except:
    import urllib.request as request  # py3

try:
    from cookielib import LWPCookieJar  # py2
except:
    from http.cookiejar import LWPCookieJar  # py3
import traceback


def install_opener():
    # Installing cookie jar.
    cj = LWPCookieJar()
    cookie_support = request.HTTPCookieProcessor(cj)
    opener = request.build_opener(cookie_support, request.HTTPHandler)
    request.install_opener(opener)


def install_handler(func):
    """
    A decorator.
    """
    def handle(*args, **kwargs):
        req = func(*args, **kwargs)
        return handle_request(req)

    return handle


def handle_request(req):
    """
    Handling request.

    :param req: the request
    :type req: str or request.Request
    """
    try:
        if not isinstance(req, request.Request):
            req = request.Request(
                url=req,
                headers=para.headers
            )
        data = request.urlopen(req).read()
        return util.decode(data)
    except:
        traceback.print_exc()
        return None


@install_handler
def handle_prelogin_request(username):
    """
    """
    install_opener()
    username = util.quote_base64_encode(username)
    st = util.get_systemtime()
    url = para.prelogin_url % (username, st)
    return url


def handle_session_request():
    try:
        request.urlopen(para.session_url).read()
        return True
    except:
        traceback.print_exc()
        return False


def handle_login_request(username, password):
    psw = util.encrypt_password(
        password, para.servertime, para.nonce,
        para.publickey, para.rsakv
    )
    para.request_body['sp'] = psw
    para.request_body['su'] = util.base64_encode(username)
    para.request_body['rsakv'] = para.rsakv
    para.request_body['nonce'] = para.nonce
    para.request_body['servertime'] = str(para.servertime)
    postdata = urlencode(para.request_body)
    postdata = bytearray(postdata, "utf-8")
    para.headers['Referer'] = 'http://weibo.com'
    req = request.Request(
        url=para.login_url,
        data=postdata,
        headers=para.headers
    )
    try:
        data = request.urlopen(req).read()
        return util.decode(data, "gbk")
    except:
        traceback.print_exc()
        return None


@install_handler
def handle_post_request(content):
    para.post_form['text'] = content
    data = urlencode(para.post_form)
    url = para.post_url % util.get_systemtime()
    req = request.Request(
        url=url,
        data=bytearray(data, 'utf-8'),
        headers=para.headers
    )
    return req


@install_handler
def handle_repost_request(mid, content, comment):
    para.repost_form["mid"] = mid
    para.repost_form["reason"] = content
    if comment:
        para.repost_form["is_comment_base"] = 1
    elif "is_comment_base" in para.repost_form:
            del(para.repost_form["is_comment_base"])

    data = urlencode(para.repost_form)
    url = para.repost_url % (para.uid, util.get_systemtime())
    req = request.Request(
        url=url,
        data=bytearray(data, 'utf-8'),
        headers=para.headers
    )
    return req


@install_handler
def handle_send_message_request(uid, content):
    para.message_form["uid"] = uid
    para.message_form["text"] = content
    data = urlencode(para.message_form)
    url = para.send_message_url % util.get_systemtime()
    headers = para.headers.copy()
    headers["X-Requested-With"] = "XMLHttpRequest"
    req = request.Request(
        url=url,
        data=bytearray(data, 'utf-8'),
        headers=headers
    )
    return req


@install_handler
def handle_comment_request(mid, content):
    para.comment_form['mid'] = mid
    para.comment_form['uid'] = para.uid
    para.comment_form['content'] = content
    data = urlencode(para.comment_form)
    url = para.post_comment_url % util.get_systemtime()
    req = request.Request(
        url=url,
        data=bytearray(data, 'utf-8'),
        headers=para.headers
    )
    return req


@install_handler
def handle_reply_comment_request(mid, cid, ouid, nick, content):
    para.reply_comment_form["mid"] = mid
    para.reply_comment_form["cid"] = cid
    para.reply_comment_form["uid"] = para.uid
    para.reply_comment_form["status_owner_user"] = para.uid
    para.reply_comment_form["ouid"] = ouid
    para.reply_comment_form["content"] = "回复@%s:%s" % (nick, content)
    data = urlencode(para.reply_comment_form)
    url = para.post_comment_url % util.get_systemtime()
    req = request.Request(
        url=url,
        data=bytearray(data, 'utf-8'),
        headers=para.headers
    )
    return req


@install_handler
def handle_like_request(mid):
    para.add_like_form['mid'] = mid
    data = urlencode(para.add_like_form)
    url = para.add_like_url
    req = request.Request(
        url=url,
        data=bytearray(data, 'utf-8'),
        headers=para.headers
    )
    return req


@install_handler
def handle_follow_request(uid, nick):
    para.follow_form["uid"] = uid
    para.follow_form["oid"] = uid
    para.follow_form["fnick"] = nick
    data = urlencode(para.follow_form)
    url = para.follow_url % util.get_systemtime()
    req = request.Request(
        url=url,
        data=bytearray(data, 'utf-8'),
        headers=para.headers
    )
    return req


@install_handler
def handle_get_weibos_request(uid, domain, page, stage=1, keyword=None):
    if keyword:
        keyword = keyword.encode("utf-8")
        keyword = request.quote(keyword)
        keyword = request.quote(keyword)
    if stage == 1:
        url = para.get_weibo_url % (uid, page)
        if keyword is not None:
            url = url + "&is_search=1&key_word=%s" % keyword
        return url
    elif stage == 2:
        parameters = para.query_form
        if keyword:
            parameters['is_all'] = '1'
            parameters['is_search'] = '1'
            parameters['key_word'] = keyword
        parameters['domain'] = domain
        parameters['domain_op'] = domain
        parameters['pre_page'] = str(page)
        parameters['page'] = str(page)
        parameters['pagebar'] = '0'
        parameters['id'] = domain + uid
        parameters['__rnd'] = util.get_systemtime()
    else:
        parameters = para.query_form
        parameters['pagebar'] = '1'

    url = construct_url(para.query_url, parameters)
    return url


def construct_url(url, parameters):
    url += '?'
    for key in parameters.keys():
        url += (key + '=' + str(parameters[key]) + '&')
    url = url[:-1]
    return url


@install_handler
def handle_namecard_request(uid):
    url = para.newcard_url % (uid, util.get_systemtime())
    return url


@install_handler
def handle_get_relation_request(uid, page, _type="followee"):
    if _type == "followee":
        url = para.get_followee_url % (uid, page)
    else:
        url = para.get_follower_url % (uid, page)

    return url


@install_handler
def handle_get_user_info_request(uid, domain):
    url = para.get_user_info_url % (domain, uid)
    return url


@install_handler
def handle_homepage_request(uid, stage=1, keyword=None):
    if keyword:
        keyword = keyword.encode("utf-8")
        keyword = request.quote(keyword)
        keyword = request.quote(keyword)
    if stage == 1:
        url = para.home_url % uid
        if keyword is not None:
            url = url + "&is_search=1&key_word=%s" % keyword
        return url
    elif stage == 2:
        parameters = para.query_home_form
        if keyword:
            parameters['is_all'] = '1'
            parameters['is_search'] = '1'
            parameters['key_word'] = keyword
        parameters['pre_page'] = '1'
        parameters['page'] = '1'
        parameters['pagebar'] = '0'
        parameters['__rnd'] = util.get_systemtime()
    else:
        parameters = para.query_form
        parameters['pagebar'] = '1'
    url = construct_url(para.query_home_url, parameters)
    return url


@install_handler
def handle_search_user_request(word=None, page=1, tag=None, auth=None,
                               region=None, gender=None, age=None):
    url = para.search_user_url
    if word:
        if isinstance(word, unicode):
            word = word.encode("utf-8")
        word = request.quote(word)
        word = request.quote(word)
        url += word

    appendix = ""
    if tag:
        if isinstance(tag, unicode):
            tag = tag.encode("utf-8")
        tag = request.quote(tag)
        tag = request.quote(tag)
        appendix += "&tag=%s" % tag
    if auth:
        appendix += "&auth=%s" % auth
    if region:
        appendix += "&region=%s" % region
    if gender:
        appendix += "&gender=%s" % gender
    if age:
        appendix += "&age=%s" % age
    if page > 1:
        appendix += "&page=%d" % page
    url += appendix
    return url


@install_handler
def handle_search_weibo_request(word, page=1, region=None,
                                start_date=None, end_date=None):
    word = word.encode("utf-8")
    word = request.quote(word)
    word = request.quote(word)
    url = para.search_weibo_url % word
    url = url + "?page=%d&typeall=1&suball=1" % page
    if region:
        url = url + ("&region=%s" % region)
    if start_date is not None or end_date is not None:
        append = "&timescope=custom:%s:%s" % (start_date, end_date)
        append = append.replace("None", "")
        url = url + append

    return url


@install_handler
def handle_get_inbox_comment_request():
    url = para.get_inbox_comment_url
    return url


@install_handler
def handle_get_inbox_count_request():
    return para.get_inbox_count_url
