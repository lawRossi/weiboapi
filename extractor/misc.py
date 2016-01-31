"""
@Author: Rossi
2016-01-28
"""
import traceback
from lxml import etree
from weiboapi.util import util


def extract_domain(doc):
    start_pos = doc.find("$CONFIG['domain']='") + len("$CONFIG['domain']='")
    end_pos = doc.find("'", start_pos)
    domain = doc[start_pos:end_pos]
    return domain


def extract_relation(doc):
    try:
        scripts = util.extract_script(doc)
        html = None
        for script in scripts:
            text = script.text.strip()
            if text.find(r'pl.content.followTab.index') != -1:
                html = util.extract_html_from_script(text)
        if not html:
            return
        html = etree.HTML(html)
        datas = html.xpath(r'.//ul[@class="follow_list"]/li/@action-data')
        followees = []
        for data in datas:
            followee = {}
            splits = data.split("&")
            for split in splits:
                _splits = split.split("=")
                followee[_splits[0]] = _splits[1]

            followees.append(followee)

        return followees
    except:
        traceback.print_exc()
        return None
