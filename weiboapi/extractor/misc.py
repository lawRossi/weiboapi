"""
@Author: Rossi
2016-01-28
This module contains exracting functions used for extracting something other
than Weibo, comment and account.
"""
import traceback
from lxml import etree
from weiboapi.util import util
import re
import json
from weiboapi.api.weibo import Weibo


def extract_domain(doc):
    start_pos = doc.find("$CONFIG['domain']='") + len("$CONFIG['domain']='")
    end_pos = doc.find("'", start_pos)
    domain = doc[start_pos:end_pos]
    return domain


def extract_relation(doc):
    scripts = util.extract_script(doc)
    script = util.select_script(scripts, r'pl.content.followTab.index')
    html = util.extract_html_from_script(script.text.strip())
    html = etree.HTML(html)
    datas = html.xpath(r'.//ul[@class="follow_list"]/li/@action-data')
    for data in datas:
        try:
            followee = {}
            splits = data.split("&")
            for split in splits:
                _splits = split.split("=")
                followee[_splits[0]] = _splits[1]
            yield followee
        except:
            traceback.print_exc()
            continue


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


def extract_user(doc, page_num=None):
    try:
        scripts = util.extract_script(doc)
        script = util.select_script(scripts, r'"pid":"pl_user_feedList"')
        json_data = re.findall("\(({.*})\)", script.text)[0]
        json_data = json.loads(json_data)
        html = etree.HTML(json_data["html"])
        divs = html.xpath(r'//div[@class="list_person clearfix"]')
        users = []
        for div in divs:
            try:
                user = {}
                detail = div.xpath(r'.//div[@class="person_detail"]')[0]
                _as = detail.xpath(r'.//p[@class="person_name"]/a')
                if len(_as) >= 1:
                    user["uid"] = _as[0].attrib.get("uid")
                    user["nick"] = _as[0].attrib.get("title")
                    user["home_url"] = _as[0].attrib.get("href")
                    if len(_as) > 1:
                        if _as[1].attrib.get("alt") != None:
                            user["verify"] = _as[1].attrib.get("alt")

                users.append(user)
            except:
                traceback.print_exc()
                continue
        if page_num:
            try:
                lis = html.xpath(r'//span[@class="list"]/div/ul/li')
                text = lis[-1].xpath(".//text()")[0]
                total = int(text[1:-1])
                return users, total
            except:
                return users, 1
        else:
            return users
    except:
        if page_num:
            return None, None
        else:
            return None


def extract_searched_weibo(doc, page_num=None):
    try:
        scripts = util.extract_script(doc)
        script = util.select_script(scripts, r'"pid":"pl_weibo_direct"')
        html = util.extract_html_from_script(script.text.strip())
        html = etree.HTML(html)
        divs = html.xpath('//div[@action-type="feed_list_item"]')
        weibos = []
        for div in divs:
            try:
                weibo = Weibo()
                weibo["mid"] = div.attrib.get("mid")
                _div = div.xpath('.//a[@class="W_texta W_fb"]')[0]
                usercard = _div.attrib.get("usercard")
                end = usercard.index("&")
                weibo["uid"] = usercard[len("id="):end]
                weibos.append(weibo)
            except:
                traceback.print_exc()

        if page_num:
            try:
                lis = html.xpath(r'//span[@class="list"]/div/ul/li')
                text = lis[-1].xpath(".//text()")[0]
                total = int(text[1:-1])
                return weibos, total
            except:
                return weibos, 1
        else:
            return weibos
    except:
        if page_num:
            return None, None
        else:
            return None
