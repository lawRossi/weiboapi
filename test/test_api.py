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
    #assert login("luoweiang@sina.cn", "luoweiang920322") == True



# def test_post():
#     assert post("[哈哈]") == True


# def test_comment():
#    assert comment("3935531970578484", "hehe") == True


def test_get_weibos():
    weibos = get_weibos("2237529652")
    print(weibos[0])
    assert len(weibos) > 0 