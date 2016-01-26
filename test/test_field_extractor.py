"""
@Author: Rossi
2016-01-26
"""

from weiboapi.extractor.field_extractor import FieldExtractor


def test_extractor():
    assert getattr(FieldExtractor, "extract_content") is not None

