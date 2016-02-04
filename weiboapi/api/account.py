"""
@Author: Rossi
2016-01-28
"""
from .item import Item, Field


class Account(Item):
    """
    Weibo account class.
    """
    uid = Field()
    nick = Field()
    domain = Field()
    home_url = Field()
    gender = Field()
    area = Field()
    discription = Field()
    tags = Field()
    follower_number = Field()
    followee_number = Field()
    post_number = Field()
    verify = Field()