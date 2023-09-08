# -*- coding: utf-8 -*-
# File : dropWineData.py
# Time : 2023/9/7 17:56 
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
# Description:
from databaseMod.milvusDB import MilvusDB


mvs_db = MilvusDB()
mvs_db.db_name = 'wine'
mvs_db.collection = 'wine_data'
mvs_db.drop_collection_by_name('wine_data')