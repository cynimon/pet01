import os
import admin_mode


# просмотр юзеров 0 мод - акт юзеры, 1 мод - только неактивные, 2 - все
def watch_users(mode=0):
    users = os.listdir(r'user_base')
    users.sort(key=lambda x: '_nonactive.txt' in x)
    for name in users:
        if mode == 0 and '_nonactive.txt' not in name:
            print(name[:-4], end='; ')
        elif mode == 1 and '_nonactive.txt' in name:
            print(name[:-4], end='; ')
        elif mode == 2:
            print(name[:-4], end='; ')


# просмотр юзеров по конкретному сайту или дате, по месяцу
def watch_any_users_info(item, mode=0):
    users = os.listdir(r'user_base')
    users.sort(key=lambda x: '_nonactive.txt' in x)
    result_info = []
    months = {'1': 'Январь', '2': 'Февраль', '3': 'Март', '4': 'Апрель',
              '5': 'Май', '6': 'Июнь', '7': 'Июль', '8': 'Август',
              '9': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь',
              '12': 'Декабрь'}
    for name in users:
        if '_nonactive.txt' in name:
            break
        with open('user_base\\' + name, encoding='utf-8') as info:
            count = 0
            for line in info:
                if mode != 2 and item in line:
                    result_info.append(name[:-4] + '/' + line)
                    break
                if mode == 2 and '.' + item in line:
                    result_info.append(name[:-4] + '/' + line)
                    count += 1
                    if count >= 2:
                        break
                    item = months[item]
    print('Сотрудник', item, sep='\t')
    for name in result_info:
        print(*name.split('/'), end='')


# выбор режима просмотра общей информации
def watch_info_mode(mode):
    if mode == 0:
        item = input('Введите искомый ресурс: ').title()
        watch_any_users_info(item)
    elif mode == 1:
        item = input('Введите дату зарплаты: ')
        watch_any_users_info(item)
    elif mode == 2:
        item = input('Введите искомый месяц (цифрой от 1 до 12): ')
        watch_any_users_info(item, mode)


def common_info():
    print('Выберите действие: ')
    print('1. Просмотр только активных пользователей\n2. Просмотр неактивных '
          'пользователей\n3. Все сотрудники\n4. Поиск сотрудников по указанному'
          ' ресурсу\n5. Поиск пользователей по дате зарплаты\n6. Просмотр зарплаты'
          ' сотрудников за месяц')
    choice = int(input())
    choices = {1: watch_users, 2: watch_users, 3: watch_users,
               4: watch_info_mode, 5: watch_info_mode, 6: watch_info_mode}
    mode = {1: 0, 2: 1, 3: 2, 4: 0, 5: 1, 6: 2}
    choices[choice](mode[choice])
    key = input('\nПродолжить работу? 1 - да, посмотреть ещё информацию\n'
                '2 - нет, вернуться в меню выбора: ')
    if key == '1':
        common_info()
    elif key == '2':
        admin_mode.admin_start_menu()


# ввод зарплаты всем в одну дату
def input_earnings_to_all():
    date = input('Введите дату в формате ДД.ММ: ')
    users = os.listdir(r'user_base')
    users.sort(key=lambda x: '_nonactive.txt' in x)
    ind = 0
    for i in range(len(users)):
        if '_nonactive.txt' in users[i]:
            ind = i
            break
    users = users[:ind]
    for name in users:
        with open('user_base\\' + name, 'at', encoding='utf-8') as info:
            print(f'Сотрудник {name[:-4]}')
            money = input('Введите сумму: ')
            line = '/'.join((date, money))
            info.write(line + '\n')
    print('Успешно')
    admin_mode.admin_start_menu()