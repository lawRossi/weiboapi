"""
@Author: Rossi
2016-01-23
"""
from weiboapi.api.api import *


def test_login():
    assert login("xiaocailuoxi@sina.com", "xiaocailuoxi") == True
    assert login("xiaocailuoxi@sina.com", "xiaocai") == False
