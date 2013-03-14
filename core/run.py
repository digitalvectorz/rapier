# core.py
# | Rapier
# | Copyright Johnathon Mlady (c) 2013. <john@digitalvectorz.com>

import sys
import socket
import string
import os

from parseconfig import parse_config

class IRC:
	# Instantiation
	def __init__(self, config_file="../config.ini"):
		self.sock		= socket.socket()
		
		# Configuration
		config 			= parse_config(config_file)
		self.host		= config['HOST'] 
		self.port		= int(config['PORT']) 
		self.ident		= config['IDENT'] 
		self.owner		= config['OWNER'] 
		self.nickname	= config['NICK'] 
		self.realname	= config['REALNAME'] 
		self.channels	= config['CHANNELS'].split()	# type: list 
		self.password	= config['PASSWORD']
		self.trigger	= config['TRIGGER']
		self.auth		= config['AUTHORIZED'].split()	# type: list

	def run(self):
		line=self.sock.recv(500)	# recieve server msgs
		if line.rstrip():
			print line					# server msg is output
	
		# Check if we're connected to server
		if line.find('Welcome to the freenode Internet Relay Chat') != -1:
			for c in self.channels:
				self.join(c) #send('JOIN '+CHANNELS+'\n')	# Join a channel
		if line.find('PRIVMSG') != -1:
			self.parse_msg(line)
			line=line.rstrip()	# remove trailing 'rn'
			line=line.split()	
			# Handle PING/PONG
			if(line[0] == 'PING'):
				self.pong(line[1])


		
	# Core Methods
	def send(self, message=''):
		# Add a \n to the end of message if it doesn't already exist
		if not message.endswith('\r\n'):
			message = message.rstrip() 	# ensure \r and \n are not present at eol
			message = message + '\r\n'			
		self.sock.send(message)

	def connect(self):
		# !!! TODO: Add Error Checking
		self.sock.connect((self.host, self.port))
		self.nick()
		self.user()
		# Identify with nickserv
		# !!! TODO error checking/logging and possibly converting to fn
		self.privmsg('nickserv', 'identify ' + self.password)

	
	# IRC Commands
	def privmsg(self, target='', message=''):
		if target:
			self.send('PRIVMSG ' + target + ' :' + message)

	def nick(self, nick=''):
		# !!! TODO: error checking and logging
		if not nick and self.nickname:
			nick = self.nickname
		if nick:
			self.send('NICK ' + nick)
		
	def user(self, ident='', mode='0', rname=''):
		if not ident and self.ident:
			ident = self.ident
		if mode == '':  # !!! TODO add error checking integer check 
			mode = '0'
		if not rname:
			rname = self.realname

		# If any values are empty, don't continue
		# !!! TODO add error logging
		if not ident or not rname:
			return

		self.send('USER ' + ident + ' ' + mode + ' * :' + rname)

	def join(self, channel=''):
		if channel:
			self.send('JOIN ' + channel)

	def pong(self, resp):
		self.send('PONG ' + resp)

	#def mode(self, 

	# Lemma Functions
	def parse_msg(self, msg):
		# form[msg]
		#	:<name>!~<realname>@<mask> PRIVMSG <channel> :<message>

		complete	= msg[1:].split(':',1) 	# Parse into useful data
		info		= complete[0].split(' ')
		msgpart		= complete[1]
		sender		= info[0].split('@')
		if msgpart[0] == self.trigger and sender[0] == OWNER:	# Treat all msg's starting with ` as command
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

#		if msgpart[0]=='-' and sender[0]==OWNER:		# Treat msg with - as explicit cmd to send to server
#			cmd=msgpart[1:]
#			s.send(cmd+'\n')
#			print 'cmd='+cmd
#
#def syscmd(commandline, channel):
#	cmd=commandline.replace('sys ','')
#	cmd=cmd.rstrip()
#	os.system(cmd+' >temp.txt')
#	a=open('temp.txt')
#	ot=a.read()
#	ot.replace('\n','|')
#	a.close()
#	s.send('PRIVMSG '+channel+' :'+ot+'\n')
#	return 0


# Main Part
if __name__ == '__main__':
	rapier = IRC()
	rapier.connect()
	while 1:
		rapier.run()

