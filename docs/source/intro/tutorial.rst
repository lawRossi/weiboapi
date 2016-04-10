=========
Tutorial
=========


Login
-----

.. module:: weiboapi
   :synopsis: api functions.


When using the package, you need first to call :meth:`~weiboapi.api.api.login` method in
order to use other api functions. You do something like this::

    import weiboapi

    weiboapi.login("username", "password")

You need to replace "username" and "password" with your username of Sina
Weibo and the coresponding password. The :meth:`~weiboapi.api.api.login` method 
returns ``True`` or ``False``, so you can judge whether you login successfully.



.. Note:: You need to login by calling :meth:`~weiboapi.api.api.login` only once.


Retrieving Weibo posts
----------------------
You can retrieving Weibo posts of a specified account using :meth:`~weiboapi.api.api.get_weibos` function. See an example::
    
    import weiboapi
    weiboapi.login("username", "password")
    weibos = weiboapi.get_weibos("2237529652", "100505", page=2)
    print(len(weibos))
    print(weibos[0])


You will see the result::
    
    45
    {'comment_number': 8,
    'content': '\xe5\xad\xb0\xe8\xbd\xbb\xe5\xad\xb0\xe9\x87\x8d[\xe6\x9c\x88\xe4\ba\xae]',
    'date': '2014-08-08 02:32:49',
    'is_repost': True,
    'like_number': 0,
    'link_text': u'\u522b\u628a\u5355\u53cd\u73a9\u6210\u50bb\u74dc\u673a\uff01\u6
        00\u5b9e\u7528\u5355\u53cd\u5165\u95e8\uff01||\u6587\u7ae0\u8be6\u60c5||198||',
    'links': ['http://t.cn/RPN6Mkw',
           'http://t.cn/RPN6Mkw',
           'javascript:void(0)',
           'javascript:void(0)'],
    'mid': '3741121643558040',
    'omid': '3740924683723337',
    'pictures': ['http://ww1.sinaimg.cn/large/a716fd45jw1ej7iiqgut7j20i20bzjrx.jpg],
    'repost_number': 1,
    'root_url': u'http://weibo.com/1656831930/BhaDyfCBP',
    'source': u'iPhone\u5ba2\u6237\u7aef',
    'uid': None,
    'url': u'http://weibo.com/2237529652/BhfLeeVBK'}

:meth:`~weiboapi.api.api.get_weibos` returns a list of instances of 
:class:`~weiboapi.api.weibo.Weibo` class.
