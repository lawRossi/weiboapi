# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-28
"""
from weiboapi.api.account import Account
import traceback
from lxml import etree


class AccountExtractor():

    def extract_account(self, doc):
        try:
            account = Account()
            html = etree.HTML(doc)
            div = html.xpath(r'.//div[@class="name"]')[0]
            href = div.xpath('./a/@href')[0]
            href = href[:href.index('?')]
            account["home_url"] = href
            account["nick"] = div.xpath('./a/text()')[0].strip()
            account["gender"] = div.xpath('.//em/@title')[0]
            keys = ["followee_number", "follower_number", "post_number"]
            spans = html.xpath(r'//div[@class="c_count"]/span')
            for i, span in enumerate(spans):
                v = span.xpath('.//em/text()')[0].strip()
                account[keys[i]] = v
            text = html.xpath('.//div[@class="intro W_autocut"]/span/text()')
            if text:
                account["description"] = text[0].strip()
            text = html.xpath('.//li[@class="info_li"]/a/text()')
            if text:
                account["area"] = text[0].strip()
            return account
        except:
            traceback.print_exc()
            return None
