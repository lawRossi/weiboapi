# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-23
"""
from weiboapi.api.api import *
# def test_get_prelogin_parameters():
#     assert get_prelogin_parameters("xiaocailuoxi@sina.com") == True


def test_login():
    #assert login("xiaocailuoxi@sina.com", "xiaocai") == False
    assert login("xiaocailuoxi@sina.com", "xiaocailuoxi03") == True



# def test_post():
#     assert post("[哈哈]") == True


def test_comment():
   assert comment("3938833714291022", "hehe") == True


# def test_get_domain():
#     domain = get_domain("2237529652")
#     print(domain)


def test_get_weibos():
    weibos = get_weibos("2237529652", "100505", page=2)

    #weibos = get_weibos("2864766784")
    print(len(weibos))
    print(weibos[0])
    # weibos = get_weibos("1750070171", "100206")
    # print(len(weibos))

    
# def test_get_weibo():
#     weibo = get_weibo("http://weibo.com/2237529652/C91R89kUV")
#     print(weibo)


# def test_get_comments():
#     comments = get_comments("3938833714291022", 1)
#     print(comments)


# def test_get_account():
#     account = get_account("2237529652")
#     print(account)


# def test_get_relation():
#     followees = get_relation("2864766784", "100505")
#     print(followees)
#     followers = get_relation("2864766784", "100505", _type="follower")
#     print(followers)


# def test_get_user_info():
#     userinfo = get_user_info("3206249732")
#     print(userinfo)


# def test_is_verified():
#     assert is_verified("1825436514") == False
#     assert is_verified("1750070171") == True