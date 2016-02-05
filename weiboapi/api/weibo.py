# -*- coding:utf-8 -*-
"""
:Author: Rossi
:Date: 2016-01-26
"""

from .item import Item, Field


class Weibo(Item):
    """
    Weibo class. Used for retriving weibo posts.
    """

    content = Field()
    uid = Field()
    mid = Field()
    omid = Field()
    like_number = Field(0)
    comment_number = Field(0)
    repost_number = Field(0)
    pictures = Field()
    is_repost = Field(False)
    date = Field()
    source = Field()
    url = Field()
    root_url = Field()
    links = Field()
    link_text = Field()
