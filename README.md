Description:

    知乎助手 - 帮助知乎用户实现官方未提供的功能。

    ZhihuHelper
        Helping user@Zhihu.com get functions unoffical.

Requires:
    requests, BeautifulSoup

Usage:
    python answer.py -u <username> -p <password> [-d, -b]

History:
++++++++++++++++++++
0.1

该版本只实现了一些零散的功能，问题还有很多。通过使用
 answer.py 可以备份/删除登录用户的答案。

使用方法：
    必须使用合法用户身份登录，因此-u与-p为必填项。使用-b
    备份登录用户的答案、-d删除登录用户的答案。

    ***** 强烈建议备份答案，慎用删除功能 *****

    举例：
        python answer.py -u 'user@zhihu.com' -p '123456' -b -d

    上述命令可以实现备份并删除用户'user@zhihu.com'的所有答案。
