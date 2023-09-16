
# -*- coding: utf-8 -*-
# File : database.py
# Time : 2023/9/13 15:07 
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

mvs_db_wines = MilvusDB()
mvs_db_wines.db_name = 'wine'
mvs_db_wines.collection = 'wine_data'
output_fields_wines = [field.name for field in mvs_db_wines.collection.schema.fields if
                 field.name not in {'id', 'wine_info_embed'}]