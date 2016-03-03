# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-26
"""
from bs4 import BeautifulSoup
from lxml import etree
import traceback
from weiboapi.util import util
import re
from weiboapi.api.weibo import Weibo

# deal with py2 encoding problem
import sys
try:
    reload(sys)
    sys.setdefaultencoding("utf-8")
except:
    pass


ID_LENGTH = 10


class WeiboExtractor():
    def __init__(self, weibo_class):
        self.install_extractors(weibo_class)

    def install_extractors(self, weibo_class):
        """
        """
        self.extractors = []
        self.extractors.append(ContentExtractor())
        self.extractors.append(MidExtractor())
        self.extractors.append(NumberInfoExtractor())
        self.extractors.append(DateSouceExtractor())
        self.extractors.append(UrlExtractor())
        self.extractors.append(MediaInfoExtractor())

    def extract_weibos(self, doc, first=False, single=False):
        """
        Extracting weibos from the html document.
        """
        weibos = []
        try:
            if first:
                doc = self.extract_content_html(doc, single)

            html = etree.HTML(doc)
            divs = html.xpath(r'//div[@action-type="feed_list_item"]')

            for div in divs:
                weibo = Weibo()
                for extractor in self.extractors:
                    try:
                        extractor.extract(div, weibo)
                    except:
                        traceback.print_exc()
                        continue
                weibos.append(weibo)
        except:
            traceback.print_exc()
        return weibos

    def extract_content_html(self, html, single=False):
        """
        Extracting html code that contains weibo content.
        """
        scripts = util.extract_script(html)
        if not single:
            script = util.select_script(
                scripts, r'"domid":"Pl_Official_MyProfileFeed'
            )
        else:
            script = util.select_script(
                scripts, r'pl.content.weiboDetail.index'
            )
        text = script.text.strip()
        return util.extract_html_from_script(text)


class FieldExtractor():
    def extract(self, div, weibo):
        pass


class ContentExtractor(FieldExtractor):
    def extract(self, div, weibo):
        """
        Extracting weibo content from the given div elment.
        """
        content = div.xpath(r'.//div[@node-type="feed_list_content"]')[0]
        root = BeautifulSoup(etree.tostring(content, encoding="utf-8"), "lxml")
        node = root.find('div')
        text = ""
        img_text = ""
        at_text = ""
        # iterating the elements and appends their text.
        for child in node.children:
            if not hasattr(child, "name") or child.name is None:
                t = str(child)
                text += t.strip()

            elif child.name == 'img':
                if child.has_attr('title'):
                    text += str(child['title'])
                    img_text += str(child['title']) + " "

            elif child.name == 'a':
                if child.has_attr('render'):
                    text += " %s " % child.text
                    at_text += child.text + " "
                else:
                    text += child.text

            elif child.name == 'em':
                for c in child.children:
                    if not hasattr(c, "name") or c.name is None:
                        t = str(c)
                        text += t.strip()

                    elif c.name == 'img':
                        if c.has_attr('title'):
                            text += c['title'].strip()
                            img_text += str(c['title']) + " "

                    elif c.name == 'a':
                        if c.has_attr('render'):
                            text += " %s " % c.text
                            at_text += child.text + " "
                        else:
                            text += c.text

        weibo["content"] = text


class NumberInfoExtractor(FieldExtractor):
    def extract(self, div, weibo):
        """
        Extracting repost_number, like_number, comment_number
        """
        weibo_handle = div.xpath(r'.//div[@class="WB_handle"]')[0]
        spans = weibo_handle.xpath(
            r'.//span[@class="line S_line1"]'
        )

        if len(spans) == 4:
            spans = spans[1:]

        for i, span in enumerate(spans):
            if i == 2:
                text = span.xpath('.//em/text()')

                if len(text) == 0:
                    weibo['like_number'] = 0
                elif len(text) == 1:
                    weibo['like_number'] = int(text[0])
                continue
            else:
                text = span.xpath("./text()")[0]
            splits = text.split()
            if len(splits) == 2:
                if splits[0] == '转发':
                    weibo['repost_number'] = int(splits[1])
                elif splits[0] == '评论':
                    weibo['comment_number'] = int(splits[1])
            elif len(splits) == 1:
                if splits[0] == '转发':
                    weibo['repost_number'] = 0
                elif splits[0] == '评论':
                    weibo['comment_number'] = 0


class MidExtractor(FieldExtractor):
    def extract(self, div, weibo):
        weibo['mid'] = div.attrib.get('mid')
        omid = div.attrib.get('omid')
        tbinfo = div.attrib.get('tbinfo')
        index = tbinfo.find("ouid=")
        weibo['uid'] = tbinfo[index+5:index+15]
        if omid is not None:
            weibo['is_repost'] = True
            weibo['omid'] = omid
        else:
            weibo['is_repost'] = False


class DateSouceExtractor(FieldExtractor):
    def extract(self, div, weibo):
        """
        Extracting date and source
        """
        new_div = div.xpath(r'.//div[@class="WB_from S_txt2"]')
        if len(new_div) == 1:
            new_div = new_div[0]
        elif len(new_div) == 2:
            new_div = new_div[1]
        date = new_div.xpath(r'.//a[@node-type="feed_list_item_date"]')[0]
        weibo['date'] = util.timestamp_to_date(
            int(date.attrib.get('date')[:-3])
            )
        source = new_div.xpath(r'.//a/text()')[1]
        weibo['source'] = source


class UrlExtractor(FieldExtractor):
    def extract(self, div, weibo):
        """
        Extracting the url(s) of weibo
        """
        weibo_handle = div.xpath(r'.//div[@class="WB_handle"]')[0]
        action_datas = weibo_handle.xpath(
            r'.//a[@class="S_txt2"]/@action-data')

        if len(action_datas) == 3:
            action_data = action_datas[0]
            if weibo["is_repost"]:
                root_url = re.findall("rooturl=([a-zA-Z0-9/:.]*)", action_data)
                if len(root_url) == 1:
                    weibo["root_url"] = root_url[0]

        url = re.findall("&url=([a-zA-Z0-9/:.]*)", action_data)
        if len(url) == 1:
            weibo["url"] = url[0]


class MediaInfoExtractor(FieldExtractor):
    def extract(self, div, weibo):
        """
        Extracting media infomation such a pictures urls and links.
        """
        if weibo['is_repost']:
            return

        media_divs = div.xpath(r'.//div[@class="media_box"]')
        for media_div in media_divs:
            pic_div = media_div.xpath(r'.//div[@node-type="fl_pic_list"]')
            if len(pic_div) == 1:
                pic_div = pic_div[0]
                imgs = pic_div.xpath(r'.//li/img/@src')
                weibo['pictures'] = imgs
                continue

            imgs = media_div.xpath('.//img/@src')
            weibo['pictures'] = imgs

            links = media_div.xpath('.//a')
            if len(links) != 0:
                link_texts = ""
                ls = []
                for link in links:
                    if link.attrib.get('href') != None:
                        ls.append(link.attrib.get('href'))
                    else:
                        continue
                    text = link.xpath(".//text()")
                    if len(text) == 1:
                        link_texts += text[0].strip() + "||"

                weibo['links'] = ls
                weibo['link_text'] = link_texts
