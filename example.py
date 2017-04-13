from pymenu import *

logo = '''88d888b. dP    dP 88d8b.d8b. .d8888b. 88d888b. dP    dP
88'  `88 88    88 88'`88'`88 88ooood8 88'  `88 88    88
88.  .88 88.  .88 88  88  88 88.  ... 88    88 88.  .88
88Y888P' `8888P88 dP  dP  dP `88888P' dP    dP `88888P'
88            .88
dP        d8888P                          {}'''.format('')

help_text = '''
usage: pymenu [-h] [-d] [commands [commands ...]]
positional arguments:
  commands
optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  turn debugging on'''

m = PyMenu()


@initcommand()
def do_this_first():
    print(m.centrify(logo))


@initcommand()
def do_this_next():
    print('Enter [help] to get help')


@command(r'help|h')
def _helpfunc():
    print(help_text)


@command(r'quit|exit|q')
def _quit():
    """ Exit the program """
    sys.exit('Goodbye')


@command(r'clear|cls|c')
def _clear():
    print('\n' * 200)


@command(r'(download|d)\s*(\d{1,4})')
def _download(_type, num):
    print('Downloading item number {}'.format(num))


class Cat(object):
    def __init__(self):
        cattext = '''     /\\
 )  ( ')
(  /  )
 \(__)|'''
        print(m.centrify(cattext))
        print('A wild cat appears.')

    def meow(self):
        print('Meow.')


cat = None


@command(r'cat')
def _cat():
    global cat
    cat = Cat()


@command(r'meow')
def _meow():
    if cat is not None:
        cat.meow()


m.set_prompt('> ')
m.run()
