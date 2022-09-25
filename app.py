from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('a0Rbxlr9ZpBUag9bsVcypB7IS/MRBFF/Rc8v7eGEDzar5yktMsChDXlo4vWnBdY40ahI2+meXJqAGK1Y4auNtEBmVL/Vcg8icq012yGPvCm6zNRKAgU0OwOQ2l8whB0aGXxvd1IaCqx91kqCfGWAlwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7ac6887d87b0e8d1c192b7aa0324d3c0')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()