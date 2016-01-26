"""
@Author: Rossi
2016-01-26
"""

from weiboapi.api.weibo import *
from weiboapi.extractor.weibo_extractor import WeiboExtractor



def test_weibo_extractor():
    extractor = WeiboExtractor(Weibo)
    