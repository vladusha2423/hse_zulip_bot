#!flask/bin/python
from flask import Flask, request
import bot

app = Flask(__name__)
# Bot = bot.BotHandler()


@app.route('/record', methods=['POST'])
def index():
    data = request.get_json() or {}
    print(data)
    if 'email' in data and 'link' in data:
        bot.BotHandler().send_private_msg(email=data['email'], content=data['link'])
        return 'OK'
    else:
        return 'please send both email and link'

if __name__ == '__main__':
    app.run(debug=True)

# Bot.client.call_on_each_message(Bot.get_msg)

