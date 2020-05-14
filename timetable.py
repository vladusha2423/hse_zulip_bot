import ruz
import csv
import datetime
import re
import check_user

DaysOfWeek = {
    'Пн': 'Понедельник',
    'Вт': 'Вторник',
    'Ср': 'Среда',
    'Чт': 'Четверг',
    'Пт': 'Пятница',
    'Сб': 'Суббота',
    'Вс': 'Воскресенье'
}


def get_lessons(email, date_start='', date_end='', sender_id=0, other_email=''):
    if other_email == '404':
        return 'Таких пользователей несколько. Попробуйте вместо упоминания использовать почту человека.'
    if other_email != '':
        if date_start != '' and date_end != '':
            response = ruz.person_lessons(other_email, date_start, date_end)
        else:
            response = ruz.person_lessons(other_email)
    else:
        checked_user = check_user.check(email)
        if checked_user:
            if date_start != '' and date_end != '':
                response = ruz.person_lessons(checked_user, date_start, date_end)
            else:
                response = ruz.person_lessons(checked_user)
        else:
            return 'В базе отсутствует такой пользователь('
    message = ''
    curr_date = ''
    if not response:
        return 'Запрос ничего не выдал(. Перепроверьте ваше сообщение. Если все в порядке, то есть два варианта: каникулы или лег руз:)'
    for lesson in response:
        if curr_date != lesson['date']:
            message += DaysOfWeek[lesson['dayOfWeekString']] + ':: ' + lesson['date'] + '\n'
            curr_date = lesson['date']
        message += str(lesson['lessonNumberStart']) + ' пара (' + \
                   lesson['beginLesson'] + '-' + lesson['endLesson'] + ')\n' + \
                   lesson['discipline'] + '\n' + \
                   lesson['kindOfWork'] + '\n'
        if datetime.datetime.strptime(lesson['date'], '%Y.%m.%d').date() < datetime.date(2020, 3, 17):
            message += lesson['auditorium'] + ' (' + lesson['building'] + ')' + '\n'
        else:
            if lesson['url1']:
                message += 'Видеочат: ' + lesson['url1'] + '\n'
            else:
                message += 'Видеочат: online\n'
        message += lesson['lecturer'] + '\n\n'
    return message


def check_msg(sender_email, content, sender_id):
    words = content.lower().split()
    if "расписание" in words:
        if 'сегодня' in words:
            today = datetime.datetime.now().date().isoformat().replace('-', '.')
            if 'для' in words:
                if '@**' in words[words.index('для') + 1]:
                    return get_lessons(sender_email, date_start=today, date_end=today, sender_id=sender_id,
                                       other_email=check_user.check_by_name(remove_dog(words[words.index('для') + 1] + ' ' + words[words.index('для') + 2])))
                return get_lessons(sender_email, date_start=today, date_end=today, sender_id=sender_id,
                                   other_email=words[words.index('для') + 1])
            else:
                return get_lessons(sender_email, date_start=today, date_end=today, sender_id=sender_id)
        elif 'завтра' in words:
            tomorrow = (datetime.datetime.now() + datetime.timedelta(1)).date().isoformat().replace('-', '.')
            if 'для' in words:
                if '@**' in words[words.index('для') + 1]:
                    return get_lessons(sender_email, date_start=tomorrow, date_end=tomorrow, sender_id=sender_id,
                                       other_email=check_user.check_by_name(remove_dog(words[words.index('для') + 1] + ' ' + words[words.index('для') + 2])))
                return get_lessons(sender_email, date_start=tomorrow, date_end=tomorrow, sender_id=sender_id,
                                   other_email=words[words.index('для') + 1])
            else:
                return get_lessons(sender_email, date_start=tomorrow, date_end=tomorrow, sender_id=sender_id)
        else:
            date = re.search(r'\d\d.\d\d.\d{4}', content)
            if date:
                start = content.index(date.group())
                date_end = re.search(r'\d\d.\d\d.\d{4}', content[start + 10:])
                if date_end:
                    if 'для' in words:
                        if '@**' in words[words.index('для') + 1]:
                            return get_lessons(sender_email, date_start=reverse_date(date.group()),
                                               date_end=reverse_date(date_end.group()), sender_id=sender_id,
                                               other_email=check_user.check_by_name(remove_dog(words[words.index('для') + 1] + ' ' + words[words.index('для') + 2])))
                        return get_lessons(sender_email, date_start=reverse_date(date.group()),
                                           date_end=reverse_date(date_end.group()), sender_id=sender_id,
                                           other_email=words[words.index('для') + 1])
                    else:
                        return get_lessons(sender_email, date_start=reverse_date(date.group()),
                                           date_end=reverse_date(date_end.group()), sender_id=sender_id)
                else:
                    if 'для' in words:
                        if '@**' in words[words.index('для') + 1]:
                            return get_lessons(sender_email, date_start=reverse_date(date.group()),
                                               date_end=reverse_date(date.group()), sender_id=sender_id,
                                               other_email=check_user.check_by_name(remove_dog(words[words.index('для') + 1] + ' ' + words[words.index('для') + 2])))
                        return get_lessons(sender_email, date_start=reverse_date(date.group()),
                                           date_end=reverse_date(date.group()), sender_id=sender_id,
                                           other_email=words[words.index('для') + 1])
                    else:
                        return get_lessons(sender_email, date_start=reverse_date(date.group()),
                                           date_end=reverse_date(date.group()), sender_id=sender_id)
            else:
                if 'для' in words:
                    if '@**' in words[words.index('для') + 1]:
                        return get_lessons(sender_email, sender_id=sender_id,
                                           other_email=check_user.check_by_name(
                                               remove_dog(words[words.index('для') + 1] + ' ' + words[words.index('для') + 2])))
                    return get_lessons(sender_email, sender_id=sender_id,
                                       other_email=words[words.index('для') + 1])
                else:
                    return get_lessons(sender_email, sender_id=sender_id)


def reverse_date(date):
    list_date = list(map(str, date.split('.')))
    if len(list_date[0]) == 1:
        list_date[0] = '0' + list_date[0]
    res_date = '.'.join(list_date[::-1])
    return res_date


def remove_dog(name):
    print(name)
    return name.replace('**', '').replace('@', '')
