# Reverse Polish Notation

Utility to compute generic expressions in RPN.

## Installing & Running
The only dependency is Python 3.6+. Copy `rpn.py` somewhere and execute it from
the terminal, e.g.:

```
./rpn.py
```

## Running the Tests

The program comes with a small test suite. Install `pytest` then run:
```
python -m pytest tests
```

## Usage Reference

```
rpn <expr>
rpn      # interactive
rpn      # expr in stdin


Supported operations:

+: Add
-: Subtract
*: Multiply
/: Divide
cla: Clear the stack and variables
clr: Clear the stack
clv: Clear the variables
!: Boolean NOT
!=: Not equal to
%: Modulus
++: Increment
--: Decrement
&: Bitwise AND
|: Bitwise OR
^: Bitwise XOR
~: Bitwise NOT
<<: Bitwise shift left
>>: Bitwise shift right
&&: Boolean AND
||: Boolean OR
^^: Boolean XOR
<: Less than
<=: Less than or equal to
==: Equal to
>: Greater than
>=: Greater than or equal to
acos: Arc Cosine
asin: Arc Sine
atan: Arc Tangent
cos: Cosine
cosh: Hyperbolic Cosine
sin: Sine
sinh: Hyperbolic Sine
tanh: Hyperbolic tangent
tan: tangent
ceil: Ceiling
floor: Floor
round: Round
ip: Integer part
fp: Floating part
sign: Push -1, 0, or 0 depending on the sign
abs: Absolute value
max: Max
min: Min
hex: Switch display mode to hexadecimal
dec: Switch display mode to decimal (default)
bin: Switch display mode to binary
oct: Switch display mode to octal
e: Push e
pi: Push Pi
rand: Generate a random number
exp: Exponentiation
fact: Factorial
sqrt: Square Root
ln: Natural Logarithm
log: Logarithm
pow: Raise a number to a power
hnl: Host to network long
hns: Host to network short
nhl: Network to host long
nhs: Network to host short
pick: Pick the -n'th item from the stack
repeat: Repeat op, e.g. '3 repeat +'
depth: Push the current stack depth
drop: Drops the top item from the stack
dropn: Drops n items from the stack
dup: Duplicates the top stack item
dupn: Duplicates the top n stack items in order
roll: Roll the stack upwards by n
rolld: Roll the stack downwards by n
stack: Toggles stack display from horizontal to vertical
swap: Swap the top 2 stack items
macro: Defines a macro, e.g. 'macro kib 1024 *'
x=: Assigns a variable, e.g. '1024 x=' (can have other names than x)
exit or ctrl+d: exits the calculator
? or help: show this message
```
