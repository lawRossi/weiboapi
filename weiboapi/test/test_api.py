# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-23
"""
from weiboapi.api.api import *
import time

# def test_get_prelogin_parameters():
#     assert get_prelogin_parameters("xiaocailuoxi@sina.com") == True


def test_login():
    # assert login("xlab1up@gmail.com", "chinese833") is True
    assert login("xiaocailuoxi@sina.com", "xiaocailuoxi03") is True
    assert has_login() is True
    # assert login("13714958221", "duiwen314")

# def test_post():
#     assert post("[哈哈]") == True


# def test_comment():
#    assert comment("3986348463031592", "[哈哈]") is True

# def test_repost():
#     assert repost("3987033825353370", "赞同", True) is True


# def test_follow():
#     assert follow("5984418785", "汪汪信用") is True


# def test_send_message():
#    assert send_message("2363405233", "hai")


# def test_get_domain():
#     domain = get_domain("2237529652")
#     print(domain)


# def test_get_weibos():
    # weibos = get_weibos("1494759712", "100505", 1, "百度")
    # for weibo in weibos:
    #     print(weibo["content"])
    # weibos = get_weibos("2375086267")
    # print len(weibos)
    # for weibo in weibos:
    #     print(weibo["mid"])
    # # weibos = get_weibos("2864766784")
    # mids1 = [weibo["mid"] for weibo in weibos]
    # fi = codecs.open("temp.txt", encoding="utf-8")
    # mids2 = [line.strip() for line in fi]
    # fi.close()
    # assert mids1 == mids2

    # weibos = get_weibos("1750070171", "100206")
    # print(weibos)


# def test_get_weibo():
#     weibo = get_weibo("http://weibo.com/1001509221/ACuc3ttTF")
#     print(weibo)
    # weibo = get_weibo("http://weibo.com/2828172374/D8ncDbB0Q")
    # print(weibo)
#     weibo = get_weibo("http://weibo.com/2237529652/C91R89kUV")
#     print(weibo)

# def test_get_comments():
#     comments = get_comments("3938833714291022", 1)
#     for comment in comments:
#         print(comment)


# def test_get_account():
#     account = get_account('1951298162')
#     print(account)
#     account = get_account("3136675261")
#     print(account)
#     account = get_account("5921927072")
#     print(account)


# def test_get_relation():
#     followees = get_relation("2683295213", 2)
#     print(list(followees))
#     print("######################")
#     followers = get_relation("2683295213", _type="follower")
#     print(list(followers))


# def test_get_user_info():
#     userinfo = get_user_info("5664214548")
#     for k, v in userinfo.items():
#         print k, ":", v


# def test_search_user():
#     users = search_user(tag="娱乐", region="custom:44:1000", auth="ord", age=None)
#     print(len(users))
#     for user in users[:3]:
#         print(user)


# def test_search_weibo():
#     weibos = search_weibo(u"旅游", region="custom:44:1000",
#                           start_date="2016-6-1")
#     print(len(weibos))
#     for weibo in weibos[:5]:
#         print(weibo)


# def test_search_count():
#     print search_count("旅游")


def test_get_hot_weibos():
    all_mids = []
    for i in range(10):
        weibos = get_hot_weibos("明星", i)
        mids = [weibo["mid"] for weibo in weibos]
        print len(mids)
        all_mids.extend(mids)
        time.sleep(1.5)
    print len(set(all_mids))
