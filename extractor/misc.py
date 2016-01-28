"""
@Author: Rossi
2016-01-28
"""


def extract_domain(doc):
    start_pos = doc.find("$CONFIG['domain']='") + len("$CONFIG['domain']='")
    end_pos = doc.find("'", start_pos)
    domain = doc[start_pos:end_pos]
    return domain
