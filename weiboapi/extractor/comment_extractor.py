# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-27
"""
from bs4 import BeautifulSoup
import json
from lxml import etree
import traceback
from weiboapi.util import util
import re


# deal with py2 encoding problem
import sys
try:
    reload(sys)
    sys.setdefaultencoding("utf-8")
except:
    pass


class CommentExtractor():
    """
    """
    def __init__(self, comment_class):
        self.comment_class = comment_class


    def extract_comments(self, doc):
        html = etree.HTML(doc)
        divs = html.xpath(r'//div[@class="list_ul"]/div')
        comments = []
        for div in divs[:-1]:
            try:
                comment = self.comment_class()
                comment["content"] = self.extract_comment_content(div)
                comment["like_number"] = self.extract_like_number(div)
                comment["date"] = self.extract_date(div)
                comment["comment_id"] = self.extract_comment_id(div)
                comment["uid"], comment["nick"] = self.extract_uid_nick(div)
                comments.append(comment)
            except:
                traceback.print_exc();
                continue
        return comments

    def extract_comment_content(self, div):
        """
        Extracting the content of comment.
        """
        content_div = div.xpath(r'.//div[@class="WB_text"]')[0]
        root = BeautifulSoup(etree.tostring(content_div, encoding="utf-8"))
        node = root.find('div')
        text = ""
        #iterating the elements and appends their text.
        for child in node.children:
            if child.name == 'img':
                if child.has_attr('title'):
                    text += child['title']
                elif child.has_attr('alt'):
                    text += child['alt']
                   
            elif child.name == None:
                t = str(child)
                text += t.strip()
                
            elif child.name == 'a':
                if child.has_attr('render'):
                    text += " %s " %child.text
                else:
                    text += child.text
                    
            elif child.name == 'em':
                for c in child.children:
                    if c.name == 'img':
                        if child.has_attr('title'):
                            text += child['title']
                        elif child.has_attr('alt'):
                            text += child['alt']
                    elif c.name == None:
                        t = str(c)
                        text += t.strip()
                    elif c.name == 'a':
                        if child.has_attr('render'):
                            text += " %s " %c.text
                        else:
                            text += c.text   
        return text

    def extract_like_number(self, div):
        t = div.xpath(r'.//span[@node-type="like_status"]/em/text()')
        if len(t) != 0:
           return int(t[0])
        else:
            return 0

    def extract_date(self, div):
        texts = div.xpath(r'.//div[@class="WB_from S_txt2"]/text()')
        if len(texts) > 0:
            return texts[0].strip()

    def extract_comment_id(slef, div):
        return div.attrib.get('comment_id')  

    def extract_uid_nick(self, div): 
        img = div.xpath(r'.//img')[0]
        uid = img.attrib.get("usercard")[3:]
        nick = img.attrib.get("alt")
        return uid, nick
