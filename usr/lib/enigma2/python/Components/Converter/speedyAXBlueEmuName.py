# EmuName
# Copyright (c) 2boom & Taapat 2013-14
# v.1.0
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.config import config
from Components.Element import cached
from Tools.Directories import fileExists
from Poll import Poll
import os

class EmuName(Poll, Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.poll_interval = 2000
		self.poll_enabled = True
		
	@cached
	def getText(self):
		info = ""
		info2 = ""
		nofile = False
		camdname = None
		cardname = None
		camdlist = None
		# VTI 	
		if fileExists("/tmp/.emu.info"):
			try:
				camdname = open("/tmp/.emu.info", "r")
			except:
				camdname = None
		# TS-Panel
		elif fileExists("/etc/startcam.sh"):
			try:
				camdname = open("/etc/startcam.sh", "r")
			except:
				camdname = None
		# BlackHole	
		elif fileExists("/etc/CurrentBhCamName"):
			try:
				camdname = open("/etc/CurrentBhCamName", "r")
			except:
				camdname = None
		# Domica	
		elif fileExists("/etc/active_emu.list"):
			try:
				camdname = open("/etc/active_emu.list", "r")
			except:
				camdname = None
				# OoZooN
		elif fileExists("/tmp/cam.info"):
			try:
				camdname = open("/tmp/cam.info", "r")
			except:
				camdname = None
		# Merlin2	
		elif fileExists("/etc/clist.list"):
			try:
				camdname = open("/etc/clist.list", "r")
			except:
				camdname = None
		# GP3
		elif fileExists("/usr/lib/enigma2/python/Plugins/Bp/geminimain/lib/libgeminimain.so"):
			try:
				from Plugins.Bp.geminimain.plugin import GETCAMDLIST
				from Plugins.Bp.geminimain.lib import libgeminimain
				camdl = libgeminimain.getPyList(GETCAMDLIST)
				cam = None
				for x in camdl:
					if x[1] == 1:
						cam = x[2] 
				camdname = cam
				nofile = True
			except:
				camdname = None
		#Pli
		elif fileExists("/etc/init.d/softcam") or fileExists("/etc/init.d/cardserver"):
			try:
				camdname = open("/etc/init.d/softcam", "r")
			except:
				camdname = None
			try:
				cardname = open("/etc/init.d/cardserver", "r")
			except:
				cardname = None 
		elif fileExists("/etc/.emustart"):
			try:
				camdname = open("/etc/.emustart", "r")
			except:
				camdname = None

		if cardname:
			for line in cardname:
				info2 = ""
				if 'oscam' in line.lower():
					info2 = 'oscam'
				elif 'newcs' in line.lower():
					info2 = 'newcs'
				elif 'wicard' in line.lower():
					info2 = 'wicardd'
				elif 'cccam' in line.lower():
					info2 = 'cccam'
			cardname.close()
		if camdname:
			camdlist = camdname
		if camdlist:
			info = 'unknow'
			if nofile:
				if nofile:
					line = camdlist
			else:
				for line in camdlist:
					if 'mgcamd' in line.lower() and 'oscam' in line.lower():
						info = 'oscammgcamd'
						break
					if 'cccam' in line.lower() and 'oscam' in line.lower():
						info = 'oscamcccam'
						break
					elif 'mgcamd' in line.lower():
						info = 'mgcamd'
					elif 'oscam' in line.lower():
						info = 'oscam'
					elif 'wicard' in line.lower():
						info = 'wicardd'
					elif 'cccam' in line.lower():
						info = 'cccam'
					elif 'camd3' in line.lower():
						info = 'camd3'
					elif 'evocamd' in line.lower():
						info = 'evocamd'
					elif 'newcs' in line.lower():
						info = 'newcs'
					elif 'rqcamd' in line.lower():
						info = 'rqcamd'
					elif 'gbox' in line.lower():
						info = 'gbox'
					elif 'mpcs' in line.lower():
						info = 'mpcs'
					elif 'sbox' in line.lower():
						info = 'sbox'
					elif 'scam' in line.lower():
						info = 'scam'
		if camdname and not nofile:
			camdname.close()
		return info2 + info

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, (self.CHANGED_POLL,))
