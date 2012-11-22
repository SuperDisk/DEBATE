#Debate, inspired by a cool TIGSource gamey

from wconio import WConio as conio

import os
import sys
import pickle
import socket
import struct
import traceback
import atexit

import msgs
import fixconio
import kbget

import encodings.idna as idna
import re


os.system("mode con cols=60 lines=30")

class WinMain:
    def __init__(self):
        self.players = []
        self.subject = ""
        self.team = None

        self.name = self.eraseInput("Enter username: ")
        self.ip = self.eraseInput("Enter session IP: ")
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, 5565))
        self.frame = 0
        self.id = -1

        self.connection.setblocking(0)

        self.sendMsg(msgs.SetName(name=self.name))

        atexit.register(self.sendMsg, (msgs.Leave(),))

    def update(self):
        if kbget.keyPush('T'):
            self.issueCommand(self.eraseInput("> "))

        try:
            datalen, = struct.unpack('h', self.connection.recv(2))
            self.processMsg(pickle.loads(self.connection.recv(datalen)))
        except socket.error:pass
        except:traceback.print_exc(file=sys.stdout)



        self.frame += 1

    def processMsg(self, msg):
        if msg.getID() == msgs.MSG_ASSIGNID:
            self.id = msg.getPID()

        elif msg.getID() == msgs.MSG_SETSUBJ:
            self.subject = msg.getSubject()
            fixconio.textcolor(5)
            print("Subject is now:", self.subject)
            fixconio.textcolor(15)

        elif msg.getID() == msgs.MSG_CHAT:
            fixconio.textcolor(msg.getColor())
            print(msg.getChat())
            fixconio.textcolor(15)

        elif msg.getID() == msgs.MSG_SETTEAM:
            print("Changed team to", str({True: "Pro", False: "Con", None:"Neutral"}[msg.getTeam()]))
            self.team = msg.getTeam()

        else:
            print("Received broken packet! ")


    def issueCommand(self, command):
        if "/" not in command:
            if self.team != None:
                self.sendMsg(msgs.Chat(chat=command))

            else:
                print("You can only talk on a team.")
                print("Join a team with: /team [pro or con or neutral]")

        else:
            if command.split(" ")[0] == "/team":
                if command.split(" ")[1] == "pro":
                    self.sendMsg(msgs.SetTeam(True))

                elif command.split(" ")[1] == "con":
                    self.sendMsg(msgs.SetTeam(False))

                else:
                    self.sendMsg(msgs.SetTeam())

            elif command.split(" ")[0] == "/topic":
                self.sendMsg(msgs.SetSubject(' '.join(command.split(" ")[1:])))

            elif command.split(" ")[0] == "/timeout":
                self.sendMsg(msgs.ResetTimeout(int(command.split(" ")[1])))

            else:
                print("Unknown command!")

    def sendMsg(self, msg):
        msg = pickle.dumps(msg)
        msg = struct.pack('h', len(msg)) + msg
        self.connection.send(msg)


    def eraseInput(self, prompt):
        pos = (fixconio.wherex(), fixconio.wherey())
        returnthing = input(prompt)
        fixconio.gotoxy(*pos)
        fixconio.clreol()
        fixconio.gotoxy(*pos)
        return returnthing

    def mainLoop(self):
        while 1:
            self.update()

winmain = WinMain()
winmain.mainLoop()
