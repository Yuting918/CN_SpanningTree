# Spanning Tree project for GA Tech OMS-CS CS 6250 Computer Networks
#
# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.  To 
# remain within the spirit of the project, the only inherited members
# functions the student is permitted to use are:
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm - 
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks
#           Based on prior work by Sean Donovan, 2015, updated for new VM by Jared Scott and James Lohse

from Message import *
from StpSwitch import *


class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):
        super(Switch, self).__init__(idNum, topolink, neighbors)
        self.root = self.switchID
        self.distance = 0
        self.activeLinks = []
        self.switchTrough = self.switchID
        self.links = neighbors

    def send_initial_messages(self):
        for link in self.links:
            message = Message(self.root, self.distance, self.switchID, link, False)
            self.send_message(message)
        return

    def send_updated_massage(self):
        for link in self.links:
            if self.switchTrough == link:
                message = Message(self.root, self.distance, self.switchID, link, True)
                self.send_message(message)
            else:
                message = Message(self.root, self.distance, self.switchID, link, False)
                self.send_message(message)


    def process_message(self, message):
        if ((message.root < self.root) or ((message.root == self.root) and ((message.distance + 1) < self.distance))):
            self.root = message.root
            self.distance = message.distance + 1
            if self.switchTrough in self.activeLinks:
                self.activeLinks.remove(self.switchTrough)
            if message.origin not in self.activeLinks:
                self.activeLinks.append(message.origin)
            self.switchTrough = message.origin
            self.send_updated_massage()

        elif message.pathThrough and message.origin not in self.activeLinks:
            self.activeLinks.append(message.origin)

        elif message.root == self.root and (message.distance + 1) == self.distance:
            if message.origin < self.switchTrough:
                self.activeLinks.remove(self.switchTrough)
                if message.origin not in self.activeLinks:
                    self.activeLinks.append(message.origin)
                self.switchTrough = message.origin
                self.send_updated_massage()
            elif message.origin > self.switchTrough:
                if message.origin in self.activeLinks:
                    self.activeLinks.remove(message.origin)

        elif message.root == self.root:
            if message.pathThrough == False:
                if message.origin in self.activeLinks:
                    self.activeLinks.remove(message.origin)


        elif message.root > self.root:
            self.send_updated_massage()
        return

    def generate_logstring(self):
        logs = []
        self.activeLinks.sort()
        for link in self.activeLinks:
            logs.append(str(self.switchID) + " - " + str(link))
        logString = ", ".join([str(log) for log in logs])
        return logString
