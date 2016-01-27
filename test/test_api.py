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
    assert login("xiaocailuoxi@sina.com", "xiaocailuoxi") == True



# def test_post():
#     assert post("[哈哈]") == True


# def test_comment():
#    assert comment("3935531970578484", "hehe") == True


# def test_get_weibos():
#     weibos = get_weibos("2237529652")
#     assert len(weibos) == 44


# def test_get_weibo():
#     weibo = get_weibo("http://weibo.com/2237529652/C91R89kUV")
#     print(weibo)


def test_get_comments():
    comments = get_comments("3935531970578484", 1)
    print(comments)
