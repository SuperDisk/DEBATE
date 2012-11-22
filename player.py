class Player:
    def __init__(self, socket, team, pid):
        self.name = "No name"
        self.team = team
        self.id = pid
        self.socket = socket

    def getSocket(self):
        return self.socket

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getTeam(self):
        return self.team

    def setName(self, name):
        self.name = name

    def setTeam(self, team):
        self.team = team
