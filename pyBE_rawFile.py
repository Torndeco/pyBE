# Filename: pyBE_rawFile.py
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


import argparse
import os
import sys
import time

from modules import settings
from modules import rcon


def close_battleye_connection(serverConnection):
	try:
		serverConnection.stop()
	except Exception:
		pass


parser = argparse.ArgumentParser(description='pyBE_rawFile Usage: pyBE_rawFile <serverid> <filename>')
parser.add_argument("serverid")
parser.add_argument("filename")
args = parser.parse_args()

settings, vac_bans_file = settings.Settings().load_rcon_bot_config()

for server in settings:
	if server["Server ID"] == args.serverid:
		serverConnection = None
		try:
			if os.path.isfile(args.filename) is True:
				serverConnection = rcon.BattleyeServer(server["ServerIP"], server["ServerPort"], server["RconPassword"])
				timeout = 60 + time.time()
				while (time.time() < timeout) and not (serverConnection.connected):
					print ("Retrying to connect to " + server["ServerName"])
					time.sleep(5)
					close_battleye_connection(serverConnection)
					serverConnection = rcon.BattleyeServer(server["ServerIP"], server["ServerPort"], server["RconPassword"])
				if serverConnection.connected:
					try:
						with open(args.filename) as f:
							for line in f:
								command = line.strip()
								data = serverConnection.command(command)
								time.sleep(0.5)
						time.sleep(5)
					finally:
						close_battleye_connection(serverConnection)
				sys.exit()
			else:
				print "File not found"
		except KeyboardInterrupt:
			print
			print("Stopping pyBE....")
			print
			close_battleye_connection(serverConnection)
			sys.exit()
		except IOError, err:
			print("IOError %s"% err)
			sys.exit()
		except Exception, err:
			print("\n")
			print("Unexpected error")
			print("Error %s"% err)
			# unexpected exception, better close the battleye connection
			close_battleye_connection(serverConnection)
			sys.exit()