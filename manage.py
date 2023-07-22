# -*- coding: utf-8 -*-
# File : manage.py.py
# Time : 2023/7/21 9:38 
# Author : Dijkstra Liu
# Email : l.tingjun@wustl.edu
# 
# 　　　    /＞ —— フ
# 　　　　　| `_　 _ l
# 　 　　　ノ  ミ＿xノ
# 　　 　 /　　　 　|
# 　　　 /　 ヽ　　ﾉ
# 　 　 │　　|　|　\
# 　／￣|　　 |　|　|
#  | (￣ヽ＿_ヽ_)__)
# 　＼_つ
#
# Description: Creat an app and run it.
#

from flask_app.app import create_app

if __name__ == 'main':
    app = create_app()
    app.run()
