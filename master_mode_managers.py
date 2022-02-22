# создание нового модератора
def create_manager():
    with open('lp_managers.txt', 'a+') as file:
        file.seek(0)
        line = file.readline()
        while line != 'MODS/':
            line = file.readline().rstrip('\n')
        print(line.rstrip('/'))
        line = [li.split('/') for li in file.readlines()]
        for li in line:
            print(li[0])
        login = input('Введите логин модератора: ')
        passw = input('Введите пароль модератора: ')
        print(f'Создаем пользователя:\nЛогин: {login}, пароль: {passw}')
        new_mod = '/'.join((login, passw)) + '\n'
        file.seek(0, 2)
        file.write(new_mod)


# поиск конкретного модератора
def search_manager(file):
    lines = file.readlines()
    ind = lines.index('MODS/\n')
    print(*lines[ind:])
    name = input('Введите логин модератора: ')
    for i in range(len(lines)):
        temp_line = lines[i].strip('\n').split('/')
        if name == temp_line[0]:
            ind = i
            return lines, ind


# изменение пароля у модератора
def edit_manager():
    with open('lp_managers.txt', 'r+') as file:
        lines, ind = search_manager(file)
        changes = lines[ind].rstrip('\n').split('/')
        new_passw = input('Введите новый пароль: ')
        changes[1] = new_passw
        lines[ind] = '/'.join(changes) + '\n'
        file.seek(0)
        print('Пароль успешно изменён')
        file.writelines(lines)


# удаление модератора из базы
def delete_manager():
    with open('lp_managers.txt', 'r+') as file:
        lines, ind = search_manager(file)
        del lines[ind]
        file.seek(0)
        print('Пользователь удалён')
        file.writelines(lines)
