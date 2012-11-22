import ctypes

kbdll = ctypes.windll.LoadLibrary("KeyboardGet.dll")

def keyPushed(key):
    return kbdll.GetIsPushed(ord(key.upper())) != 0

def keyPush(key):
    return kbdll.GetIsPushed(ord(key.upper())) == -32767
