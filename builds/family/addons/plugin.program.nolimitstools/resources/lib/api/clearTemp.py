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
import xbmcgui, shutil, os

addon_id    = 'plugin.program.nolimitstools'
AddonTitle  = "[COLOR yellowgreen]ECHO[/COLOR] [COLOR white]Wizard[/COLOR]"
TEMP_FOLDER = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'temp'))
dialog      = xbmcgui.Dialog()
dp          = xbmcgui.DialogProgress()

dp.create(AddonTitle, "[COLOR yellowgreen]Removing ECHO Wizard temp files.[/COLOR]")

if os.path.exists(TEMP_FOLDER):
	
	try:
		shutil.rmtree(TEMP_FOLDER)
	except:
		dp.close()
		dialog.ok(AddonTitle, "There was an error removing the ECHO temp files.")
		quit()
	dp.close()
	dialog.ok(AddonTitle, "We have succesfully removed the ECHO temp files.")
	quit()

else:
	dp.close()
	dialog.ok(AddonTitle, "No temp files could be found.")
	quit()