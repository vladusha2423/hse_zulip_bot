#!flask/bin/python
from flask import Flask, request
import bot

app = Flask(__name__)
Bot = bot.BotHandler()


@app.route('/record', methods=['POST'])
def index():
    data = request.get_json() or {}
    if 'email' in data and 'link' in data:
        Bot.send_private_msg(data['email'], data['link'])
        return 'OK'
    else:
        return 'please send both email and link'


if __name__ == '__main__':
    app.run(debug=True)


Bot.client.call_on_each_message(Bot.get_msg)
handler_class = bot.BotHandler
