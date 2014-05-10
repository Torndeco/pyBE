# Filename: pyBE_chatbot.py
#    This file is part of pyBE.
#
#    pyBEscanner is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pyBEscanner is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pyBEscanner.  If not, see <http://www.gnu.org/licenses/>.



import ConfigParser

import argparse
import os
import platform
import sys
import time
import Queue

from modules import settings
from modules import rcon

from threading import Thread, Event, Lock

class Scheduler(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(60):
            print "*"
            # call a function

#def hello():
    #print "hello, world"

#t = Timer(30.0, hello)
#t.start() # after 30 seconds, "hello, world" will be printed


class Main:
	def __init__(self):
		#
		self.battleye_event_queue = Queue.Queue(400)
		self.settings, self.vac_bans_file = settings.Settings().load_rcon_bot_config()

		self.vac_bans = ConfigParser.ConfigParser().read(self.vac_bans_file)


	def on_battleye_event(self, event):

		try:
			self.battleye_event_queue.put((time.time(), time.time() + 10, event), timeout=2)
			#print('Battleye Event Queue: %s' % repr(self.battleye_event_queue))
		except Queue.Full:
			print("Battleye Event queue full, dropping event %r" % event)


	def route_battleye_event(self, message):

		if message.startswith('RCon admin #'):
			pass
		elif message.startswith('Player #'):
			if message.endswith(' disconnected'):
				pass
			elif message.endswith(' connected'):
				pass
			elif message.endswith('(unverified)'):
				pass
			elif message.find(' has been kicked by BattlEye: '):
				pass
			else:
				print('Unhandled server message %s' % message)
		elif message.startswith('Verified GUID'):
			pass
		elif message.startswith('(Lobby)'):
			pass
		elif message.startswith('(Global)'):
			pass
		elif message.startswith('(Direct)'):
			pass
		elif message.startswith('(Vehicle)'):
			pass
		elif message.startswith('(Group)'):
			pass
		elif message.startswith('(Side)'):
			pass
		elif message.startswith('(Command)'):
			pass
		elif message.find(' Log: #') != -1:
			pass
		else:
			print('Unhandled server message %s' % message)


	def close_battleye_connection(self, serverConnection):
		try:
			serverConnection.stop()
			self.sch_stop_flag.set()
		except Exception:
			pass


	def setup_battleye_connection(self, server, serverConnection):
		self.close_battleye_connection(serverConnection)
		serverConnection = rcon.BattleyeServer(server["ServerIP"], server["ServerPort"], server["RconPassword"])
		serverConnection.subscribe(self.on_battleye_event)
		time.sleep(5)

		self.sch_stop_flag = Event()
		self.sch_thread = Scheduler(self.sch_stop_flag)
		self.sch_thread.start()

		return serverConnection


	def start(self, serverid):
		os_name = platform.system()
		print "---------------------------------------------------------"
		print "Local System Platform = " + os_name
		print "---------------------------------------------------------"
		for server in self.settings:
			if server["Server ID"] == serverid:

				print "Server ID:       " + str(serverid)
				print "Server Name:     " + server["ServerName"]
				print "Server IP:       " + server["ServerIP"]
				print "Server Port:     " + str(server["ServerPort"])
				print "---------------------------------------------------------"
				serverConnection = None

				while True:
					if not serverConnection or not serverConnection.connected:
						try:
							serverConnection = self.setup_battleye_connection(server, serverConnection)
							timeout = 60 + time.time()
							while (time.time() < timeout) and not (serverConnection.connected):
								print ("Retrying to connect to game server...")
								serverConnection = self.setup_battleye_connection(server, serverConnection)
						except KeyboardInterrupt:
							print
							print("Stopping pyBE....")
							print
							self.close_battleye_connection(serverConnection)
							sys.exit()
						except IOError, err:
							print("IOError %s"% err)
							sys.exit()
						except Exception, err:
							print("\n")
							print("Unexpected error")
							print("Error %s"% err)
							# unexpected exception, better close the battleye connection
							self.close_battleye_connection(serverConnection)
							sys.exit()

					try:
						added, expire, event = self.battleye_event_queue.get(timeout=5)
						#print str(added)
						#print str(expire)
						#print str(event)
						#print ("--------------------")
						self.route_battleye_event(event)
					except Queue.Empty:
						sys.stdout.write('.')
						sys.stdout.flush()
					except rcon.BattleyeError, err:
						# the connection to the battleye server is lost
						print("\n")
						print(str(err))
						self.close_battleye_connection()
					except IOError, err:
						print("IOError %s"% err)
						sys.exit()
					except KeyboardInterrupt:
						print
						print("Stopping pyBE....")
						print
						self.close_battleye_connection(serverConnection)
						sys.exit()
					except Exception, err:
						print("\n")
						print("Unexpected error")
						print("Error %s"% err)
						# unexpected exception, better close the battleye connection
						self.close_battleye_connection(serverConnection)
						sys.exit()

parser = argparse.ArgumentParser(description='pyBEbot Usage: pyBE <serverid>')
parser.add_argument("serverid")
args = parser.parse_args()

main = Main()
main.start(args.serverid)