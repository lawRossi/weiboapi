"""
@Author: Rossi
2016-01-25
"""
from weiboapi.util import util
from . import para
try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode

try:
    import urllib2 as request
except:
    import urllib.request as request

try:
    from cookielib import LWPCookieJar
except:
    from http.cookiejar import LWPCookieJar
import traceback


cj = LWPCookieJar()
cookie_support = request.HTTPCookieProcessor(cj)
opener = request.build_opener(cookie_support, request.HTTPHandler)
request.install_opener(opener)


def open_decode(req):
    try:
        data = request.urlopen(req).read()
        return util.decode(data)
    except:
        traceback.print_exc()
        return None


def handle_prelogin_request(username):
    """
    """
    username = util.quote_base64_encode(username)
    st = util.get_systemtime()
    url = para.prelogin_url % (username, st)
    return open_decode(url)


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


def handle_url_request(url):
    req = request.Request(
        url=url,
        headers=para.headers
    )
    return open_decode(req)
    


def handle_post_request(content):
    para.post_form['text'] = content
    data = urlencode(para.post_form)
    url = para.post_url % util.get_systemtime()
    req = request.Request(
        url=url,
        data=bytearray(data, 'utf-8'),
        headers=para.headers
    )
    return open_decode(req)


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
    return open_decode(req)


def handle_get_weibos_request(uid, domain, page, stage=1, end_id=None):
    try:
        if stage == 1:
            url = 'http://weibo.com/p/' + domain + uid + '/home?page=%d' %page
            return open_decode(url)
        elif stage == 2:
            parameters = para.query_form
            parameters['domain'] = domain
            parameters['domain_op'] = domain
            parameters['pre_page'] = str(page)
            parameters['page'] = str(page)
            parameters['end_id'] = end_id
            parameters['pagebar'] = '0'
            parameters['id'] = domain + uid
            parameters['__rnd'] = util.get_systemtime()
        else:
            parameters = para.query_form
            parameters['pagebar'] = '1'

        url = construct_url(parameters)
        return open_decode(url)
        
    except:
        traceback.print_exc();
        return None


def construct_url(parameters):
    url = para.query_url
    url += '?'
    for key in parameters.keys():
        url += (key + '=' + str(parameters[key]) + '&')
    url = url[:-1]
    return url