# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-23
"""
from weiboapi.api.api import *
import codecs


# def test_get_prelogin_parameters():
#     assert get_prelogin_parameters("xiaocailuoxi@sina.com") == True


def test_login():
    # assert login("xiaocailuoxi@sina.com", "xiaocai") == False
    assert login("xiaocailuoxi@sina.com", "xiaocailuoxi03") == True

# def test_post():
#     assert post("[哈哈]") == True


# def test_comment():
#    assert comment("3938833714291022", "评论一下") == True


# def test_get_domain():
#     domain = get_domain("2237529652")
#     print(domain)


# def test_get_weibos():
    # weibos = get_weibos("2237529652", "100505", 2)
    # print(weibos)
    # weibos = get_weibos("2828172374", "100505")
    # print(weibos)
    # # weibos = get_weibos("2864766784")
    # mids1 = [weibo["mid"] for weibo in weibos]
    # fi = codecs.open("temp.txt", encoding="utf-8")
    # mids2 = [line.strip() for line in fi]
    # fi.close()
    # assert mids1 == mids2

    # weibos = get_weibos("1750070171", "100206")
    # print(weibos)


# def test_get_weibo():
#     weibo = get_weibo("http://weibo.com/2828172374/DiC3JCtzo")
#     print(weibo)
#     # weibo = get_weibo("http://weibo.com/2828172374/D8ncDbB0Q")
#     # print(weibo)
#     weibo = get_weibo("http://weibo.com/2237529652/C91R89kUV")
#     print(weibo)

# def test_get_comments():
#     comments = get_comments("3938833714291022", 1)
#     for comment in comments:
#         print(comment)


# def test_get_account():
#     account = get_account("2237529652")
#     print(account)


# def test_get_relation():
#     followees = get_relation("2683295213", 2)
#     print(list(followees))
#     print("######################")
#     followers = get_relation("2683295213", _type="follower")
#     print(list(followers))


# def test_get_user_info():
#     userinfo = get_user_info("3206249732")
#     print(userinfo)


# def test_is_verified():
#     assert is_verified("1825436514") == False
#     assert is_verified("1750070171") == True


# def test_search_user():
#     users = search_user("足球")
#     print(len(users))
#     for user in users:
#         print(user)


def test_search_weibo():
    weibos = search_weibo("足球")
    print(len(weibos))
    for weibo in weibos[:3]:
        account = get_account(weibo["uid"])
        print(account)
