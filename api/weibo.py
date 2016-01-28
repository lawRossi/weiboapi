# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-26
"""

from .item import Item, Field


class Weibo(Item):
    content = Field()
    uid = Field()
    mid = Field()
    omid = Field()
    like_number = Field()
    comment_number = Field()
    repost_number = Field()
    pictures = Field()
    is_repost = Field()
    date = Field()
    source = Field()
    url = Field()
    root_url = Field()
    links = Field()
    link_text = Field()
