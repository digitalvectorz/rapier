# core.py
# | Rapier
# | Copyright Johnathon Mlady (c) 2013. <john@digitalvectorz.com>

import sys
import socket
import string
import os

import parseconfig

config = parseconfig("config.ini")

HOST=config['HOST'] #'irc.freenode.net'
PORT=config['PORT'] #6667
NICK=config['NICK'] #'Rapier'
IDENT=config['IDENT'] #'dvbot'
REALNAME=config['REALNAME'] #'Rapier'
OWNER=config['OWNER'] #'dvz-'
CHANNELS=config['CHANNELS'] #'#gamegods'
PASSWORD=config['PASSWORD']

readbuffer=''					# Store messages from server


# Socket Initialization
s = socket.socket()				# Create socket
s.connect( (HOST, PORT) )		# Connect to server
s.send( 'NICK '+NICK+'\n' )		# Send the nick to server
s.send( 'USER '+IDENT+' '+HOST+' bla :'+REALNAME+'\n')	# Identify to server
s.send( 'PRIVMSG nickserv :identify '+PASSWORD+'\n' )


def parsemsg(msg):
	complete=msg[1:].split(':',1) 	# Parse into useful data
	info=complete[0].split(' ')
	msgpart=complete[1]
	sender=info[0].split('!')
	if msgpart[0] == '`' and sender[0] == OWNER:	# Treat all msg's starting with ` as command
		cmd=msgpart[1:].split(' ')
		if cmd[0]=='op':
			s.send('MODE '+info[2]+' +o '+cmd[1]+'\n')
		if cmd[0]=='deop':
			s.send('MODE '+info[2]+' -o '+cmd[1]+'\n')
		if cmd[0]=='voice':
			s.send('MODE '+info[2]+' +v '+cmd[1]+'\n')
		if cmd[0]=='devoice':
			s.send('MODE '+info[2]+' -v '+cmd[1]+'\n')
		if cmd[0]=='sys':
			syscmd(msgpart[1:],info[2])

	if msgpart[0]=='-' and sender[0]==OWNER:		# Treat msg with - as explicit cmd to send to server
		cmd=msgpart[1:]
		s.send(cmd+'\n')
		print 'cmd='+cmd

def syscmd(commandline, channel):
	cmd=commandline.replace('sys ','')
	cmd=cmd.rstrip()
	os.system(cmd+' >temp.txt')
	a=open('temp.txt')
	ot=a.read()
	ot.replace('\n','|')
	a.close()
	s.send('PRIVMSG '+channel+' :'+ot+'\n')
	return 0


# Main Part
while 1:
	line=s.recv(500)			# recieve server msgs
	print line					# server msg is output
	
	if line.find('Welcome to the freenode Internet Relay Chat Network') != -1:
		s.send('JOIN '+CHANNELS+'n')	# Join a channel
	if line.find('PRIVMSG') != -1:
		parsemsg(line)
		line=line.rstrip()	# remove trailing 'rn'
		line=line.split()	
		if(line[0] == 'PING'):	# If server pings, then pong
			s.send('PONG '+line[1]+'\n')


