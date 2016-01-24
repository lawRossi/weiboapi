"""
@Author: Rossi
2016-01-23
"""
from weiboapi.http.request import *
from weiboapi.http import para
import re
import json


def get_prelogin_parameters(username):
    """
    Getting parameters that are needed to login.
    username: the uername to login.
    """
    data = handle_prelogin_request(username)
    if not data:
        return False

    p = re.compile('\((.*)\)')
    json_data = p.search(data).group(1)
    data = json.loads(json_data)
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
    data = data[260:]
    data = str(data, 'utf-8')
    p = re.compile('\((.*?)\)')
    json_data = p.search(data).group(1)
    json_data = json.loads(json_data)
    retcode = json_data['retcode']
    
    if retcode == 0:
        try:
            start_pos = data.find('location.replace')
            end_pos = data.find('\');})')
            s = data[start_pos:end_pos]
            start_pos = s.find('http:')
            url = s[start_pos:]
            url = urllib.request.unquote(url)
            req = urllib.request.Request(
                url = url,
                headers = para.headers,
            )
            data = urllib.request.urlopen(req).read()
            data = str(data, 'utf-8')
            p = re.compile('\((.*)\)')
            json_data = p.search(data).group(1)
            json_data = json.loads(json_data)
            if(json_data['result']):
                json_data = json_data['userinfo']
                uniqueid = json_data['uniqueid']
                home_url = 'http://weibo.com/u/' + uniqueid + "/home"
                data = urllib.request.urlopen(home_url).read()
            else:
                return False
        except:
            return False