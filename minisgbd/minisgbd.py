from helpers import *
import importlib

commands = importlib.import_module('commands')

cprint('Welcome on MiniSGBD')

while True:
    cprint('What to you want to do ? (help for commands list)', 'OKGREEN')
    user_input = input().strip()
    try:
        command = user_input[:user_input.index(' ')]
        params = user_input[user_input.index(' ') + 1:].split(' ')
    except:
        command = user_input
        params = []
    if command == 'exit':
        exit()
    elif command in dir(commands):
        if len(params) > 0:
            getattr(commands, command)(params)
        else:
            getattr(commands, command)()
    else:
        cprint('Sorry, unknown command', 'FAIL')

cprint('Bye bye !')