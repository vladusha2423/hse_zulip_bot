import ruz
import csv
import datetime
import re

DaysOfWeek = {
    'Пн': 'Понедельник',
    'Вт': 'Вторник',
    'Ср': 'Среда',
    'Чт': 'Четверг',
    'Пт': 'Пятница',
    'Сб': 'Суббота',
    'Вс': 'Воскресенье'
}


def check_csv(tid):
    with open('teacher_id.csv', "r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
            for r in row:
                if tid == int(r):
                    return 'hse.ru'
    return 'edu.hse.ru'


def get_lessons(email, date_start='', date_end='', sender_id=0, other_email=''):
    if other_email != '':
        if date_start != '' and date_end != '':
            response = ruz.person_lessons(other_email, date_start, date_end)
        else:
            response = ruz.person_lessons(other_email)
    else:
        if date_start != '' and date_end != '':
            response = ruz.person_lessons(email.replace('miem.hse.ru', check_csv(sender_id)), date_start, date_end)
        else:
            response = ruz.person_lessons(email.replace('miem.hse.ru', check_csv(sender_id)))
    message = ''
    curr_date = ''
    print('LESSSSSSONS: \n', response)
    if not response:
        return 'Запрос ничего не выдал. Тут два варианта: каникулы или лег руз :)'
    for lesson in response:
        if curr_date != lesson['date']:
            message += DaysOfWeek[lesson['dayOfWeekString']] + ':: ' + lesson['date'] + '\n'
            curr_date = lesson['date']
        message += str(lesson['lessonNumberStart']) + ' пара (' + \
                   lesson['beginLesson'] + '-' + lesson['endLesson'] + ')\n' + \
                   lesson['discipline'] + '\n' + \
                   lesson['kindOfWork'] + '\n' + \
                   lesson['auditorium'] + ' (' + lesson['building'] + ')' + '\n' + \
                   lesson['lecturer'] + '\n\n'
    return message


def check_msg(sender_email, content, sender_id):
    words = content.lower().split()
    if "расписание" in words:
        if 'сегодня' in words:
            today = datetime.datetime.now().date().isoformat().replace('-', '.')
            if 'для' in words:
                return get_lessons(sender_email, date_start=today, date_end=today, sender_id=sender_id,
                                   other_email=words[words.index('для') + 1])
            else:
                return get_lessons(sender_email, date_start=today, date_end=today, sender_id=sender_id)
        elif 'завтра' in words:
            tomorrow = (datetime.datetime.now() + datetime.timedelta(1)).date().isoformat().replace('-', '.')
            if 'для' in words:
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
                        return get_lessons(sender_email, date_start=reverse_date(date.group()),
                                           date_end=reverse_date(date_end.group()), sender_id=sender_id,
                                           other_email=words[words.index('для') + 1])
                    else:
                        return get_lessons(sender_email, date_start=reverse_date(date.group()),
                                           date_end=reverse_date(date_end.group()), sender_id=sender_id)
                else:
                    if 'для' in words:
                        return get_lessons(sender_email, date_start=reverse_date(date.group()),
                                           date_end=reverse_date(date.group()), sender_id=sender_id,
                                           other_email=words[words.index('для') + 1])
                    else:
                        return get_lessons(sender_email, date_start=reverse_date(date.group()),
                                           date_end=reverse_date(date.group()), sender_id=sender_id)
            else:
                if 'для' in words:
                    return get_lessons(sender_email, sender_id=sender_id,
                                       other_email=words[words.index('для') + 1])
                else:
                    return get_lessons(sender_email, sender_id=sender_id)
    elif "преподаватель" in words:
        with open('teacher_id.csv', "r") as file:
            reader = csv.reader(file)
            ids = []
            for r in reader:
                ids = r
            print(ids)
            with open('teacher_id.csv', "w", newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                ids.append(str(sender_id))
                print(ids)
                writer.writerow(ids)
        return 'Готово! Теперь я, наверное, смогу показать ваше расписание))'


def reverse_date(date):
    list_date = list(map(str, date.split('.')))
    print(list_date)
    if len(list_date[0]) == 1:
        list_date[0] = '0' + list_date[0]
    res_date = '.'.join(list_date[::-1])
    return res_date
