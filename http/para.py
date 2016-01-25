# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-23
"""

prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo' \
    + '&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod' \
    + '&client=ssologin.js(v1.4.11)&_=%s'

login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.4.11)'

session_url = 'http://beacon.sina.com.cn/e.gif?UATrack||300805596634.7456.1392949880014' \
    + '||7143980532418.937.1396334858970||||tblog_weibologin3||click_sign||' \
    + 'http%3A//www.hao123.com/||javascript%3Avoid%280%29||||WEIBO-V5:&gUid_1396343431857'

post_url = 'http://weibo.com/aj/mblog/add?ajwvr=6&__rnd=%s'

query_url = 'http://weibo.com/p/aj/v6/mblog/mbloglist'  # for quering weibo content

newcard_url = 'http://weibo.com/aj/v6/user/newcard?ajwvr=6&id=%s' \
    + '&type=1&call_back=STK_%s'

comment_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id=%s&max_id=%s&page=%d&__rnd=%s'

big_picture_url = 'http://ww3.sinaimg.cn/bmiddle/%s'

servertime = None

request_body = {
    'entry': 'weibo',
    'gateway': '1',
    'from': '',
    'savestate': '7',
    'useticket': '1',
    'pagerefer': 'http: //login.sina.com.cn/sso/logout.php?entry=miniblog&r=' \
    + 'http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
    'vsnf': '1',
    'su': '',
    'service': 'miniblog',
    'servertime': '',
    'nonce': '',
    'pwencode': 'rsa2',
    'rsakv': '',
    'sp': '',
    'encoding': 'UTF-8',
    'prelt': '273',
    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=' \
    + 'parent.sinaSSOController.feedBackUrlCallBack',
    'returntype': 'META'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36' \
    + '(KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36',
    'Connection': 'keep-alive'
}


ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DICT = {}


for i in range(len(ALPHABET)):
    DICT[ALPHABET[i]] = i

query_parameters = {
    'domain': '',
    'ajwvr': '6',
    'wvr': '6',
    'pre_page': '',
    'page': '',
    'max_id': '',
    'end_id': '',
    'pagebar': '',
    'max_msign': '',
    'filtered_min_id': '',
    'pl_name': '',
    'id': '',
    'script_uri': '',
    'feed_type': '0',
    'is_search': '0',
    'from': '',
    'mod': 'data',
    'domain_op': '',
    '__rnd': ''
}


post_form = {
    "location": "v6_content_home",
    "appkey": "",
    "style_type": "1",
    "pic_id": "",
    "text": "",
    "pdetail": "",
    "rank": 0,
    "rankid": "",
    "module": "stissue",
    "pub_source": "main_",
    "pub_type": "dialog",
    "_t": 0
}