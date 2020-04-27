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
#######################################################################
#						GET ALL DEPENDANCIES NEEDED
#######################################################################
import xbmc, xbmcgui, shutil, os, base64, urllib, urllib2 

addon_id      =  'plugin.program.nolimitstools'
AddonTitle    =  "[COLOR yellowgreen]ECHO[/COLOR] [COLOR white]Wizard[/COLOR]"
TEMP_FOLDER   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'temp'))
TEMP_BUILDS   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'temp/temp.xml'))
TEMP_ADDONS   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'temp/temp_installer.xml'))
KODIAPPS_FILE =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'temp/kodiapps.xml'))
BASEURL       =  base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20v')
BUILDS_API    =  BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/c2VydmljZT1idWlsZHMmYWN0aW9uPWNvdW50')
ADDONS_API    =  BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/c2VydmljZT1hZGRvbnMmYWN0aW9uPWNvdW50')
KODIAPPS_API  = base64.b64decode(b'aHR0cDovL2tvZGlhcHBzLmNvbS9lY2hvcy54bWw=')

dialog        =  xbmcgui.Dialog()
dp            =  xbmcgui.DialogProgress()
passed        =  0

dp.create(AddonTitle, "[COLOR yellowgreen][B]Connecting to the ECHO Wizard API....[/B][/COLOR]")
dp.update(0)

if os.path.exists(TEMP_FOLDER):

	try:
		shutil.rmtree(TEMP_FOLDER)
	except: pass

try:
	if not os.path.exists(TEMP_FOLDER):
		os.makedirs(TEMP_FOLDER)

	if not os.path.isfile(TEMP_BUILDS):
		open(TEMP_BUILDS, 'w')
	if not os.path.isfile(TEMP_ADDONS):
		open(TEMP_ADDONS, 'w')
	if not os.path.isfile(KODIAPPS_FILE):
		open(KODIAPPS_FILE, 'w')
except: pass
	
try:
	dp.update(25, '[COLOR yellowgreen][B]Connected![/B][/COLOR]','[COLOR white]Getting build information from the API.[/COLOR]')
	req = urllib2.Request(BUILDS_API)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
	response = urllib2.urlopen(req)
	counts=response.read()
	response.close()
	text_file = open(TEMP_BUILDS, "w")
	text_file.write(counts)
	text_file.close()

	dp.update(50, '','[COLOR white]Getting addon installer information from the API.[/COLOR]')
	req = urllib2.Request(ADDONS_API)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
	response = urllib2.urlopen(req)
	counts=response.read()
	response.close()
	text_file = open(TEMP_ADDONS, "w")
	text_file.write(counts)
	text_file.close()

	dp.update(75, '','[COLOR white]Getting Kodiapps information from the API.[/COLOR]')
	req = urllib2.Request(KODIAPPS_API)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
	response = urllib2.urlopen(req)
	counts=response.read()
	response.close()
	text_file = open(KODIAPPS_FILE, "w")
	text_file.write(counts)
	text_file.close()

	dp.update(100, '','[COLOR dodgerblue]Finishing up.[/COLOR]')
	dp.close()
	dialog.ok(AddonTitle, "We have successfully genenerated the ECHO download counters.")
	passed = 1
	quit()
except: pass
	
if passed == 0:
	dialog.ok(AddonTitle, "There was an error generating the download counters. Please try again later.")
	quit()