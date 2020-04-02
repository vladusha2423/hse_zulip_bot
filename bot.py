import sys
sys.path.insert(1, 'venv/lib/python3.7/site-packages')
import zulip
import timetable


BOT_MAIL = "hse-bot@chat.miem.hse.ru"
HSE_API = "https://www.hse.ru/api/timetable/lessons?"

HELLO_MESSAGE = '''
Доброго времени суток!

Я, Service Bot, призван помочь узнавать расписание прямо в диалоге со мной или в стриме, упомянув меня в сообщении 
(через @) :)

Есть один момент. Если Вы преподаватель, то для корректного вывода расписания вам надо дать мне понять об этом.
Для этого напишите мне какое-нибудь сообщение, содержащее ключевое слово "преподаватель".

Пример: "Я - преподаватель".

Перейдем к расписанию. 
Самый быстрый способ его узнать - написать мне сообщение с одним только ключевым словом "Расписание".

Пример: "Покажи мне расписание!" или просто "расписание"

Такой способ показывает положение дел на текущую неделю.
Если нужно конкретнее указать, на какой день или на какой период расписание необходимо, есть несколько способов:

"Расписание на сегодня"
"Расписание на завтра"
"Расписание на dd.MM.yyyy" - Будьте внимательны. Число всегда содержит две цифры (5 мая 2020 года = 05.05.2020).
"Расписание на dd.MM.yyyy-dd.MM.yyyy" - на период

Также, есть возможность узнать расписание приятеля или преподавателя. 
Нужно всего лишь знать его корпоративную почту и добавить в конец сообщения фразу "для xxx@edu.hse.ru".

Пример: "расписание на завтра для msmeladze@hse.ru"

Чтобы уточнить список команд, отправь мне сообщение с ключевым словом "Помощь".

'''
HELP_MESSAGE = '''
Доброго времени суток!

Я, Service Bot, призван помочь узнавать расписание прямо в диалоге со мной или в стриме, упомянув меня в сообщении 
(через @) :)

Самый быстрый способ - написать мне сообщение с одним только ключевым словом "Расписание".

Пример: "Покажи мне расписание!" или просто "расписание"

Такой способ показывает положение дел на текущую неделю.
Если нужно конкретнее указать, на какой день или на какой период расписание необходимо, есть несколько способов:

"Расписание на сегодня"
"Расписание на завтра"
"Расписание на dd.MM.yyyy" - Будьте внимательны. Число всегда содержит две цифры (5 мая 2020 года = 05.05.2020).
"Расписание на dd.MM.yyyy-dd.MM.yyyy" - на период

Также, есть возможность узнать расписание приятеля или преподавателя. 
Нужно всего лишь знать его корпоративную почту и добавить в конец сообщения фразу "для xxx@edu.hse.ru".

Пример: "расписание на завтра для msmeladze@hse.ru"

Если Вы преподаватель, то для корректного вывода расписания вам надо дать мне понять об этом.
Для этого напишите мне какое-нибудь сообщение, содержащее ключевое слово "преподаватель".

Пример: "Я - преподаватель".

'''


class BotHandler(object):
    def __init__(self):
        self.client = zulip.Client(config_file="zuliprc")

    def get_msg(self, msg):
        if msg["sender_email"] != "hse-bot@chat.miem.hse.ru":
            for i in msg.keys():
                print(i, ':', msg[i])
            self.check_msg(msg)

    def send_msg(self, msg, content):
        if msg["type"] == 'private':
            request = {
                "type": "private",
                "to": msg["sender_email"],
                "content": content
            }
            self.client.send_message(request)
        elif msg["type"] == 'stream':
            request = {
                "type": "stream",
                "to": msg["display_recipient"],
                "topic": msg["subject"],
                "content": content
            }
            print(request)
            self.client.send_message(request)

    def send_private_msg(self, email, content):
        request = {
            "type": "private",
            "to": email,
            "content": content
        }
        self.client.send_message(request)

    def check_msg(self, msg):
        words = msg["content"].lower().split()
        if (msg["type"] == 'private' or '@**Service Bot**' in msg["content"]) \
                and msg['sender_full_name'] != 'Service Bot':
            if "расписание" in words:
                self.send_msg(msg,
                              timetable.check_msg(msg["sender_email"], msg["content"], msg["sender_id"]))
            elif "преподаватель" in words:
                self.send_msg(msg,
                              timetable.check_msg(msg["sender_email"], msg["content"], msg["sender_id"]))
            elif "привет" in words:
                self.send_msg(msg, HELLO_MESSAGE)
            elif "помощь" in words:
                self.send_msg(msg, HELP_MESSAGE)
            else:
                self.send_msg(msg, "Не знаю что и ответить :(. \n"
                                   "Чтобы узнать какие у меня есть команды, напиши 'Помощь'")


# Bot = BotHandler()
# Bot.client.call_on_each_message(Bot.get_msg)
# handler_class = BotHandler
