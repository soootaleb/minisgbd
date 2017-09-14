
COLORS = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}

def c(val, color='BOLD'):
    return COLORS[color] + str(val) + COLORS['ENDC']

def cprint(val, color='HEADER'):
    print(c(val, color))