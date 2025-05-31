import datetime
import inspect
import sys
import re
import os
from colorama import Fore, Style, Back, init

init(autoreset=True)

class Type:
    INFO  = f'{Back.BLUE} INFO {Back.RESET}'
    ERROR = f'{Back.RED}{Style.BRIGHT} FAIL {Back.RESET}{Fore.RED}'
    WARN  = f'{Back.YELLOW} WARN {Back.RESET}{Fore.YELLOW}'
    DEBUG = f'{Back.MAGENTA} DEBG {Back.RESET}'

_log_history = []
_log_file = 'latest.log'

try:
    with open(_log_file, 'w'):
        pass
except Exception as e:
    print(f"Error initializing log file: {e}", file=sys.stderr)

def _get_caller_info():
    frame = inspect.stack()[2]
    filename = os.path.basename(frame.filename)
    module_name = os.path.splitext(filename)[0]
    return module_name

def _strip_ansi(text: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def output(message: str, *, end: str = '\n', type: str = Type.INFO):
    now = datetime.datetime.now().strftime('%H:%M:%S')
    module_name = _get_caller_info()

    formatted = f"{Back.GREEN} {now} {Back.CYAN} {module_name} {type} {message} {Style.RESET_ALL}"
    print(formatted, end=end)

    plain_level = _strip_ansi(type)
    log_entry = f"{now} {module_name} {plain_level} {message}"
    _log_history.append(log_entry)

    try:
        with open(_log_file, 'a') as f:
            f.write(log_entry + '\n')
    except Exception as e:
        print(f"Error writing to log: {e}", file=sys.stderr)

