"""
@Author: Rossi
2016-02-01
"""
from os.path import dirname, join
from setuptools import setup, find_packages


with open(join(dirname(__file__), 'weiboapi/VERSION'), 'r') as f:
    version = f.read().strip()


setup(
    name="weiboapi",
    version=version,
    description="Sina weibo api.",
    author="Rossi",
    packages=find_packages(exclude=("test", "test.*")),
    install_requires=[
        "lxml",
        "rsa",
        "BeautifulSoup4"
    ]
)
