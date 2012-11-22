import os, sys
import pickle
import socket
import struct
import traceback
import copy
import _thread as thread
from time import sleep

import msgs
from player import Player


class WinMain:
    def __init__(self):
        self.players = []

        self.timeout = 300

        if len(sys.argv) > 1:
            for index, arg in enumerate(sys.argv):
                if 'timeout=' in arg:
                    self.timeout = int(arg.split('=')[1])
                    del sys.argv[index]
                    break

        if len(sys.argv) < 1:
            self.subject = "Sample Subject"
        else:
            stuf = copy.copy(sys.argv)
            del stuf[0]
            self.subject = " ".join(stuf)

        print("Starting new server on port 5565!")
        print("Topic is", self.subject)
        print("Timeout is", self.timeout)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', 5565))

        thread.start_new_thread(self.getPlayers, ())
        thread.start_new_thread(self.runTimer, ())

    def getPlayers(self):
        try:
            while 1:
                self.server.listen(1)
                conn, _ = self.server.accept()
                conn.setblocking(False)
                self.players.append(Player(conn, None, len(self.players)))
                self.sendMsg(self.players[len(self.players) - 1], msgs.AssignID(pid=len(self.players) - 1))
                self.sendMsg(self.players[len(self.players) - 1], msgs.SetSubject(subject=self.subject))

        except:traceback.print_exc(file=sys.stdout)

    def update(self):
        for player in self.players:
            try:
                datalen, = struct.unpack('h', player.getSocket().recv(2))
                msg = pickle.loads(player.getSocket().recv(datalen))
                self.processMsg(msg, player)
            except socket.error as e:
                if e.errno == 10035: pass
                if e.errno == 10054:
                    self.killPlayer(player)

                
            except:traceback.print_exc(file=sys.stdout)

    def sendMsg(self, receiver, msg):
        msg = pickle.dumps(msg)
        msg = struct.pack('h', len(msg)) + msg
        receiver.socket.send(msg)

    def broadcastMsg(self, msg):
        msg = pickle.dumps(msg)
        for player in self.players:
            player.socket.send(struct.pack('h', len(msg)) + msg)

    def processMsg(self, msg, sender=...):
        if msg.getID() == msgs.MSG_SETNAME:
            sender.setName(msg.name)
            self.broadcastMsg(msgs.Chat(chat=msg.name + " has joined the debate!"))
            print("Got name:", msg.name)

        elif msg.getID() == msgs.MSG_CHAT:
            print("CHAT:", msg.getChat())

            thecolor = {True: 1, False: 4, None: 15}[sender.getTeam()]
            self.broadcastMsg(msgs.Chat(chat=sender.name + ": " + msg.getChat(), color=thecolor))

        elif msg.getID() == msgs.MSG_SETTEAM:
            print(sender.getName(), "changed team to:", str(msg.getTeam()))
            sender.setTeam(msg.getTeam())
            self.sendMsg(sender, msgs.SetTeam(team=msg.getTeam()))

        elif msg.getID() == msgs.MSG_SETSUBJ:
            self.subject = msg.getSubject()
            print(sender.getName(), "changed the subject to", self.subject)
            self.broadcastMsg(msg)

        elif msg.getID() == msgs.MSG_RESETTIMEOUT:
            self.timeout = msg.getTimeout()
            thread.start_new_thread(self.runTimer, ())

    def killPlayer(self, player):
        for index, item in enumerate(self.players):
            if item is player:
                del self.players[index]
                self.broadcastMsg(msgs.Chat(item.getName() + " has left the debate."))
                break

    def mainLoop(self):
        while 1: self.update()

    def runTimer(self):
        sleep(self.timeout)
        procount = 0
        concount = 0

        for player in self.players:
            if player.team == True:
                procount += 1

            if player.team == False:
                concount += 1

        if procount == concount:
            self.broadcastMsg(msgs.Chat("GAME OVER! There was a tie!", color=3))

        else:
            self.broadcastMsg(msgs.Chat("GAME OVER! Team " + {True: "Pro", False:"Con"}[procount>concount] + " had the majority vote!", color=3))
        
winmain = WinMain()
winmain.mainLoop()
