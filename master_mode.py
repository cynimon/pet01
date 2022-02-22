import os
import sys
import admin_mode
import admin_tables_view
import admin_edit_user
import master_mode_managers


# изменение пароля мастер-админа
def edit_own_password():
    with open('lp_managers.txt', 'r+') as output:
        temp_line = output.readline()
        line = output.readline().split('/')
        temp_file = output.read()
        passw = input('Введите новый пароль: ')
        print(f'Ваш пароль: {passw}, запомните его и никому не сообщайте')
        line[1] = passw + '\n'
        line = '/'.join(line)
        temp_line += line + temp_file
        output.seek(0)
        output.write(temp_line)


# удаление из текстовой базы логпассов
def delete_user_from_base(name):
    with open('lp_users.txt', 'r', encoding='utf-8') as file:
        file.seek(0)
        lines = file.readlines()
        for i in range(len(lines)):
            if name + '_nonactive' in lines[i]:
                ind = i
                break
    with open('lp_users.txt', 'w', encoding='utf-8') as file:
        del lines[ind]
        file.seek(0)
        file.writelines(lines)


# удаление одного юзера из базы
def delete_user():
    admin_tables_view.watch_users(2)
    name = input('Введите имя пользователя: ').title()
    if not admin_edit_user.check_user_in_base(name + '_nonactive'):
        delete_user()
    else:
        os.remove('user_base\\' + name + '_nonactive.txt')
        os.remove('user_notes\\' + name + '_nonactive.txt')
        delete_user_from_base(name)
        option = input('Удалить ещё пользователя? Да/Нет ').lower()
        if option == 'да':
            delete_user()


# сброс всей базы по дефолту
def clean_full_base():
    print('ВНИМАНИЕ: Будут удалены все данные пользователей системы, '
          'все пользователи и модераторы системы. Если вы уверены, нажмите 1')
    key = input()
    if key != '1':
        return
    else:
        notes = os.listdir(r'user_notes')
        for name in notes:
            os.remove('user_base\\' + name)
            os.remove('user_notes\\' + name)
        with open('lp_users.txt', 'w', encoding='utf-8') as file:
            file.write('Имя/Логин/Пароль\n')
        with open('lp_managers.txt', 'w') as file:
            file.write('ADMINS/\nadmin/admin\n\nMODS/\n')
    sys.exit()


# проверка первого вхождения в систему
def first_time_checking():
    with open('lp_managers.txt', encoding='utf-8') as file:
        file.readline()
        line = file.readline()
        if line == 'admin/admin\n':
            print('Ваш пароль установлен по умолчанию.'
                  'Советуем поменять пароль. Сменить? Да/Нет')
            answer = input().lower()
            if answer == 'да':
                return True
        else:
            return False


def master_menu():
    print('Выберите действие: ')
    choice = input('1. Создать нового модератора\n2. Редактировать пароль'
                   ' модератора\n3. Редактировать свой пароль\n4. Удалить'
                   ' модератора\n5. Удалить пользователя\n6. Очистить всю базу\n'
                   '7. Выход\n')
    choices = {'1': master_mode_managers.create_manager, '2': master_mode_managers.edit_manager,
               '3': edit_own_password, '4': master_mode_managers.delete_manager, '5': delete_user,
               '6': clean_full_base}
    if choice == '7':
        return
    choices[choice]()
    master_menu()


def master_start(name):
    print(f'Приветствуем {name}!')
    if first_time_checking():
        edit_own_password()
        master_start(name)
    else:
        print('Войти как: ')
        mode = input('1. Главный админ\n2. Модератор\n')
        if mode == '1':
            master_menu()
            master_start(name)
        elif mode == '2':
            admin_mode.admin_start(name)
