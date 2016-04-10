##Introduction
This is an api of Sina Weibo, which provides interfaces for retriving Weibos and comments, posting Weibo and comments, etc.  
This api is a third-party one. It's developed based on web page crawling and parsing, so, it's not efficient. But it's easy to obtain and easy to use after all.

##Author
Author: Rossi  
luoweiang@gmail.com

##Installation
Clone the code: git clone https://github.com/lawRossi/weiboapi.git .  
Then execute the setup.py by command "python setup.py install".

##Python version
This package supports both python2.7 and python3.4.

##Dependencies
This package dependends on following packages:  
lxml  
rsa  
BeautifulSoup4 

##Building documentation
If you want to build documentation, the sphinx package is needed.
To build the documentation, just swich to the docs directory and 
type ``make`` and read the help message.