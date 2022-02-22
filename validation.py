# нахождение логин в базе, вытаскиваем связку лог/пасс
def find_login(login):
    with open('lp_managers.txt', 'rt', encoding='utf-8') as managers, \
            open('lp_users.txt', 'rt', encoding='utf-8') as users:
        for line in managers:
            log = line.rstrip().split('/')
            if login in log:
                return log, 0, True
        for line in users:
            log = line.rstrip().split('/')
            if login in log:
                return log, 1, True
    return 'Такого пользователя не существует или ошибка ввода, попробуйте ещё раз', False


# проверка связки лог/пасс
def valid(temp, password):
    logs, acss = temp
    if logs[-1] == password:
        print('Доступ предоставлен')
        if logs[0] == 'admin':
            return logs[0], 0, True
        elif logs[0] != 'admin' and acss == 0:
            return logs[0], 1, True
        elif acss == 1:
            return logs[0], 2, True
    else:
        return 'Неверный пароль', False


# проверка валидности лог/пасс и присвоение прав доступа
# (0 = главный админ, 1 = модераторы, 2 = юзеры)
def start(login, password):
    *temp, flag_log = find_login(login)
    while not flag_log:
        print(*temp)
        login = input('Введите логин: ')
        *temp, flag_log = find_login(login)
    *temp_data, flag_pass = valid(temp, password)
    while not flag_pass:
        print(*temp_data)
        password = input('Введите пароль: ')
        *temp_data, flag_pass = valid(temp, password)
    return temp_data
