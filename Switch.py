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

    def __repr__(self):
        return "%% Switch "+ str(self.switchID) +" %%  "+" root = " + str(self.root) + "; distance = " + str(self.distance) \
               + "; activeLinks = " + str(self.activeLinks) + \
               "; switchThrough = " + str(self.switchTrough) + "\n"

    def send_initial_messages(self):
        print("####Begin initial massage\n")
        for link in self.links:
            message = Message(self.root, self.distance, self.switchID, link, False)
            self.send_message(message)
            print(message)
        print("end initial message##")
        return

    def send_updated_massage(self):
        for link in self.links:
            if self.switchTrough == link:
                message = Message(self.root, self.distance, self.switchID, link, True)
                self.send_message(message)
                print("Sent Message")
                print(message)
            else:
                message = Message(self.root, self.distance, self.switchID, link, False)
                self.send_message(message)
                print("Sent Message")
                print(message)

    def process_message(self, message):
        print("&&& \nCurrent Switch is")
        print(self)
        print("###Process message")
        print(message)
        print("end message ###")
        if message.root < self.root or (message.distance + 1) < self.distance:
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

        elif not message.pathThrough and message.origin in self.activeLinks:
            self.activeLinks.remove(message.origin)
            self.send_updated_massage()

        elif message.origin < self.switchTrough:
            self.activeLinks.remove(self.switchTrough)
            if message.origin not in self.activeLinks:
                self.activeLinks.append(message.origin)
            self.switchTrough = message.origin
            self.send_updated_massage()
        print("Switched is updated to")
        print(self)
        return

    def generate_logstring(self):
        # TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked 
        #      only after the simulaton is complete.  Output the links included in the 
        #      spanning tree by increasing destination switch ID on a single line. 
        #      Print links as '(source switch id) - (destination switch id)', separating links 
        #      with a comma - ','.  
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string 
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        #       "switch log string, do not return a static string, build the log string"
        logs = []
        for link in self.activeLinks:
            logs.append(str(self.switchID) + " - " + str(link))
        logString = ", ".join([str(log) for log in logs])
        return logString
