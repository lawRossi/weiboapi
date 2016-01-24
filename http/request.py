"""
@Author: Rossi
2016-01-24
"""
from weiboapi.util import util
from . import para
import requests
from urllib import urlencode
session = requests.Session()


def handle_prelogin_request(username):
    """
    """
    username = util.quote_base64_encode(username)
    st = util.get_systemtime()
    url = para.prelogin_url % (username, st)
    r = session.get(url)
    if util.check_status(r):
        return r.text
    else:
        return None


def handle_session_request():
    r = requests.get(para.session_url)
    return util.check_status(r)


def handle_login_request(username, password):
    psw = util.encrypt_password(
        password, para.servertime, para.nonce,
        para.publickey, para.rsakv
    )
    para.request_body['sp'] = str(psw, 'utf-8')
    para.request_body['su'] = util.base64_encode(username)
    para.request_body['rsakv'] = para.rsakv
    para.request_body['nonce'] = para.nonce
    para.request_body['servertime'] = str(para.servertime)
    postdata = urlencode(para.request_body)
    para.headers['Referer'] = 'http://weibo.com'
    r = session.post(para.login_url, postdata, headers=para.headers)
    if not util.check_status(r):
        return False 
    else:
        return r.text

    