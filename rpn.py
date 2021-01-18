#!/usr/bin/env python

import math
import os
import re
import sys

from os.path import expanduser
from random import random
from math import (cos, sin, tan, acos, asin, atan, sinh, cosh,
                  tanh, floor, ceil, factorial, log, log10, sqrt)
from socket import htons, htonl, ntohs, ntohl


OPS = {
      '+': (lambda a, b: a + b, 2, "Add"),
      '-': (lambda a, b: a - b, 2, "Subtract"),
      '*': (lambda a, b: a * b, 2, "Multiply"),
      '/': (lambda a, b: a / b, 2, "Divide"),
      'cla': ('_cla', 0, "Clear the stack and variables"),
      'clr': ('_clr', 0, "Clear the stack"),
      'clv': ('_clv', 0, "Clear the variables"),
      '!': (lambda x: not x, 1, "Boolean NOT"),
      '!=': (lambda a, b: a != b, 2, "Not equal to"),
      '%': (lambda a, b: a % b, 2, "Modulus"),
      '++': (lambda x: x + 1, 1, "Increment"),
      '--': (lambda x: x - 1, 1, "Decrement"),
      '&': (lambda a, b: a & b, 2, "Bitwise AND"),
      '|': (lambda a, b: a | b, 2, "Bitwise OR"),
      '^': (lambda a, b: a ^ b, 2, "Bitwise XOR"),
      '~': (lambda x: ~x, 1, "Bitwise NOT"),
      '<<': (lambda x: x << 1, 1, "Bitwise shift left"),
      '>>': (lambda x: x >> 1, 1, "Bitwise shift right"),
      '&&': (lambda a, b: a and b, 2, "Boolean AND"),
      '||': (lambda a, b: a or b, 2, "Boolean OR"),
      '^^': (lambda a, b: (a and not b) or (not a and b), 2, "Boolean XOR"),
      '<': (lambda a, b: a < b, 2, "Less than"),
      '<=': (lambda a, b: a <= b, 2, "Less than or equal to"),
      '==': (lambda a, b: a == b, 2, "Equal to"),
      '>': (lambda a, b: a > b, 2, "Greater than"),
      '>=': (lambda a, b: a >= b, 2, "Greater than or equal to"),
      'acos': (lambda x: acos(x), 1, "Arc Cosine"),
      'asin': (lambda x: asin(x), 1, "Arc Sine"),
      'atan': (lambda x: atan(x), 1, "Arc Tangent"),
      'cos': (lambda x: cos(x), 1, "Cosine"),
      'cosh': (lambda x: cosh(x), 1, "Hyperbolic Cosine"),
      'sin': (lambda x: sin(x), 1, "Sine"),
      'sinh': (lambda x: sinh(x), 1, "Hyperbolic Sine"),
      'tanh': (lambda x: tanh(x), 1, "Hyperbolic tangent"),
      'tan': (lambda x: tan(x), 1, "tangent"),
      'ceil': (lambda x: ceil(x), 1, "Ceiling"),
      'floor': (lambda x: floor(x), 1, "Floor"),
      'round': (lambda x: round(x), 1, "Round"),
      'ip': (lambda x: int(x), 1, "Integer part"),
      'fp': (lambda x: x - int(x), 1, "Floating part"),
      'sign': (lambda x: int(x/abs(x)) if x != 0 else 0, 1,
               "Push -1, 0, or 0 depending on the sign"),
      'abs': (lambda x: abs(x), 1, "Absolute value"),
      'max': (lambda a, b: max(a, b), 2, "Max"),
      'min': (lambda a, b: min(a, b), 2, "Min"),
      'hex': ('_hexmode', 0, "Switch display mode to hexadecimal"),
      'dec': ('_decmode', 0, "Switch display mode to decimal (default)"),
      'bin': ('_binmode', 0, "Switch display mode to binary"),
      'oct': ('_octmode', 0, "Switch display mode to octal"),

      'e': (lambda: math.e, 0, "Push e"),
      'pi': (lambda: math.pi, 0, "Push Pi"),
      'rand': (lambda: random(), 0, "Generate a random number"),

      'exp': (lambda a, b: pow(a, b), 2, "Exponentiation"),
      'fact': (lambda x: factorial(x), 1, "Factorial"),
      'sqrt': (lambda x: sqrt(x), 1, "Square Root"),
      'ln': (lambda x: log(x), 1, "Natural Logarithm"),
      'log': (lambda x: log10(x), 1, "Logarithm"),
      'pow': (lambda a, b: pow(b, a), 2, "Raise a number to a power"),

      'hnl': (lambda x: htonl(x), 1, "Host to network long"),
      'hns': (lambda x: htons(x), 1, "Host to network short"),
      'nhl': (lambda x: ntohl(x), 1, "Network to host long"),
      'nhs': (lambda x: ntohs(x), 1, "Network to host short"),

      'pick': ('_stkidx', 1, "Pick the -n'th item from the stack"),
      'repeat': ('_repeat', 1, "Repeat op, e.g. '3 repeat +'"),
      'depth': ('_depth', 0, "Push the current stack depth"),
      'drop': ('_drop', 0, "Drops the top item from the stack"),
      'dropn': ('_drop', 1, "Drops n items from the stack"),
      'dup': ('_dup', 0, "Duplicates the top stack item"),
      'dupn': ('_dup', 1, "Duplicates the top n stack items in order"),
      'roll': ('_rollup', 1, "Roll the stack upwards by n"),
      'rolld': ('_rolldown', 1, "Roll the stack downwards by n"),
      'stack': ('_stktoggl', 0,
                "Toggles stack display from horizontal to vertical"),
      'swap': ('_stkswap', 0, "Swap the top 2 stack items"),
}


