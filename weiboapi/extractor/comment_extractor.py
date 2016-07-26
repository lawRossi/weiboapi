# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-27
"""
from bs4 import BeautifulSoup
from lxml import etree
import traceback
from weiboapi.util import util
from weiboapi.api.comment import Comment

# deal with py2 encoding problem
import sys
try:
    reload(sys)
    sys.setdefaultencoding("utf-8")
except:
    pass


class CommentExtractor():

    def __init__(self, comment_class):
        self.comment_class = comment_class

    def extract_comments(self, doc):
        html = etree.HTML(doc)
        divs = html.xpath(r'//div[@class="list_ul"]/div')
        for div in divs[:-1]:
            try:
                comment = self.comment_class()
                comment["content"] = self.extract_comment_content(div)
                comment["like_number"] = self.extract_like_number(div)
                comment["date"] = self.extract_date(div)
                comment["comment_id"] = self.extract_comment_id(div)
                comment["uid"], comment["nick"] = self.extract_uid_nick(div)
                yield comment
            except:
                traceback.print_exc()
                continue

    def extract_comment_content(self, div):
        """
        Extracting the content of comment.
        """
        content_div = div.xpath(r'.//div[@class="WB_text"]')[0]
        root = BeautifulSoup(
            etree.tostring(content_div, encoding="utf-8"), "lxml"
            )
        node = root.find('div')
        text = ""
        # iterating the elements and appends their text.
        for child in node.children:
            if not hasattr(child, "name") or child.name is None:
                t = str(child)
                text += t.strip()

            if child.name == 'img':
                if child.has_attr('title'):
                    text += child['title']
                elif child.has_attr('alt'):
                    text += child['alt']

            elif child.name == 'a':
                if child.has_attr('render'):
                    text += " %s " % child.text
                else:
                    text += child.text

            elif child.name == 'em':
                for c in child.children:
                    if not hasattr(c, "name") or c.name is None:
                        t = str(c)
                        text += t.strip()

                    elif c.name == 'img':
                        if child.has_attr('title'):
                            text += child['title']
                        elif child.has_attr('alt'):
                            text += child['alt']

                    elif c.name == 'a':
                        if child.has_attr('render'):
                            text += " %s " % c.text
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


def extract_inbox_comment(data):
    comments = []
    try:
        scripts = util.extract_script(data)
        script = util.select_script(
                    scripts, r'"domid":"v6_pl_content_commentlist"'
        )
        print len(scripts)
        text = script.text.strip()
        doc = util.extract_html_from_script(text)
        html = etree.HTML(doc)
        divs = html.xpath('//div[@node-type="feed_commentList_comment"]')
    except:
        return comments

    for div in divs:
        try:
            weibo_url, comment = extract_individual_comment(div)
            comments.append((weibo_url, comment))
        except:
            pass
    return comments


def extract_individual_comment(div):
    try:
        comment = Comment()
        comment["comment_id"] = div.attrib["comment_id"]
        a = div.xpath('.//div[@class="WB_info S_txt2"]/a')[0]
        comment["nick"] = a.text.strip()
        usercard = a.attrib["usercard"]
        comment["uid"] = usercard[len("id="):]
        comment["content"] = div.xpath('.//div[@class="WB_text"]/text()')[0]
        a = div.xpath('//a[@class="S_func1"]')[0]
        weibo_url = "http://weibo.com%s" % a.attrib["href"]
        return weibo_url, comment
    except:
        traceback.print_exc()
