"""
@Author: Rossi
2016-01-23
"""
from weiboapi.api.api import *


def test_get_prelogin_parameters():
    assert get_prelogin_parameters("xiaocailuoxi@sina.com") == True


def test_login():
    #assert login("xiaocailuoxi@sina.com", "xiaocai") == False
    #assert login("xiaocailuoxi@sina.com", "xiaocailuoxi") == True
    assert login("luoweiang@sina.cn", "luoweiang920322") == True


def test_post():
    assert post("a post by self-created api.(testing py3)") == True