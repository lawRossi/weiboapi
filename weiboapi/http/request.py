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
def handle_get_weibos_request(uid, domain, page, stage=1):
    if stage == 1:
        url = 'http://weibo.com/p/' + domain + uid \
            + ('/home?is_all=1&page=%d' % page)
        return url
    elif stage == 2:
        parameters = para.query_form
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

    url = construct_url(parameters)
    return url


def construct_url(parameters):
    url = para.query_url
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
def handle_homepage_request(uid):
    url = para.home_url % uid
    return url
