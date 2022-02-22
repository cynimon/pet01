import os
import user_mode
import admin_mode
import admin_creating_user
import admin_tables_view
from datetime import datetime


# проверка наличия юзера в базе
def check_user_in_base(name):
    files = os.listdir(r'user_base')
    if name + '.txt' in files:
        return True
    else:
        print('Что-то пошло не так, попробуйте ещё раз')
        return False


# замена пароля пользователя на доступ к базе
def change_sys_password(name):
    with open('lp_users.txt', 'r+', encoding='utf-8') as users:
        lines = users.readlines()
        for i in range(len(lines)):
            temp_line = lines[i].split('/')
            if name == temp_line[0]:
                temp_passw = input('Введите новый пароль: ')
                while not admin_creating_user.passw_input(temp_passw):
                    temp_passw = input('Введите новый пароль: ')
                temp_line[2] = temp_passw
                lines[i] = '/'.join(temp_line) + '\n'
                break
        users.seek(0)
        users.writelines(lines)
        return


# редактирует информацию логпассы в нужных сайтах и суммы в зп
# 1 - логпасс, 2 - зп
def write_newinfo(info_dict, name_user, mode):
    with open('user_base\\' + name_user + '.txt', 'r', encoding='utf-8') as wrfile:
        lines = wrfile.readlines()
        temp_line = []
        if mode == 1:
            info_line = sorted(info_dict.items(), reverse=True)
            for key, values in info_line:
                temp_line.append('/'.join((key, '/'.join(values))) + '\n')
            for i in range(1, len(temp_line) + 1):
                lines[i] = temp_line[i - 1]
        elif mode == 2:
            earn_line = sorted(info_dict.items(),
                               key=lambda x: datetime.strptime(x[0], '%d.%m'))
            for value in earn_line:
                temp_line.append('/'.join(value) + '\n')
            ind = lines.index('Заработок\n')
            for i in range(ind + 2, len(temp_line) + ind + 2):
                lines[i] = temp_line[i - ind - 2]
    with open('user_base\\' + name_user + '.txt', 'w', encoding='utf-8') as wrfile:
        wrfile.seek(0)
        wrfile.writelines(lines)
        return


# редактируем логинпароли
def edit_logpass(name):
    name_read = os.path.join('user_base', name + '.txt')
    logpass_dict = user_mode.read_access(name_read)
    site = input('Какой ресурс требует изменений? ').title()
    login = input('Введите новый логин: ')
    passw = input('Введите новый пароль: ')
    logpass_dict[site] = (login, passw)
    write_newinfo(logpass_dict, name, mode=1)
    return


# редактируем зарплату
def edit_earnings(name):
    name_read = os.path.join('user_base', name + '.txt')
    earnings_dict = user_mode.read_money(name_read)
    if len(earnings_dict) == 1:
        print('У сотрудника пока что не было зарплаты')
        return
    data = input('Введите дату корректировки: ')
    summa = input('Введите новую сумму: ')
    earnings_dict[data] = summa
    del earnings_dict['Дата']
    write_newinfo(earnings_dict, name, mode=2)
    return


def whats_next():
    key = input('Продолжить редактировать пользователя? 1 - да, 2 - нет, '
                '3 - работа с другим пользователем ')
    return key


# выбор действий для изменения пользователя
def change_exist_user(name):
    key_u = int(input('Выберите действие:\n1. Изменить пароль доступа в систему\n'
                      '2. Добавить новый ресурс\n3. Редактировать логин/пароль в'
                      ' существующем ресурсе\n4. Редактировать зарплату\n'))
    choices = {1: change_sys_password, 2: admin_creating_user.edit_user_info,
               3: edit_logpass, 4: edit_earnings}
    choices[key_u](name)
    key = whats_next()
    if key == '1':
        change_exist_user(name)
    elif key == '2':
        return
    else:
        check_user()


def check_user():
    admin_tables_view.watch_users()
    name = input('\nВведите пользователя: ').title()
    if not check_user_in_base(name):
        check_user()
    else:
        choice = input('Выберите действие:\n1. Просмотр пользователя\n'
                       '2. Редактирование пользователя\n')
        if choice == '1':
            user_mode.user_start(name)
        elif choice == '2':
            change_exist_user(name)
        return


# делает юзера неактивным в базе пользователей
def deactivate_user_from_base(name):
    with open('lp_users.txt', 'r', encoding='utf-8') as file:
        file.seek(0)
        lines = file.readlines()
        for i in range(len(lines)):
            if name in lines[i]:
                temp = lines[i].split('/')
                temp[0] = name + '_nonactive'
                lines[i] = '/'.join(temp) + '\n'
                break
    with open('lp_users.txt', 'w', encoding='utf-8') as file:
        file.seek(0)
        file.writelines(lines)


# переносит юзера в неактивных
def deactive_user():
    name = input('Введите имя пользователя: ').title()
    if not check_user_in_base(name):
        deactive_user()
    else:
        os.rename('user_base\\' + name + '.txt', 'user_base\\' + name + '_nonactive.txt')
        os.rename('user_notes\\' + name + '.txt', 'user_notes\\' + name + '_nonactive.txt')
        deactivate_user_from_base(name)
        admin_mode.admin_start_menu()
