# -*- coding:utf-8 -*-
"""
:Author: Rossi
:Date: 2016-01-27
"""
from .item import Item, Field


class Comment(Item):
    """
    Weibo comment class. Used for retriving comments of a Weibo post.
    """
    comment_id = Field()
    content = Field()
    date = Field()
    uid = Field()
    nick = Field()
    like_number = Field()
