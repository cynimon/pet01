import os
import sys
import master_mode
import admin_edit_user
import admin_tables_view
import admin_creating_user


def admin_start_menu():
    print('Выберите действие:')
    menu = '1. Создание пользователя\n2. Просмотр/редактирование пользователя\n' \
           '3. Деактивация пользователя\n4. Сводная информация\n' \
           '5. Ввод зарплаты\n6. Выход'
    print(menu)
    choice = int(input('Введите номер действия: '))
    while choice not in [1, 2, 3, 4, 5, 6]:
        print(menu)
        choice = int(input('Введите число от 1 до 6: '))
    choice_dict = {1: admin_creating_user.create_user,
                   2: admin_edit_user.check_user, 3: admin_edit_user.deactive_user,
                   4: admin_tables_view.common_info,
                   5: admin_tables_view.input_earnings_to_all, 6: sys.exit}
    choice_dict[choice]()


def admin_start(name):
    print(f'Приветствуем, {name}!')
    if name == 'admin':
        key = input('Это режим для редактирования обычных пользователей системы.\n'
                    'Если вам нужны модераторы, нажмите 1, если вы хотите продолжить, нажмите 2: ')
        if key == '1':
            master_mode.master_menu()
        else:
            pass
    admin_start_menu()
    key = input('\nВыберите действие:\n'
                '1. Продолжить работу\n'
                '2. Зайти как другой пользователь\n'
                '3. Завершить работу\n')
    if key == '1':
        admin_start_menu()
    elif key == '2':
        os.execl(sys.executable, 'python', 'main.py')
    elif key == '3':
        sys.exit()
