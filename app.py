##載入LineBot所需要的套件
#from flask import Flask, request, abort
#
#from linebot import (
#    LineBotApi, WebhookHandler
#)
#from linebot.exceptions import (
#    InvalidSignatureError
#)
#from linebot.models import *
#
#app = Flask(__name__)
#
## 必須放上自己的Channel Access Token
#line_bot_api = LineBotApi('1VQGdLbDdmlpaEKonuPlg5lJczQzvQzoTYkreebQ/FQHiJMjNgt2P9CI3a2JrVQyWlnYRV2VOiXiBlM4k4u+OrQqRX74X6XKVVW0TnlOhHCm6EesFoSJXXnvi7RLAWQXjI6IkCCtCh7+L+Sjug1ktAdB04t89/1O/w1cDnyilFU=')
## 必須放上自己的Channel Secret
#handler = WebhookHandler('a227e7f5daf93c58b285bdcfcc5dc9e3')
#yourid='U801d402e8e9ced65a6a6d7d25c5f0fb3'
#line_bot_api.push_message(yourid, TextSendMessage(text='你可以開始了'))
#
## 監聽所有來自 /callback 的 Post Request
#@app.route("/callback", methods=['POST'])
#def callback():
#    # get X-Line-Signature header value
#    signature = request.headers['X-Line-Signature']
#
#    # get request body as text
#    body = request.get_data(as_text=True)
#    app.logger.info("Request body: " + body)
#
#    # handle webhook body
#    try:
#        handler.handle(body, signature)
#    except InvalidSignatureError:
#        abort(400)
#
#    return 'OK'
#
##訊息傳遞區塊
#@handler.add(MessageEvent, message=TextMessage)
#def handle_message(event):
#    message = TextSendMessage(text=event.message.text)
#    line_bot_api.reply_message(event.reply_token,message)
#
##主程式
#import os
#if __name__ == "__main__":
#    port = int(os.environ.get('PORT', 5000))
#    app.run(host='0.0.0.0', port=port)
#










#-------------------------------- 幫你報股價 ---------------------------------

#載入LineBot所需要的套件
#from flask import Flask, request, abort
#
#from linebot import (
#    LineBotApi, WebhookHandler
#)
#from linebot.exceptions import (
#    InvalidSignatureError
#)
#from linebot.models import *
#import Standard_Deviation
#import re
#from bs4 import BeautifulSoup
#import requests
#
#app = Flask(__name__)
#
## 必須放上自己的Channel Access Token
#line_bot_api = LineBotApi('你自己的token')
## 必須放上自己的Channel Secret
#handler = WebhookHandler('你自己的Secret')
#yourid='你自己的ID'
#line_bot_api.push_message(yourid, TextSendMessage(text='你可以開始了'))
#
## 監聽所有來自 /callback 的 Post Request
#@app.route("/callback", methods=['POST'])
#def callback():
#    # get X-Line-Signature header value
#    signature = request.headers['X-Line-Signature']
#
#    # get request body as text
#    body = request.get_data(as_text=True)
#    app.logger.info("Request body: " + body)
#
#    # handle webhook body
#    try:
#        handler.handle(body, signature)
#    except InvalidSignatureError:
#        abort(400)
#
#    return 'OK'
#
##訊息傳遞區塊
#@handler.add(MessageEvent, message=TextMessage)
#def handle_message(event):
#    message = event.message.text #取得使用者訊息
#    if re.match('[0-9]{4}',message):
#        ########## 開始請求網站，報價 ##########
#        url = 'https://tw.stock.yahoo.com/q/q?s=' + message # 要請求的網址
#        list_req = requests.get(url) #請求
#        soup = BeautifulSoup(list_req.content, "html.parser") # 取得所有網站內容
#        getstock= soup.find('b').text # 拉出股價
#        line_bot_api.push_message(yourid, TextSendMessage(text=getstock))#推訊息出去瞜
#        
#        ########## 開始請求網站，報價 ##########
#        line_bot_api.push_message(yourid, TextSendMessage(text=Standard_Deviation.searchstock(message)))#推訊息出去瞜
#        
#    else:
#        line_bot_api.push_message(yourid, TextSendMessage(text='請打上股票代號'))#推訊息出去瞜
#        
##主程式
#import os
#if __name__ == "__main__":
#    port = int(os.environ.get('PORT', 5000))
#    app.run(host='0.0.0.0', port=port)














#-------------------------------- 神秘的小房間 ---------------------------------


import requests
import datetime
from bs4 import BeautifulSoup
from flask import Flask, request, abort	
from linebot import (LineBotApi, WebhookHandler, exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import mongodb
import re
import json
import Standard_Deviation

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('1VQGdLbDdmlpaEKonuPlg5lJczQzvQzoTYkreebQ/FQHiJMjNgt2P9CI3a2JrVQyWlnYRV2VOiXiBlM4k4u+OrQqRX74X6XKVVW0TnlOhHCm6EesFoSJXXnvi7RLAWQXjI6IkCCtCh7+L+Sjug1ktAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('2b6fcc6cce5d335afc320bed4457febf')
yourid='U801d402e8e9ced65a6a6d7d25c5f0fb3'
line_bot_api.push_message(yourid, TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):  
    ### 抓到顧客的資料 ###
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id #使用者ID
    usespeak = event.message.text #取得使用者訊息
#####################################系統功能按鈕##############################

    if re.match('[0-9]{4}[<>][0-9]',usespeak): # 先判斷是否是使用者要用來存股票的
        mongodb.write_user_stock_fountion(stock=usespeak[0:4], bs=usespeak[4:5], price=usespeak[5:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak[0:4]+'已經儲存成功'))
        return 0

    elif re.match('刪除[0-9]{4}',usespeak): # 刪除存在資料庫裡面的股票
        mongodb.delete_user_stock_fountion(stock=usespeak[2:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak+'已經刪除成功'))
        return 0
        
    elif re.match('[0-9]{4}',usespeak): # 如果只有給四個數字就判斷是股票查詢
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
        ######### 開始請求網站，報價 ##########
        url = 'https://tw.stock.yahoo.com/q/q?s=' + message # 要請求的網址
        list_req = requests.get(url) #請求
        soup = BeautifulSoup(list_req.content, "html.parser") # 取得所有網站內容
        getstock= soup.find('b').text # 拉出股價
        line_bot_api.push_message(yourid, TextSendMessage(text=getstock))#推訊息出去瞜
        return 0
    
    elif re.match('我的股票',usespeak):  # 秀出所有自動推撥的股票

        get=mongodb.show_user_stock_fountion()
        msg=''

        if len(get) >0:
            for i in get:  
                msg += i['stock'] + " " + i['bs'] + " " + str(i['price']) +'\n'
            line_bot_api.push_message(uid, TextSendMessage(msg))
        
        else:
            line_bot_api.push_message(uid, TextSendMessage('沒有資料'))
            return 0

        
    else: # 都找不到就回答看不懂
        line_bot_api.push_message(uid, TextSendMessage(usespeak +'是啥？ 看不懂'))
        return 0

                    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 27017))
    app.run(host='0.0.0.0', port=port)



