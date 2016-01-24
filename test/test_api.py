"""
@Author: Rossi
2016-01-23
"""
from weiboapi.api.api import *


def test_get_prelogin_parameters():
    assert get_prelogin_parameters("xiaocailuoxi@sina.com") == True


def test_login():
    assert login("xiaocailuoxi@sina.com", "xiaocailuoxi") == True
    assert login("xiaocailuoxi@sina.com", "xiaocai") == False
