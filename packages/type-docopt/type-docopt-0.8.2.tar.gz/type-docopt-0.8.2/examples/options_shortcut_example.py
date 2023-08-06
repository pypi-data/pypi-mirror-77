"""Example of program which uses [options] shortcut in pattern.

Usage:
  options_shortcut_example.py [options] <port>

Options:
  -h --help                show this help message and exit
  --version                show version and exit
  -n, --number N           use N as a number [type: int]
  -t, --timeout TIMEOUT    set timeout TIMEOUT seconds [type: float]
  --apply                  apply changes to database
  -q                       operate in quiet mode

"""
from type_docopt import docopt


if __name__ == "__main__":
    arguments = docopt(__doc__, version="1.0.0rc2")
    print(arguments)
