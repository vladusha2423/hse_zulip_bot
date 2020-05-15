#!flask/bin/python
import sys
sys.path.insert(1, 'venv/Lib/site-packages')
from flask import Flask, request
import bot

app = Flask(__name__)
# Bot = bot.BotHandler()


@app.route('/api/send-msg', methods=['POST'])
def index():
    data = request.get_json() or {}
    if 'email' in data and 'msg' in data:
        bot.BotHandler().send_private_msg(email=data['email'], content=data['msg'])
        return 'OK'
    else:
        return 'please send both email and link'


if __name__ == '__main__':
    app.run(debug=True)

# Bot.client.call_on_each_message(Bot.get_msg)

