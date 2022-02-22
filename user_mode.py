import os


# чтение из файла в виде словаря и вывод
def read_to_dict(line, file):
    temp = []
    while line != '':
        line = file.readline().rstrip()
        temp.append(line.split('/'))
    temp_dict = {li[0]: tuple(li[1:]) for li in temp[:-1]}
    for key, values in temp_dict.items():
        print(key, *values, sep='\t')
    return temp_dict


# чтение только заработка
def read_money(temp_name):
    with open(temp_name, encoding='utf-8') as file:
        line = file.readline().rstrip()
        while line != 'Заработок':
            line = file.readline().rstrip()
        print(line)
        temp_dict = read_to_dict(line, file)
        return temp_dict


# чтение только инфо о доступах
def read_access(temp_name):
    with open(temp_name, encoding='utf-8') as file:
        line = file.readline().rstrip()
        print(line)
        temp_dict = read_to_dict(line, file)
        return temp_dict


# access = 0 это показать всё инфо о сотруднике,
# доступы и зарплату, 1 - только доступы, 2 = только зп
def check_info(name, access=0):
    temp_name = os.path.join('user_base', name + '.txt')
    if access == 0:
        read_access(temp_name)
        read_money(temp_name)
    elif access == 1:
        read_access(temp_name)
    elif access == 2:
        read_money(temp_name)


# открывает файл с заметками
def open_notes(name):
    temp = os.path.join('user_notes', name + '.txt')
    os.startfile(temp)


# выбор действия пользователем
def user_menu(name):
    print('Выберите действие:')
    print('1. Открыть всю доступную информацию и заметки')
    print('2. Открыть только доступную информацию')
    print('3. Открыть только информацию по доступам к ресурсам')
    print('4. Открыть только информацию по зарплате')
    print('5. Открыть только заметки')
    key = input('Введите номер действия: ')
    if key == '1':
        return check_info(name), open_notes(name), False
    elif key == '2':
        return check_info(name), False
    elif key == '3':
        return check_info(name, 1), False
    elif key == '4':
        return check_info(name, 2), False
    elif key == '5':
        return open_notes(name), False
    else:
        return print('Введите число от 1 до 5'), True


# выбор режима - открыть только био, только заметки, всё вместе - дефолт
def user_start(name):
    print('Приветствуем!')
    flag = True
    while flag:
        *result, flag = user_menu(name)
    again = input('Требуется ли что-то ещё? 1 - да, '
                  '2 - нет, выйти ')
    if again == '1':
        user_start(name)
    else:
        return
