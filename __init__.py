from __future__ import print_function

import sys
import re
import collections

from . import g, terminalsize

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

Command = collections.namedtuple('Command', 'regex function')
InitCommand = collections.namedtuple('InitCommand', 'function')


def initcommand():
    def decorator(function):
        cmd = InitCommand(function)
        g.init_commands.append(cmd)
        return function

    return decorator


def command(regex):
    def decorator(function):
        cmd = Command(re.compile(regex), function)
        g.commands.append(cmd)
        return function

    return decorator

ansirx = re.compile(r'\x1b\[\d*m', re.UNICODE)

def stripansi(s):
    return ansirx.sub('', s)


class PyMenu(object):
    def __init__(self):
        pass

    def _match_function(self, func, regex, userinput):
        match = regex.match(userinput)
        if match and match.group(0) == userinput:
            matches = match.groups()
            try:
                func(*matches)
            except IndexError:
                print('invalid range')
            except (ValueError, IOError) as e:
                print('value or IO error: {}'.format(str(e)))

            return True

    def update(self, text):
        if g.message:
            sys.stdout.write(g.message)
        if text:
            sys.stdout.write(text)

    def clear(self):
        if g.clear_every_print:
            print('\n' * 200)
        if g.clear_on_load and g.cleared_on_load:
            print('\n' * 200)

    def centrify(self, text):
        lines = text.split('\n')
        numlines = len(lines)
        length = max(len(stripansi(x)) for x in lines)
        x, y = terminalsize.get_terminal_size()
        indent = (x - length) // 2
        newlines = (y) // 2 - (numlines // 2)
        lines = [' ' * indent + L for L in lines]
        text = '\n' * 200 + '\n'.join(lines) + '\n' * newlines
        return text

    def print(self, text):
        self.clear()
        self.update(text)

    def set_prompt(self, newprompt):
        g.prompt = newprompt

    def run(self):
        if g.clear_on_load:
            print('\n' * 200)

        for c in g.init_commands:
            c.function()

        while True:
            try:
                if PY2:
                    userinput = raw_input(g.prompt).strip()
                elif PY3:
                    userinput = input(g.prompt).strip()
            except (KeyboardInterrupt, EOFError):
                sys.exit(0)
            for c in g.commands:
                if self._match_function(c.function, c.regex, userinput):
                    break
