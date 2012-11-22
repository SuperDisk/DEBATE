from wconio.WConio import *

def layCh(char, pos):
    gotoxy(pos[0], pos[1])
    putch(char)

def layStr(string, pos):
    gotoxy(pos[0], pos[1])
    cputs(string)

def delCh(pos):
    gotoxy(pos[0], pos[1])
    putch(" ")

def layCh(char, pos):
    gotoxy(pos[0], pos[1])
    putch(char)

def moveCur(pos):
    gotoxy(wherex() + pos[0], wherey() + pos[1])
