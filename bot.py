import sys
sys.path.insert(1, 'venv/Lib/site-packages')
import zulip
import timetable
import record


BOT_MAIL = "hse-bot@chat.miem.hse.ru"
HSE_API = "https://www.hse.ru/api/timetable/lessons?"

HELLO_MESSAGE = '''
Доброго времени суток!

Я, Service Bot, cоздан для интеграции Зулипа с некоторыми сервисами МИЭМа

С моей помощью вы можете: 
1) Узнать расписание для себя или другого человека
Чтобы уточнить список команд для работы с расписанием, отправьте мне сообщение с ключевой фразой "Помощь расписание"

2) Отправить запрос на запись занятия
Чтобы уточнить список команд для работы с расписанием, отправьте мне сообщение с ключевой фразой "Помощь запись"

'''
HELP_RUZ_MESSAGE = '''
Я, Service Bot, могу помочь узнавать расписание прямо в диалоге со мной или в стриме, упомянув меня в сообщении 
(через @) :)

Самый быстрый способ - написать мне сообщение с одним только ключевым словом "Расписание".

Пример: "Покажи мне расписание" или просто "расписание"

Такой способ показывает положение дел на текущую неделю.
Если нужно конкретнее указать, на какой день или на какой период расписание необходимо, есть несколько способов:

"Расписание на сегодня"
"Расписание на завтра"
"Расписание на dd.MM.yyyy" - на день, соответствующий какой-то дате
"Расписание на dd.MM.yyyy-dd.MM.yyyy" - на период
"Расписание на среду" - на какой-то день недели (день недели в винительном падеже :))

Также, есть возможность узнать расписание приятеля или преподавателя. 
Нужно всего лишь знать его корпоративную почту и добавить в конец сообщения фразу "для xxx@edu.hse.ru".

Пример: "расписание на завтра для msmeladze@hse.ru"

'''

HELP_NVR_MESSAGE = '''
Я, Service Bot, могу помочь получить запись лекции прямо в диалоге со мной или в стриме, упомянув меня в сообщении 
(через @) :)

Чтобы получить список доступных аудиторий, введите команду "Список аудиторий"

Чтобы запросить видеозапись занятия, отправьте сообщение с номером аудитории, датой, временем начала и окончания записи, 
а также названием будущей видеозаписи в таком формате: "запись room_name dd.MM.yyyy hh:mm-hh:mm event_name". Например,
"запись 504 11.09.2020 9:00-10:20 лекция"
'''


class BotHandler(object):
    def __init__(self):
        self.client = zulip.Client(config_file="zuliprc")

    def get_msg(self, msg):
        if msg["sender_email"] != "hse-bot@chat.miem.hse.ru":
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
            self.client.send_message(request)

    def send_private_msg(self, email='', content=''):
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
            if "помощь" in words:
                if "расписание" in words:
                    self.send_msg(msg, HELP_RUZ_MESSAGE)
                elif "запись" in words:
                    self.send_msg(msg, HELP_NVR_MESSAGE)
                else:
                    self.send_msg(msg, HELLO_MESSAGE)
            elif "расписание" in words:
                self.send_msg(msg,
                              timetable.check_msg(msg["sender_email"], msg["content"], msg["sender_id"]))
            elif "привет" in words:
                self.send_msg(msg, HELLO_MESSAGE)
            elif "запись" in words:
                self.send_msg(msg,
                              record.check_msg(msg["sender_email"], msg["content"]))
            elif "список" in words and "аудиторий" in words:
                rooms = ', '.join(record.get_rooms())
                self.send_msg(msg, 'Доступные аудитории:\n' + rooms)
            else:
                self.send_msg(msg, "Не знаю что и ответить :(. \n"
                                   "Чтобы узнать какие у меня есть команды, напиши 'Помощь'")


if __name__ == '__main__':
    Bot = BotHandler()
    Bot.client.call_on_each_message(Bot.get_msg)
    handler_class = BotHandler
