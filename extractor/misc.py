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
        script = util.select_script(scripts, r'pl.content.followTab.index')
        html = util.extract_html_from_script(script.text.strip())
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


def extract_user_info(doc):
    try:
        scripts = util.extract_script(doc)
        script = util.select_script(
            scripts, r'"domid":"Pl_Official_PersonalInfo__63"'
            )
        html = util.extract_html_from_script(script.text.strip())
        html = etree.HTML(html)
        lis = html.xpath(r'//ul/li')
        info = []
        for li in lis:
            text = li.xpath("string()")
            info.append(util.clean_text(text))
        return info
    except:
        traceback.print_exc()
        return None
