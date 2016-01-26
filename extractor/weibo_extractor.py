"""
@Author: Rossi
2016-01-26
"""
from bs4 import BeautifulSoup
import json
from lxml import etree
import traceback


# deal with py2 encoding problem
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def extract_script(html):
    """
    Extracting scripts from html.
    """
    soup = BeautifulSoup(html, "lxml")
    scripts = soup.find_all('script')
    return scripts


class WeiboExtractor():
    def __init__(self, weibo_class):
        self.weibo_class = weibo_class
        self.install_extractors(weibo_class)

    def install_extractors(self, weibo_class):
        """
        """
        self.extractors = []
        self.extractors.append(ContentExtractor())

    def extract_weibos(self, doc, first=False):
        """
        Extracting weibos from the html document.
        """
        if first:
            doc = self.extract_content_html(doc)

        html = etree.HTML(doc)
        divs = html.xpath(r'//div[@action-type="feed_list_item"]')
        weibos = []

        for div in divs:
            try:
                weibo = self.weibo_class()
                for extractor in self.extractors:
                    extractor.extract(div, weibo)
                weibos.append(weibo)
            except:
                traceback.print_exc()
                continue

        return weibos

    def extract_html(self, text):
        """
        Extracting html from script text.
        """
        begin = len('FM.view(')
        end = len(text) - len(')')
        json_data = json.loads(text[begin: end])
        doc = json_data['html']
        return doc

    def extract_content_html(self, html):
        """
        Extracting html code that contains weibo content.
        """
        scripts = extract_script(html)
        for script in scripts:
            text = script.text.strip()
            if text.find(r'"domid":"Pl_Official_MyProfileFeed') != -1:
                return self.extract_html(text)



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
            if child.name == 'img':
                if child.has_attr('title'):
                    text += child['title']
                    img_text += child['title'] + " "
            elif child.name is None:
                t = str(child)
                text += t.strip()
            elif child.name == 'a':
                if child.has_attr('render'):
                    text += " %s " % child.text
                    at_text += child.text + " "
                else:
                    text += child.text
            elif child.name == 'em':
                for c in child.children:
                    if c.name == 'img':
                        if c.has_attr('title'):
                            text += c['title']
                            img_text += c['title'] + " "
                    elif c.name is None:
                        t = str(c)
                        text += t.strip()
                    elif c.name == 'a':
                        if c.has_attr('render'):
                            text += " %s " % c.text
                            at_text += child.text + " "
                        else:
                            text += c.text
                            
        weibo["content"] = text


class PicturesExtractor(FieldExtractor):
    def extract(self, div, weibo):
        pass


class NumberInfoExtractor(FieldExtractor):
    def extract(self, div, weibo):
        pass
