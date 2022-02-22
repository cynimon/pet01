import sys
import validation as vl
import user_mode
import admin_mode
import master_mode

login = input('Введите логин: ').lower()
password = input('Введите пароль: ')

name, mode = vl.start(login, password)

mode_dict = {0: master_mode.master_start, 1: admin_mode.admin_start, 2: user_mode.user_start}

mode_dict[mode](name)

sys.exit()
