import requests
import re


def montage_event(room, start_time, end_time, date, event_name, email):
    json = {
        "start_time": start_time,
        "end_time": end_time,
        "date": reverse_date(date),
        "event_name": event_name,
        "user_email": email
    }
    print(room)
    print(json)
    response = requests.post(
        'https://nvr.miem.hse.ru/api/montage-event/' + room,
        headers={"key": "49433faafad24c4c8944564cb076eadb", "content-type": "application/json"},
        params={'q': 'requests+language:python'},
        json=json
    )
    return response.status_code == 200 or response.status_code == 201


def get_rooms():
    response = requests.get(
        'https://nvr.miem.hse.ru/api/rooms',
        headers={'key': '49433faafad24c4c8944564cb076eadb'},
    )
    return [r["name"] for r in response.json()]


def check_msg(sender_email, content):
    words = content.split()
    if len(words) > 3:
        date = re.search(r'([1-9]|0[1-9]|[12][0-9]|3[01])[- /.]([1-9]|0[1-9]|1[012])[- /.](19|20)\d\d$', words[2])
        time = re.search(r'^(\d|[01]\d|2[0-3])(:[0-5]\d)[-](\d|[01]\d|2[0-3])(:[0-5]\d)$', words[3])

        rooms = [item.lower() for item in get_rooms()]
        print(rooms)

        if words[1].lower() in rooms:
            if date:
                if time:
                    times = time.group().split('-')
                    if montage_event(
                            words[1],
                            times[0],
                            times[1],
                            date.group(),
                            words[4] if len(words) > 4 else '',
                            sender_email
                    ):
                        return 'Запрос на склейку отправлен, когда всё будет готово я сообщу'
                    else:
                        return 'Ошибка сервера :\'('
                else:
                    return 'Неверный формат временного интервала :( ПроверьТЕ свои данные.'
            else:
                return 'Неверный формат даты :( Проверьте введенные данные'
        else:
            return 'Такой аудитории не существует :( Проверьте введенные данные'
    else:
        return 'Недостаточно данных'


def reverse_date(date):
    list_date = list(map(str, date.split('.')))
    if len(list_date[0]) == 1:
        list_date[0] = '0' + list_date[0]
    if len(list_date[1]) == 1:
        list_date[1] = '0' + list_date[1]
    res_date = '-'.join(list_date[::-1])
    return res_date


    # запись 504 dd.MM.yyyy hh:mm-hh:mm event_name




