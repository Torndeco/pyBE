# Filename: settings.py
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
#    along with pyBE.  If not, see <http://www.gnu.org/licenses/>.

import ConfigParser
import copy
import os
import re
import sys


class Settings:
	def __init__(self):

		self.main_dir = os.getcwd()
		conf_dir = os.path.join(self.main_dir, 'conf')

		self.conf_file = os.path.join(self.main_dir, 'conf', 'conf.ini')
		self.vac_bans_file = os.path.join(self.main_dir, 'conf', 'vac_bans.ini')

		if not os.path.isfile(os.path.join(self.main_dir, 'pyBE_chatbot.py')):
			print "Wrong working Directory"
			sys.exit()
		else:
			if not os.path.exists(conf_dir):
				print "Missing Conf Directory @ " + self.conf_dir
				sys.exit()
			else:
				if not os.path.isfile(self.conf_file):
					print "Missing Server Configs @ " + self.conf_file
					sys.exit()

		config = ConfigParser.ConfigParser()
		config.read(self.conf_file)

		if config.has_option("Default", "Version"):
			if config.get("Default", "Version") != "20":
				print "-------------------------------------------------"
				print "ERROR: Bad conf.ini version"
				print "-------------------------------------------------"
				print "Read Changes.txt for more info"
				print "Old version = " + config.get("Default", "Version")
				sys.exit()
		else:
			print "-------------------------------------------------"
			print "ERROR: No conf.ini version found"
			print "-------------------------------------------------"
			print "This either means a mistake in your servers.ini file,"
			print "Look @ conf-example.ini"
			print
			print "Or if u haven't updated in awhile"
			print "Recommend u delete pyBEscanner temp folders & read Changes.txt for update changes"
			sys.exit()


	def get_config_file(self):
		return self.conf_file


	def load_rcon_bot_config(self):

		settings = []

		config = ConfigParser.ConfigParser()
		config.read(self.conf_file)
		config_sections= config.sections()
		config_sections.remove("Default")

		default = { "pyBE Directory": self.main_dir}

		options = []

		for x in range(len(options)):
			default[options[x][1]] = config.get("Default", options[x][0])

		for section in config_sections:

			server = copy.copy(default)

			## Server Info
			server["Server ID"] = section
			server["ServerName"] = config.get(section, "ServerName")
			server["ServerIP"] = config.get(section, "ServerIP")
			server["ServerPort"] = config.getint(section, "ServerPort")
			server["RconPassword"] = config.get(section, "RconPassword")

			for y in range(len(options)):
				if config.has_option(section, options[y][0]):
					server[options[y][1]] = config.get(section, options[y][0])

			settings.append(server)

		return settings, self.vac_bans_file