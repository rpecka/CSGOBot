# Modified from sentdex's pygta5
# Citation: Box Of Hats (https://github.com/Box-Of-Hats )

import win32api as wapi
import time

mappableKeys = ["\b"] # the list of all the keys that can be mapped to a character
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
    mappableKeys.append(char)

# Full list of key codes here https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx.85).aspx

LSHIFT = 0xA0
LCTRL = 0xA2
LBUTTON = 0x01
RBUTTON = 0x02

nonMappableKeys =     [ LSHIFT,  LCTRL, LBUTTON, RBUTTON]  # the list of keys that cannot be mapped to a character
nonMappanleKeyNames = ["SHIFT", "CTRL",  "LBUTTON", "RBUTTON"]

codedKeys = nonMappableKeys[:] # the list of all keys by their unicode key
for char in mappableKeys:
    codedKeys.append(ord(char))

def key_check():
    keys = []
    for code in codedKeys:
        if wapi.GetAsyncKeyState(code):
            keys.append(token_for_code(code))
    x, y = wapi.GetCursorPos()
    return keys, x, y

def token_for_code(code):
    if code in nonMappableKeys:
        index = nonMappableKeys.index(code)
        return nonMappanleKeyNames[index]
    else:
        return str(chr(code))
