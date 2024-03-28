#======python的函數庫==========
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
# 從linebot.models模組 匯入代表傳入訊息的事件的 messafeEvent類別、代表文字訊息的TextMessage類別,以及用來回復文字訊息的 TextSendMessage類別
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import tempfile, os
import datetime
import openai
import time
import traceback
#=============================
from my_commands.bot_gpt import get_reply
#==============================

# 初始化Flask應用程式,這是Flask運作的核心.app會根據設定的路由和對應的涵式來處理HTTP請求
app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# 讀取金鑰區
api = LineBotApi(os.getenv('LINE_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_SECRET'))
openai.api_key = os.getenv('OPENAI_API_KEY')


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
     # 取得 X-Line-Signature 表頭電子簽章內容
     # Line傳送過來的電子簽章.由於這個電子簽章式已建立通道時取得的密鑰為基準,可以篩選不是由我的通道送來的請求
    signature = request.headers['X-Line-Signature']
    # 以文字形式取得請求內容
    # 以文字形式取的請求內容並透過app來記錄,這會在稍後驗證電子簽章時使用
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # 比對電子簽章並處理請求內容
    # 以剛剛取得的請求內容及表頭中的電子簽章進行驗證,電子簽章驗證錯誤會拋出例外訊息;驗證正確,則會自動呼叫稍後設定的處理涵式
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("電子簽章錯誤, 請檢查密鑰是否正確？")
        abort(400)
    return 'OK'


# 當驗證電子簽章成功時,由下一行定義的handle_message 函式來處理接收到的文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    msg = [{
      "role": "system",
      "content": "reply in 繁體中文"
    }, {
      "role": "user",
      "content": user_message
    }]
    reply_text = get_reply(msg)
  #接著將回復訊息包裝到 TextSendMessage 物件中回傳到通道
    api.reply_message(event.reply_token, TextSendMessage(reply_text))

     
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)