def _ensure_arg1_int(f):
    def inner(*args, **kwargs):
        if type(args[1]) is not int:
            raise Exception('Integer argument required')
        return f(*args, **kwargs)
    return inner


class Engine:
    def __init__(self):
        self.stack = []
        self.vars = {}
        self.macros = {}
        self.mode = 'dec'
        self.stkhorizontal = True
        self._nrepeat = 1

    def display(self):
        int2str = {
            'dec': lambda n: str(n),
            'oct': lambda n: oct(n),
            'bin': lambda n: bin(n),
            'hex': lambda n: '0x%x' % n,
        }[self.mode]
        sep = ' ' if self.stkhorizontal else '\n'
        return sep.join([int2str(x) if type(x) is int else str(x)
                         for x in self.stack])

    def result(self):
        return self.stack[-1]

    def evaluate(self, expr):

        for macro, expansion in self.macros.items():
            expr = re.sub(r'\b' + macro + r'\b', ' %s ' % expansion, expr)

        parts = re.split(r'\s+', expr.strip())

        if parts[0] == 'macro':
            name = parts[1]
            self.macros[name] = ' '.join(parts[2:])
            return 0

        stack0 = self.stack[:]
        for part in parts:
            try:
                if self._nrepeat > 1:
                    for _ in range(self._nrepeat - 1):
                        self._evaluate_part(part)
                    self._nrepeat = 1
                self._evaluate_part(part)
            except Exception as e:
                sys.stderr.write('Error: %s\n' % e)
                self.stack = stack0
                return 1
        return 0

    def _evaluate_part(self, part):

        if part.endswith('='):
            if len(self.stack) == 0:
                raise Exception('No value to assign')
            name = part[:-1]
            self.vars[name] = self.stack[-1]
            return

        val = self._try_literal(part)
        if val is not None:
            self.stack.append(val)
            return
        info = OPS.get(part)
        if not info:
            raise Exception('Unsupported operation: %s' % part)
        func, nargs, _ = info
        if len(self.stack) < nargs:
            raise Exception(
                'Insufficient operands: %d required for %s' % (nargs, part))

        if type(func) is str:
            try:
                func = getattr(self, func)
            except AttributeError:
                raise Exception('Invalid op %s' % func)

        args = [self.stack.pop() for _ in range(nargs)]
        try:
            result = func(*args[::-1])
        except ZeroDivisionError:
            raise Exception('Division by zero!')
        except TypeError:
            raise Exception(
                'The operation is not compatible with the operands')
        if result is not None:
            self.stack.append(result)

    def _try_literal(self, part):

        val = self.vars.get(part)
        if val is not None:
            return val

        base = 10
        if part.startswith('0x'):
            base = 16
        elif part.startswith('0b'):
            base = 2
        elif part.startswith('0'):
            base = 8
        try:
            val = int(part, base)
        except ValueError:
            val = None

        if val is not None:
            return val

        try:
            val = float(part)
        except ValueError:
            val = None

        return val

    def _cla(self):
        self.stack = []
        self.vars = {}

    def _clr(self):
        self.stack = []

    def _clv(self):
        self.vars = {}

    def _hexmode(self):
        self.mode = 'hex'

    def _decmode(self):
        self.mode = 'dec'

    def _octmode(self):
        self.mode = 'oct'

    def _binmode(self):
        self.mode = 'bin'

    def _stktoggl(self):
        self.stkhorizontal = not self.stkhorizontal

    @_ensure_arg1_int
    def _stkidx(self, i):
        return self.stack[-i-1]

    def _depth(self):
        return len(self.stack)

    @_ensure_arg1_int
    def _drop(self, n=1):
        [self.stack.pop() for _ in range(n)]

    @_ensure_arg1_int
    def _dup(self, n=1):
        self.stack += self.stack[-n:]

    def _stkswap(self):
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

    @_ensure_arg1_int
    def _repeat(self, n):
        self._nrepeat = n

    @_ensure_arg1_int
    def _rollup(self, n):
        if len(self.stack) == 0:
            return
        n %= len(self.stack)
        self.stack = self.stack[-n:] + self.stack[:-n]

    @_ensure_arg1_int
    def _rolldown(self, n):
        if len(self.stack) == 0:
            return
        n %= len(self.stack)
        self.stack = self.stack[n:] + self.stack[:n]


def clearscreen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def showhelp():
    print('''Reverse Polish Notation calculator. Usage:
rpn <expr>
rpn      # interactive
rpn      # expr in stdin''')
    print('\n\nSupported operations:\n')
    print('\n'.join(('%s: %s' % (op, info[2]) for op, info in OPS.items())))
    print('''macro: Defines a macro, e.g. 'macro kib 1024 *'
x=: Assigns a variable, e.g. '1024 x=' (can have other names than x)
exit or ctrl+d: exits the calculator
? or help: show this message''')


def main():
    engine = Engine()

    try:
        with open(expanduser('~/.rpnrc')) as f:
            init = f.read()
            engine.evaluate(init)
    except FileNotFoundError:
        pass

    expr = None
    if len(sys.argv) > 1:
        expr = ' '.join(sys.argv[1:])
    elif not sys.stdin.isatty():
        expr = sys.stdin.read()

    if expr:
        status = engine.evaluate(expr)
        if status == 0:
            print(engine.result())
        sys.exit(status)

    while True:
        vals = engine.display()
        if vals:
            vals += ' '
        print('%s>> ' % vals, end='')
        try:
            expr = input()
        except EOFError:
            print('')
            break
        if expr.lower() == 'exit':
            break
        if expr.lower() == 'clear':
            clearscreen()
            continue
        if expr.lower() in ('help', '?'):
            showhelp()
            continue

        engine.evaluate(expr)


if __name__ == '__main__':
    main()
