#!/usr/bin/env python3
#Michael ORTEGA - 09 jan 2018

###############################################################################
## Global libs
import sys
import socket
import keyboard

###############################################################################
## Global vars
GREEN       = '\033[92m'
WHITE       = '\x1b[0m'
BLUE        = '\033[94m'
YELLOW      = '\033[93m'
RED         = '\033[91m'

stop        = False
DEBUG       = False

address     = ('localhost', 6006)
sock        = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)

#list of tuples: (received command, keyboard key, keyboard func )
bindings    = [ ['UP', 'up', keyboard.press_and_release],
                ['DOWN', 'down', keyboard.press_and_release],
                ['LEFT', 'left', keyboard.press_and_release],
                ['RIGHT', 'right', keyboard.press_and_release],
                ['SELECT', 'enter', keyboard.press_and_release],
                ['CANCEL', 'backspace', keyboard.press_and_release],
                ['BACK', 'backspace', keyboard.press_and_release],
                ['P_FIRE', 'space', keyboard.press],
                ['R_FIRE', 'space', keyboard.release],
                ['NITRO', 'n', keyboard.press_and_release],
                ['P_SKIDDING', 'v', keyboard.press],
                ['R_SKIDDING', 'v', keyboard.release],
                ['P_LOOKBACK', 'b', keyboard.press],
                ['R_LOOKBACK', 'b', keyboard.release],
                ['P_RESCUE', 'backspace', keyboard.press],
                ['R_RESCUE', 'backspace', keyboard.release],
                ['PAUSE', 'escape', keyboard.press_and_release],
                ['P_UP', 'up', keyboard.press],
                ['R_UP', 'up', keyboard.release],
                ['P_DOWN', 'down', keyboard.press],
                ['R_DOWN', 'down', keyboard.release],
                ['P_LEFT', 'left', keyboard.press],
                ['R_LEFT', 'left', keyboard.release],
                ['P_RIGHT', 'right', keyboard.press],
                ['R_RIGHT', 'right', keyboard.release],
                ['P_ACCELERATE', 'up', keyboard.press],
                ['R_ACCELERATE', 'up', keyboard.release],
                ['P_BRAKE', 'down', keyboard.press],
                ['R_BRAKE', 'down', keyboard.release]
                ]

commands = [b[0] for b in bindings]

###############################################################################
## Main
if len(sys.argv) > 1:
    # Reading command line
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-d':
            DEBUG = True

print()
print('STK input server started ', end='')
if DEBUG:   print(GREEN+'(Debug mode)'+WHITE)
else:       print()

while (not stop):
    data, addr = sock.recvfrom(1024)
    if type(data) is bytes:
        data = data.decode("utf-8").replace(',','')

    if data == 'STOPSERVEUR':
        stop = True
    else:
        if data in commands:
            if DEBUG: print(YELLOW+'\t'+data+WHITE)
            b = bindings[commands.index(data)]
            b[2](b[1])
        else:
            if DEBUG: print(RED+'\t'+data+WHITE+' (Unknown)')

print('STK input server stopped')
