MSG_ASSIGNID = 1
MSG_SETNAME = 2
MSG_SETSUBJ = 3
MSG_CHAT = 4
MSG_SETTEAM = 5
MSG_LEAVE = 6
MSG_JOIN = 7
MSG_RESETTIMEOUT = 8

class Message:
    def __init__(self):
        self.id = 0

    def getID(self):
        return self.id


class AssignID(Message):
    def __init__(self, pid=-1):
        super().__init__()
        self.id = MSG_ASSIGNID
        self.pid = pid

    def getPID(self):
        return self.pid

class SetName(Message):
    def __init__(self, name="No Name"):
        super().__init__()
        self.id = MSG_SETNAME
        self.name = name

    def getName(self):
        return self.name

class SetSubject(Message):
    def __init__(self, subject=""):
        super().__init__()
        self.id = MSG_SETSUBJ
        self.subject = subject

    def getSubject(self):
        return self.subject

class Chat(Message):
    def __init__(self, chat="", color=15):
        super().__init__()
        self.id = MSG_CHAT
        self.chat = chat
        self.color = color

    def getChat(self):
        return self.chat

    def getColor(self):
        return self.color

class SetTeam(Message):
    def __init__(self, team=None):
        super().__init__()
        self.id = MSG_SETTEAM
        self.team = team

    def getTeam(self):
        return self.team

class ResetTimeout(Message):
    def __init__(self, timeout=300):
        super().__init__()
        self.id = MSG_RESETTIMEOUT
        self.timeout = timeout

    def getTimeout(self):
        return self.timeout
    
class Leave(Message):
    def __init__(self):
        super().__init__()
        self.id = MSG_LEAVE

class Join(Message):
    def __init__(self):
        super().__init__()
        self.id = MSG_JOIN
