# -*- coding: utf-8 -*-


from pymongo import MongoClient
import pymongo
import urllib.parse
from datetime import datetime 
import pandas as pd

###############################################################################
#                             股票機器人 MongoDB教學                           #
###############################################################################

######### 資料庫設定 #########
host = 'ds163870.mlab.com' #主機位置
port = '63870' #port號碼
username = urllib.parse.quote_plus('mitter') #使用者帳號
password = urllib.parse.quote_plus('554433abc') #使用者密碼
# Authentication Database認證資料庫
Authdb='trial_test'

######### 發出請求 #########
client = MongoClient('mongodb://%s:%s@%s:%s/%s?authMechanism=SCRAM-SHA-1'
                      % (username, password, host, port, Authdb))
# 切換資料庫
dbname='trial_test'
db = client[dbname]

# 輸入想搜尋的collection
collection_name = 'coll'
# 注意下方的 coll 只是我自己命名
coll = db[collection_name]



#取出所有doc
coll.find()

# 轉成list
list(coll.find())

# 插入 單行
dic = {'userid':'lw73iofqnjwenqeopop12387',
       'username':'apple',
       'creattime':datetime.now(),
       'Note':'testuser'}

coll.insert_one(dic)

# 插入 多行
dic_list = [{'userid':'nrt345iofqnjwengtgg4387',
           'username':'jarry',
           'creattime':datetime.now(),
           'Note':'testuser'},
            {'userid':'jei45646hop4454op12387',
           'username':'ketio',
           'creattime':datetime.now(),
           'Note':'testuser'},
            {'userid':'rgmmemroemrm37237y4',
           'username':'zino',
           'creattime':datetime.strptime('2018-05-30 16:20:06',
                                         '%Y-%m-%d %H:%M:%S'),
           'Note':'testuser'}]

coll.insert_many(dic_list)

# 排序 預設遞增排序 A -> Z
list(coll.find().sort("username"))
list(coll.find().sort("username",pymongo.ASCENDING))
list(coll.find().sort("username",pymongo.DESCENDING))


# 根據時間選擇（尋找區間內時間）
start = datetime.strptime('2018-04-30 16:20:06',
                           '%Y-%m-%d %H:%M:%S')
end = datetime.strptime('2018-06-30 16:20:06',
                           '%Y-%m-%d %H:%M:%S')
list(coll.find({'creattime': {'$gte': start, '$lt': end}}))

# 針對特殊id 抓取
from bson.objectid import ObjectId
list(coll.find({'_id':ObjectId('5b9dd15e38050622a264f54a')}))

# 根據條件 整個取代
coll.update({'username':'jarry'} ,
             {'Note':'updateuser'})

# 根據條件 指取代其中一個
coll.update({"username":"ketio"},
            {"$set":{"Email":"libing@126.com","Password":"123"}}) 


# 移除單個
coll.delete_one({'username':'ketio'})

# 移除多個
coll.delete_many({'Note':'testuser'}) 






