#   script.ezmaintenance
#   Copyright (C) 2016  SchisM
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import controlstartup as control
packagesdir    =  xbmc.translatePath(os.path.join('special://home/addons/packages',''))
thumbnails    =  xbmc.translatePath('special://home/userdata/Thumbnails')
dialog = xbmcgui.Dialog()
setting = xbmcaddon.Addon().getSetting
iconpath = xbmc.translatePath(os.path.join('special://home/addons/script.clean','icon.png'))
# if setting('autoclean') == 'true':
	# control.clearCache()
filesize = int(setting('filesize_alert'))
filesize_thumb = int(setting('filesizethumb_alert'))
maxpackage_zips = int(setting('packagenumbers_alert'))
print("MAINTENANCE SETTINGS", maxpackage_zips, filesize, filesize_thumb)
total_size2 = 0
total_size = 0
count = 0
for dirpath, dirnames, filenames in os.walk(packagesdir):
	count = 0
	for f in filenames:
		count += 1
		fp = os.path.join(dirpath, f)
		total_size += os.path.getsize(fp)
total_sizetext = "%.0f" % (total_size/1024000.0)
	
if count > maxpackage_zips or int(total_sizetext) > filesize:
	choice2 = xbmcgui.Dialog().yesno("[COLOR=silver]Autocleaner[/COLOR]", 'The packages folder is [COLOR silver]' + str(total_sizetext) +' MB [/COLOR] - [COLOR silver]' + str(count) + '[/COLOR] zip files', 'The folder can be cleaned up without issues to save space...', 'Do you want to clean it now?', yeslabel='Yes',nolabel='No')
	if choice2 == 1:
		control.purgePackages()
			
for dirpath2, dirnames2, filenames2 in os.walk(thumbnails):
	for f2 in filenames2:
		fp2 = os.path.join(dirpath2, f2)
		total_size2 += os.path.getsize(fp2)
total_sizetext2 = "%.0f" % (total_size2/1024000.0)

if int(total_sizetext2) > filesize_thumb:
	choice2 = xbmcgui.Dialog().yesno("[COLOR=silver]Autocleaner[/COLOR]", 'The images folder is [COLOR silver]' + str(total_sizetext2) + ' MB   [/COLOR]', 'The folder can be cleaned up without issues to save space...', 'Do you want to clean it now?', yeslabel='Yes',nolabel='No')
	if choice2 == 1:
		control.deleteThumbnails()

xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % ('Maintenance Status',  'Packages: '+ str(total_sizetext) +  ' MB'  ' - Images: ' + str(total_sizetext2) + ' MB' , '5000', iconpath))