import shutil
import user_mode
import admin_edit_user


# проверка ввода логина - требования
def login_input(login):
    if (len(login) >= 4) and (not login.isalpha() and not login.isdigit()):
        return True
    else:
        return False


# проверка ввода пароля - требования
def passw_input(password):
    if len(password) >= 6 and (not password.isalpha() and not password.isdigit()):
        return False, 'Пароль принят'
    else:
        return True, 'Некорректный пароль, введите другой'


# проверка наличия этого имени в базе
def name_check(name):
    with open('lp_users.txt', encoding='utf-8') as names:
        temp = '  '
        while len(temp) != 1:
            temp = names.readline().split('/')
            if name == temp[0]:
                return True, 'Имя уже занято, введите другое'
        return False, 'Имя принято'


# проверка наличия логина в базе и его требований
def login_check(login):
    with open('lp_users.txt', encoding='utf-8') as logins:
        temp = '  '
        if login_input(login):
            while len(temp) != 1:
                temp = logins.readline().split('/')
                if login in temp:
                    return False, 'Логин уже занят, введите другой'
        else:
            return False, 'В логине должно быть более 4х символов: буквы и цифры'
        return True, 'Логин принят'


# ввод данных нового юзера, отправка на проверку данных юзера в базе
def user_info_input_check():
    flag = True
    name, login, password = 0, 0, 0
    while flag:
        name = input('Введите имя пользователя: ').title()
        flag, msg = name_check(name)
        print(msg)
    while not flag:
        login = input('Введите логин пользователя: ').lower()
        flag, msg = login_check(login)
        print(msg)
    while flag:
        password = input('Введите пароль пользователя: ').lower()
        flag, msg = passw_input(password)
        print(msg)
    print(f'Имя пользователя: {name}\nЛогин пользователя: {login}\n'
          f'Пароль пользователя: {password}\nВерно?\n1. Да\n2. Ввести заново')
    choice = int(input('Выбор: '))
    if choice == 2:
        create_user()
    return name, login, password


# ввод данных и запись новых данных в файл
def input_access_info(user_info):
    site = input('Введите название ресурса: ').title()
    login = input('Введите логин пользователя: ')
    password = input('Введите пароль пользователя: ')
    temp_info = '/'.join((site, login, password)) + '\n\n'
    with open('user_base\\' + user_info + '.txt', 'r', encoding='utf-8') as info:
        line = info.readline()
        temp_line = ''
        while line != '\n':
            temp_line += line
            line = info.readline()
        temp_line += temp_info
        line = info.read()
        temp_line += line
    with open('user_base\\' + user_info + '.txt', 'w', encoding='utf-8') as info:
        info.write(temp_line)
    choice = input('Добавить ещё один ресурс? 1 - да, 2 - нет ')
    return choice


# вывод старых данных, обновление, вывод новых данных
def edit_user_info(user_info):
    user_mode.check_info(user_info, 1)
    print(f'Добавление информации для {user_info}')
    key = input_access_info(user_info)
    while key == '1':
        input_access_info(user_info)
    print('Результат: ')
    user_mode.check_info(user_info, 1)

# создание юзера - ввод имя, лог, пасс
def create_user():
    print('Логин и пароль должны состоять из букв и чисел, '
          'длина логина - от 4 символов, длина пароля - от 6 символов')
    user_info = user_info_input_check()
    user = '/'.join(user_info) + '\n'
    # добавление юзера в базу и создание его персональных файлов
    with open('lp_users.txt', 'a', encoding='utf-8') as outputs:
        outputs.write(user)
    path = user_info[0] + '.txt'
    user_file = open('user_notes\\' + path, 'wt')
    user_file.close()
    shutil.copyfile('_template.txt', 'user_base\\' + path)
    print('Добавить ещё одного пользователя?\n1. Да\n'
          '2. Перейти к добавлению информации о пользователе')
    choice = int(input('Выбор: '))
    if choice == 1:
        create_user()
    elif choice == 2:
        edit_user_info(user_info[0])
    return
