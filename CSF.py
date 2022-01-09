#!/usr/bin/env python

# TODO:
# F-ing lot of stuff

from sys import argv
import re

if "--help" in argv or "-h" in argv or len(argv) == 1:
    print("CSF Engine V 0.0.1 by SkaneroOo")

    print("\nUsage:")
    print("\t{} [mode] ... [option | file]".format(argv[0])) # .format, because f-string doesn't allow backslashes

    print("\nAvailable modes:")
    print("\tinter\tInterpretation mode")

    print("\nAvailable options:")
    print("\t--debug\t-d\tDebug mode for interpretation")
    print("\t--help\t-h\tDisplay this message")
    print()
    exit()

argv.pop(0)

iota_counter = 0
src = []
mode = None

debug = "--debug" in argv or "-d" in argv
if "--debug" in argv:
    argv.remove("--debug")
if "-d" in argv:
    argv.remove("-d")


def iota(reset: bool = False):
    global iota_counter
    if reset:
        iota_counter = 0
    iota_counter += 1
    return iota_counter-1

OP_PUSH=iota()
OP_PLUS=iota()
OP_MINUS=iota()
OP_DUMP=iota()
OP_EXIT=iota()
OP_COUNT=iota()

OPS = ("PUSH", "PLUS", "MINUS", "DUMP", "EXIT")

# creating automatically numerated OP codes for exery operation

def tokenize(line: str, i):
    if "#" in line:
        if line[line.index("#")-1] != "\\":
            line = line[:line.index("#")]
    op = line.split()
    # print(op[0])
    assert op[0].upper() in OPS, f"Syntax error at line {i}. Unknown Operation \"{op[0].upper()}\""
    op[0] = OPS.index(op[0].upper())
    if op[0] == OP_PUSH:
        assert len(op) < 3, "Too many arguments for \"PUSH\""
        assert len(op) > 1, "Not enough arguments for \"PUSH\""
        assert op[1].isnumeric() or op[1][1:].isnumeric(), "Invalid value for \"PUSH\""
        op[1] = int(op[1])
    else:
        assert len(op) == 1, f"Too many arguments for \"{op[0]}\""
    return op

def interprete(program, debug=False):
    stack = []
        
    for op in program:
        
        if op[0] == OP_PUSH:
            if debug:
                print("PUSH", op[1])
            stack.append(op[1])
        
        elif op[0] == OP_PLUS:
            if debug:
                print("PLUS")
            assert len(stack) > 1, "Not enough values on stack"
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b)

        elif op[0] == OP_MINUS:
            if debug:
                print("MINUS")
            assert len(stack) > 1, "Not enough values on stack"
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)

        elif op[0] == OP_DUMP:
            if debug:
                print("DUMP")
            print(stack.pop())

        elif op[0] == OP_EXIT:
            if debug:
                print("EXIT")
            exit()

        else:
            assert False, "Not implemented"
    

def compile():
    assert False, "Not implemented"


def readfile(path):
    program = []
    i = 0
    with open(path, "r") as f:
        for line in f:
            i += 1
            if line and not line.strip().startswith("#"):
                program.append(tokenize(line, i))
    return program



if "inter" in argv:
    argv.remove("inter")
    mode = interprete


src = readfile(argv[0])

mode(src, debug)