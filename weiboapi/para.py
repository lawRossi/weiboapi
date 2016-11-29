# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-23

This module contains some global varibles.
"""


prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo' \
    + '&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod' \
    + '&client=ssologin.js(v1.4.11)&_=%s'

login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.4.11)'

session_url = 'http://beacon.sina.com.cn/e.gif?UATrack||300805596634.7456.1392949880014' \
    + '||7143980532418.937.1396334858970||||tblog_weibologin3||click_sign||' \
    + 'http%3A//www.hao123.com/||javascript%3Avoid%280%29||||WEIBO-V5:&gUid_1396343431857'

post_url = 'http://weibo.com/aj/mblog/add?ajwvr=6&__rnd=%s'

repost_url = 'http://weibo.com/aj/v6/mblog/forward?ajwvr=6&domain=%s&__rnd=%s'

send_message_url = "http://weibo.com/aj/message/add?ajwvr=6&__rnd=%s"

post_comment_url = 'http://weibo.com/aj/v6/comment/add?ajwvr=6&__rnd=%s'

get_weibo_url = 'http://weibo.com/u/%s/home?wvr=6&page=%d&is_all=1'

query_url = 'http://weibo.com/p/aj/v6/mblog/mbloglist'  # for quering weibo content

query_home_url = 'http://weibo.com/aj/mblog/fsearch'

newcard_url = 'http://weibo.com/aj/v6/user/newcard?ajwvr=6&id=%s' \
    + '&type=1&call_back=STK_%s'

comment_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id=%s&max_id=''&page=%d&__rnd=%s'

get_followee_url = 'http://weibo.com/%s/follow?rightmod=1&wvr=6&page=%d'

get_follower_url = 'http://weibo.com/%s/fans?rightmod=1&wvr=6&page=%d'

get_user_info_url = 'http://weibo.com/p/%s%s/info'

search_user_url = "http://s.weibo.com/user/"

search_weibo_url = "http://s.weibo.com/weibo/%s"

search_personal_weibo_url = ""

home_url = 'http://weibo.com/u/%s/home'

big_picture_url = 'http://ww3.sinaimg.cn/bmiddle/%s'

follow_url = "http://weibo.com/aj/f/followed?ajwvr=6&__rnd=%s"

add_like_url = "http://weibo.com/aj/v6/like/add?ajwvr=6"

get_inbox_comment_url = "http://weibo.com/comment/inbox?topnav=1&wvr=6&f=1"

get_inbox_count_url = ("http://rm.api.weibo.com/2/remind/push_count.json?"
                       "with_common_cmt=1&msgbox=true&source=351354573")

get_hot_weibo_url = "http://weibo.com/feed/hot?leftnav=1&page_id="

get_more_hot_weibo_url = "http://weibo.com/aj/hot/list"

servertime = None

uid = ''  # the id of the "login account".

already_login = False

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
}  # used by login requests.

headers = {
    'User-Agent': ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                   "(KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"),
    'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9'
               ',image/webp,*/*;q=0.8'),
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Referer': 'http://weibo.com'
}


ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DICT = {}


for i in range(len(ALPHABET)):
    DICT[ALPHABET[i]] = i


query_form = {
    'domain': '',
    'is_all': '1',
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
}  # used for requesting Weibo posts.


query_hot_form = {
    "ajwvr": "6",
    "pre_page": 1,
    "page": 1,
    "leftnav": "1",
    "page_id": "",
    "pagebar": 1,
    "tab": "home",
    "min_id": "",
    "current_page": 2,
    "__rnd": ""
}


query_home_form = {
    'ajwvr': '6',
    'pre_page': '1',
    'page': '1',
    'wvr': '5',
    'pagebar': '',
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
}  # used for posting a Weibo

repost_form = {
    "pic_src": "",
    "pic_id": "",
    "appkey": "",
    "mid": "",
    "style_type": 1,
    "mark": "",
    "reason": "",
    "location": "v6_content_home",
    "pdetail": "",
    "module": "",
    "page_module_id": "",
    "refer_sort": "",
    # "is_comment_base": 1,
    "rank": 0,
    "rankid": "",
    "group_source": "group_all",
    "rid": "",
    "_t": 0
}


comment_form = {
    "act": "post",
    "mid": "",
    "uid": "",
    "rid": "",
    "forward": "0",
    "isroot": "0",
    "content": "",
    "location": "v6_content_home",
    "module": "scommlist",
    "group_source": "group_all",
    "pdetail": "",
    "_t": 0
}  # used for posting a coment


reply_comment_form = {
    'act': 'reply',
    'mid': '4000905839424545',
    'cid': '',
    'uid': '',
    'forward': '0',
    'isroot': '0',
    'content': '',
    'ouid': '',
    'status_owner_user': '',
    '_t': '0',
    'location': 'v6_comment_inbox'
}

message_form = {
    "location": "msgdialog",
    "module": "msgissue",
    "style_id": "1",
    "text": "",
    "uid": "",
    "tovfids": "",
    "fids": "",
    "el": "[object HTMLDivElement]",
    "_t": "0"
}

follow_form = {
    "uid": "",
    "objectid": "",
    "refer_flag": "1005050001_",
    "location": "page_100505_home",
    "extra": "",
    "refer_sort": "",
    "f": "1",
    "oid": "",
    "wforce": "1",
    "nogroup": "false",
    "fnick": "",
    "_t": "0"
}

add_like_form = {
    "location": "v6_content_home",
    "group_source": "group_all",
    "rid": "",
    "version": "mini",
    "qid": "heart",
    "mid": "",
    "like_src": "1"
}

cat_page_id_dict = {
    "视频": "102803_ctg1_1199_-_ctg1_1199",
    "社会": "102803_ctg1_4188_-_ctg1_4188",
    "国际": "102803_ctg1_6288_-_ctg1_6288",
    "科技": "102803_ctg1_2088_-_ctg1_2088",
    "科普": "102803_ctg1_5988_-_ctg1_5988",
    "数码": "102803_ctg1_5088_-_ctg1_5088",
    "财经": "102803_ctg1_6388_-_ctg1_6388",
    "股市": "102803_ctg1_1288_-_ctg1_1288",
    "明星": "102803_ctg1_4288_-_ctg1_4288",
    "综艺": "102803_ctg1_4688_-_ctg1_4688",
    "电视剧": "102803_ctg1_2488_-_ctg1_2488",
    "电影": "102803_ctg1_3288_-_ctg1_3288",
    "音乐": "102803_ctg1_5288_-_ctg1_5288",
    "汽车": "102803_ctg1_5188_-_ctg1_5188",
    "体育": "102803_ctg1_1388_-_ctg1_1388",
    "运动健身": "102803_ctg1_4788_-_ctg1_4788",
    "健康": "102803_ctg1_2188_-_ctg1_2188",
    "瘦身": "102803_ctg1_6488_-_ctg1_6488",
    "养生": "102803_ctg1_6588_-_ctg1_6588",
    "军事": "102803_ctg1_6688_-_ctg1_6688",
    "历史": "102803_ctg1_6788_-_ctg1_6788",
    "美女模特": "102803_ctg1_2288_-_ctg1_2288",
    "美图": "102803_ctg1_4988_-_ctg1_4988",
    "情感": "102803_ctg1_1988_-_ctg1_1988",
    "搞笑": "102803_ctg1_4388_-_ctg1_4388",
    "辟谣": "102803_ctg1_6988_-_ctg1_6988",
    "正能量": "102803_ctg1_7088_-_ctg1_7088",
    "政务": "102803_ctg1_5788_-_ctg1_5788",
    "游戏": "102803_ctg1_4888_-_ctg1_4888",
    "旅游": "102803_ctg1_2588_-_ctg1_2588",
    "育儿": "102803_ctg1_3188_-_ctg1_3188",
    "校园": "102803_ctg1_1488_-_ctg1_1488",
    "美食": "102803_ctg1_2688_-_ctg1_2688",
    "房产": "102803_ctg1_5588_-_ctg1_5588",
    "家居": "102803_ctg1_5888_-_ctg1_5888",
    "星座": "102803_ctg1_1688_-_ctg1_1688",
    "读书": "102803_ctg1_4588_-_ctg1_4588",
    "三农": "102803_ctg1_7188_-_ctg1_7188",
    "设计": "102803_ctg1_5388_-_ctg1_5388",
    "艺术": "102803_ctg1_5488_-_ctg1_5488",
    "时尚": "102803_ctg1_4488_-_ctg1_4488",
    "美妆": "102803_ctg1_1588_-_ctg1_1588",
    "动漫": "102803_ctg1_2388_-_ctg1_2388",
    "宗教": "102803_ctg1_5688_-_ctg1_5688",
    "萌宠": "102803_ctg1_2788_-_ctg1_2788",
    "法律": "102803_ctg1_7388_-_ctg1_7388"
}
