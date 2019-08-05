# Shreepa Parthaje

Colors = {
    'ARDUINO': '\033[95m',
    'PYTHON': '\033[94m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'SUCCESS': '\033[92m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
}


def log(content, color):
    print(f'{Colors[color]}{color}: {content}' + '\033[0m')
