# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-27
"""
from weiboapi.item import Item, Field


class Comment(Item):
    comment_id = Field()
    content = Field()
    date = Field()
    uid = Field()
    nick = Field()
    like_number = Field()
