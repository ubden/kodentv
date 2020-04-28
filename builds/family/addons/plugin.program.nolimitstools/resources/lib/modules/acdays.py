"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import zipfile
from resources.lib.modules import extract
from resources.lib.modules import downloader
from resources.lib.modules import installer
import re
import time
from resources.lib.modules import common as Common
from resources.lib.modules import wipe
from resources.lib.modules import plugintools
from random import randint
from datetime import date
import calendar
from resources.lib.modules import maintenance

def Checker():

	addon_id = 'plugin.program.nolimitstools'
	my_date = date.today()
	today = calendar.day_name[my_date.weekday()]
	accache = plugintools.get_setting("accache")
	acpackages = plugintools.get_setting("acpackages")
	accrash = plugintools.get_setting("accrash")
	acthumbs = plugintools.get_setting("acthumbs")
	day = plugintools.get_setting("clearday")
	CLEANEDMON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/cleanedmon.txt'))
	CLEANEDTUE = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/cleanedtue.txt'))
	CLEANEDWED = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/cleanedwed.txt'))
	CLEANEDTHU = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/cleanedthu.txt'))
	CLEANEDFRI = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/cleanedfri.txt'))
	CLEANEDSAT = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/cleanedsat.txt'))
	CLEANEDSUN = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/cleanedsun.txt'))
	cleaned = 0

	if day == "0":
		cleaned = 0
	
	if today == "Monday" and day == "1":
		cleaned = 1
		if not os.path.isfile(CLEANEDMON):
			if accache == "true":
				maintenance.AutoCache()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			open(CLEANEDMON, 'w')
		if os.path.isfile(CLEANEDTUE):
			try:
				os.remove(CLEANEDTUE)
			except: pass
		if os.path.isfile(CLEANEDWED):
			try:
				os.remove(CLEANEDWED)
			except: pass
		if os.path.isfile(CLEANEDTHU):
			try:
				os.remove(CLEANEDTHU)
			except: pass
		if os.path.isfile(CLEANEDFRI):
			try:
				os.remove(CLEANEDFRI)
			except: pass
		if os.path.isfile(CLEANEDSAT):
			try:
				os.remove(CLEANEDSAT)
			except: pass
		if os.path.isfile(CLEANEDSUN):
			try:
				os.remove(CLEANEDSUN)
			except: pass

	if today == "Tuesday" and day == "2":
		cleaned = 1
		if not os.path.isfile(CLEANEDTUE):
			if accache == "true":
				maintenance.AutoCache()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			open(CLEANEDTUE, 'w')
		if os.path.isfile(CLEANEDMON):
			try:
				os.remove(CLEANEDMON)
			except: pass
		if os.path.isfile(CLEANEDWED):
			try:
				os.remove(CLEANEDWED)
			except: pass
		if os.path.isfile(CLEANEDTHU):
			try:
				os.remove(CLEANEDTHU)
			except: pass
		if os.path.isfile(CLEANEDFRI):
			try:
				os.remove(CLEANEDFRI)
			except: pass
		if os.path.isfile(CLEANEDSAT):
			try:
				os.remove(CLEANEDSAT)
			except: pass
		if os.path.isfile(CLEANEDSUN):
			try:
				os.remove(CLEANEDSUN)
			except: pass
		
	if today == "Wednesday" and day == "3":
		cleaned = 1
		if not os.path.isfile(CLEANEDWED):
			if accache == "true":
				maintenance.AutoCache()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			open(CLEANEDWED, 'w')
		if os.path.isfile(CLEANEDTUE):
			try:
				os.remove(CLEANEDTUE)
			except: pass
		if os.path.isfile(CLEANEDMON):
			try:
				os.remove(CLEANEDMON)
			except: pass
		if os.path.isfile(CLEANEDTHU):
			try:
				os.remove(CLEANEDTHU)
			except: pass
		if os.path.isfile(CLEANEDFRI):
			try:
				os.remove(CLEANEDFRI)
			except: pass
		if os.path.isfile(CLEANEDSAT):
			try:
				os.remove(CLEANEDSAT)
			except: pass
		if os.path.isfile(CLEANEDSUN):
			try:
				os.remove(CLEANEDSUN)
			except: pass

	if today == "Thursday" and day == "4":
		cleaned = 1
		if not os.path.isfile(CLEANEDTHU):
			if accache == "true":
				maintenance.AutoCache()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			open(CLEANEDTHU, 'w')
		if os.path.isfile(CLEANEDTUE):
			try:
				os.remove(CLEANEDTUE)
			except: pass
		if os.path.isfile(CLEANEDWED):
			try:
				os.remove(CLEANEDWED)
			except: pass
		if os.path.isfile(CLEANEDMON):
			try:
				os.remove(CLEANEDMON)
			except: pass
		if os.path.isfile(CLEANEDFRI):
			try:
				os.remove(CLEANEDFRI)
			except: pass
		if os.path.isfile(CLEANEDSAT):
			try:
				os.remove(CLEANEDSAT)
			except: pass
		if os.path.isfile(CLEANEDSUN):
			try:
				os.remove(CLEANEDSUN)
			except: pass

	if today == "Friday" and day == "5":
		cleaned = 1
		if not os.path.isfile(CLEANEDFRI):
			if accache == "true":
				maintenance.AutoCache()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			open(CLEANEDFRI, 'w')
		if os.path.isfile(CLEANEDTUE):
			try:
				os.remove(CLEANEDTUE)
			except: pass
		if os.path.isfile(CLEANEDWED):
			try:
				os.remove(CLEANEDWED)
			except: pass
		if os.path.isfile(CLEANEDTHU):
			try:
				os.remove(CLEANEDTHU)
			except: pass
		if os.path.isfile(CLEANEDMON):
			try:
				os.remove(CLEANEDMON)
			except: pass
		if os.path.isfile(CLEANEDSAT):
			try:
				os.remove(CLEANEDSAT)
			except: pass
		if os.path.isfile(CLEANEDSUN):
			try:
				os.remove(CLEANEDSUN)
			except: pass

	if today == "Saturday" and day == "6":
		cleaned = 1
		if not os.path.isfile(CLEANEDSAT):
			if accache == "true":
				maintenance.AutoCache()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			open(CLEANEDSAT, 'w')
		if os.path.isfile(CLEANEDTUE):
			try:
				os.remove(CLEANEDTUE)
			except: pass
		if os.path.isfile(CLEANEDWED):
			try:
				os.remove(CLEANEDWED)
			except: pass
		if os.path.isfile(CLEANEDTHU):
			try:
				os.remove(CLEANEDTHU)
			except: pass
		if os.path.isfile(CLEANEDFRI):
			try:
				os.remove(CLEANEDFRI)
			except: pass
		if os.path.isfile(CLEANEDMON):
			try:
				os.remove(CLEANEDMON)
			except: pass
		if os.path.isfile(CLEANEDSUN):
			try:
				os.remove(CLEANEDSUN)
			except: pass
		
	if today == "Sunday" and day == "7":
		cleaned = 1
		if not os.path.isfile(CLEANEDSUN):
			if accache == "true":
				maintenance.AutoCache()
			if accrash == "true":
				maintenance.AutoCrash()
			if acthumbs == "true":
				maintenance.AutoThumbs()
			if acpackages == "true":
				time.sleep(60)
				maintenance.AutoPackages()
			open(CLEANEDSUN, 'w')
		if os.path.isfile(CLEANEDTUE):
			try:
				os.remove(CLEANEDTUE)
			except: pass
		if os.path.isfile(CLEANEDWED):
			try:
				os.remove(CLEANEDWED)
			except: pass
		if os.path.isfile(CLEANEDTHU):
			try:
				os.remove(CLEANEDTHU)
			except: pass
		if os.path.isfile(CLEANEDFRI):
			try:
				os.remove(CLEANEDFRI)
			except: pass
		if os.path.isfile(CLEANEDSAT):
			try:
				os.remove(CLEANEDSAT)
			except: pass
		if os.path.isfile(CLEANEDMON):
			try:
				os.remove(CLEANEDMON)
			except: pass

	if cleaned == 0:
		if os.path.isfile(CLEANEDMON):
			try:
				os.remove(CLEANEDMON)
			except: pass
		if os.path.isfile(CLEANEDTUE):
			try:
				os.remove(CLEANEDTUE)
			except: pass
		if os.path.isfile(CLEANEDWED):
			try:
				os.remove(CLEANEDWED)
			except: pass
		if os.path.isfile(CLEANEDTHU):
			try:
				os.remove(CLEANEDTHU)
			except: pass
		if os.path.isfile(CLEANEDFRI):
			try:
				os.remove(CLEANEDFRI)
			except: pass
		if os.path.isfile(CLEANEDSAT):
			try:
				os.remove(CLEANEDSAT)
			except: pass
		if os.path.isfile(CLEANEDSUN):
			try:
				os.remove(CLEANEDSUN)
			except: pass
		