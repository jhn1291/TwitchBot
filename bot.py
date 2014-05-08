#!/usr/bin/env python
import sys
import socket
import string
from random import randint

def Sockinit(HOST, PORT, PASS, NICK, IDENT, REALNAME, CHAN, s): 
	s.connect((HOST, PORT))
	s.send("PASS %s\r\n" % PASS)
	s.send("NICK %s\r\n" % NICK)
	s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
	s.send("JOIN :%s\r\n" % CHAN)

def extractName(line):
	newUser = ""
	iterator = line[0][1]
	i = 2
	while(iterator != '!'):
		newUser = newUser + iterator
		iterator = line[0][i]
		i += 1
	return newUser

def interpretPlayerMSG(line):
	if(line[3] == ':!help'):
		return 0
	if(line[3] == ':!fortune'):
		return 1
	if(line[3] == ':!fact'):
		return 2
	if(line[3] == ':!trailer'):
		return 3
	

def readFortune(fortunes):
	return fortunes[randint(1, len(fortunes))]

def botTalk(s, NICK, CHAN, words):
	s.send(":%s %s %s :%s\r\n" % (NICK, 'PRIVMSG', CHAN, words))
	return

def commandList():
	commandList = []
	commandList.append("=LIST OF COMMANDS=\r\n")
	commandList.append("!help    -- List bot commands\r\n")
 	commandList.append("!fortune -- Shake the 8-ball\r\n")
	commandList.append("!fact    -- Learn a fun fact\r\n")
	commandList.append("=========================\r\n")
	return commandList

def tpbquote(quotes, s, NICK, CHAN):
	index = randint(1, len(quotes))
	startLine = quotes[index]	
	while(len(startLine) > 2):
		index = index + 1
		startLine = quotes[index]
	
	index = index + 1
	startLine = quotes[index]
	while(len(startLine) > 2):
		botTalk(s, NICK, CHAN, startLine)
		index = index + 1
		startLine = quotes[index]
	return

def main():

	s=socket.socket()
	HOST="irc.twitch.tv"
	PORT=6667
	PASS='oauth:72ufy9dsoqf6eqy0r5d9rt426bipooo'
	NICK="Tatl_and_tael"
	IDENT="Tatl_and_tael"
	REALNAME="Tatl_and_tael"
	CHAN="#natefromspace"
	readbuffer=""
	

	with open('8ball.txt') as infile:
		fortunes = infile.readlines()
		infile.close()

	with open('facts.txt') as infile:
		facts = infile.readlines()
		infile.close()

	with open('trailer.txt') as infile:
		tpbQuotes = infile.readlines()
		infile.close()

	Sockinit(HOST, PORT, PASS, NICK, IDENT, REALNAME, CHAN, s)

	while 1:
		readbuffer=readbuffer+s.recv(1024)
		temp=string.split(readbuffer, "\n")
		readbuffer=temp.pop()

		for line in temp:
			line=string.rstrip(line)
			line=string.split(line)
		
		if(line[0]=="PING"):
			s.send("PONG %s\r\n" % line[1])

		if(line[1] == 'PRIVMSG'):
			playermsg = interpretPlayerMSG(line)

			if(playermsg == 0 and (extractName(line) == "demmko" or extractName(line) == "dungaloid")):
				myCommands = commandList()
				for i in range(len(myCommands)):
					botTalk(s, NICK, CHAN, myCommands[i])
			if(playermsg == 1):
				botTalk(s, NICK, CHAN, readFortune(fortunes)) 	

			if(playermsg == 2):
				botTalk(s, NICK, CHAN, facts[randint(1, len(facts))])
			
			if(playermsg == 3 and (extractName(line) == "demmko" or extractName(line) == "dungaloid")):
				tpbquote(tpbQuotes, s, NICK, CHAN) 	

		if(line[1] == 'JOIN'):
			welcome = "Welcome to demmko's channel, " + extractName(line)  + "!"
			welcome = welcome + " I am demmko's new chatbot, type '!help' (no quotes) for" 
			welcome = welcome + " a list of commands\r\n"
			botTalk(s, NICK, CHAN, welcome)

		print line



main()
