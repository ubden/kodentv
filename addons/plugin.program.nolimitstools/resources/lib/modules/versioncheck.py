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

ADDONTITLE = "[COLOR aqua]No Limits[/COLOR] [COLOR white]Tools[/COLOR]"
dialog     = xbmcgui.Dialog()

#---------------------------------------------------------------------------------------------------
#Report back with the version of Kodi installed
def XBMC_Version():
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])

    if version >= 11.0 and version <= 11.9:
		codename = 'Eden'
    if version >= 12.0 and version <= 12.9:
		codename = 'Frodo'
    if version >= 13.0 and version <= 13.9:
		codename = 'Gotham'
    if version >= 14.0 and version <= 14.9:
		codename = 'Helix'
    if version >= 15.0 and version <= 15.9:
		codename = 'Isengard'
    if version >= 16.0 and version <= 16.9:
		codename = 'Jarvis'
    if version >= 17.0 and version <= 17.9:
		codename = 'Krypton'
    if version >= 18.0 and version <= 18.9:
		codename = 'Leia'
	
    if version >= 16:
		dialog=xbmcgui.Dialog()
		dialog.ok(ADDONTITLE, "[COLOR green][B]CONGRATULATIONS![/B][/COLOR]","Your version is: Kodi %s" % version + " " + codename, "You can install a No Limits Build on this system!")
    else:
		dialog=xbmcgui.Dialog()
		dialog.ok(ADDONTITLE, "[COLOR lightskyblue][B]SORRY![/B][/COLOR]","Your version is: Kodi %s" % version, "You cannot install a no Limits Build on this system!")

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#Report back with the version of Kodi installed
def BUILD_Version():
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])

    if version >= 11.0 and version <= 11.9:
		codename = 'Eden'
		dialog.ok(ADDONTITLE, "[COLOR smokewhite][B]Which should I choose? - Jarvis or Krypton?![/B][/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "Sorry no builds can be installed on this system! Please update your Kodi installation to 16 Jarvis or 17 Krypton to use a No Limits Build.")
    if version >= 12.0 and version <= 12.9:
		codename = 'Frodo'
		dialog.ok(ADDONTITLE, "[COLOR smokewhite][B]Which should I choose? - Jarvis or Krypton?![/B][/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "Sorry no builds can be installed on this system! Please update your Kodi installation to 16 Jarvis or 17 Krypton to use a No Limits Build.")
    if version >= 13.0 and version <= 13.9:
		codename = 'Gotham'
		dialog.ok(ADDONTITLE, "[COLOR smokewhite][B]Which should I choose? - Jarvis or Krypton?![/B][/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "Sorry no builds can be installed on this system! Please update your Kodi installation to 16 Jarvis or 17 Krypton to use a No Limits Build.")
    if version >= 14.0 and version <= 14.9:
		codename = 'Helix'
		dialog.ok(ADDONTITLE, "[COLOR smokewhite][B]Which should I choose? - Jarvis or Krypton?![/B][/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "Sorry no builds can be installed on this system! Please update your Kodi installation to 16 Jarvis or 17 Krypton to use a No Limits Build.")
    if version >= 15.0 and version <= 15.9:
		codename = 'Isengard'
		dialog.ok(ADDONTITLE, "[COLOR smokewhite][B]Which should I choose? - Jarvis or Krypton?![/B][/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "Sorry no builds can be installed on this system! Please update your Kodi installation to 16 Jarvis or 17 Krypton to use a No Limits Build.")
    if version >= 16.0 and version <= 16.9:
		codename = 'Jarvis'
		dialog.ok(ADDONTITLE, "[COLOR smokewhite]Which should I choose? [/COLOR][COLOR white]- Jarvis or Krypton?[/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "You should install a [B][COLOR yellowgreen]Jarvis[/B][/COLOR] build on this system!")
    if version >= 17.0 and version <= 17.9:
		codename = 'Krypton'
		dialog.ok(ADDONTITLE, "[COLOR smokewhite]Which should I choose? - Jarvis or Krypton?[/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "You should install a [B][COLOR aqua]Krypton[/B][/COLOR] build on this system!")
    if version >= 18.0 and version <= 18.9:
		codename = 'Leia'
		dialog.ok(ADDONTITLE, "[COLOR smokewhite]Which should I choose? - Jarvis or Krypton?[/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "You should install a [B][COLOR aqua]Krypton[/B][/COLOR] build on this system!")
#---------------------------------------------------------------------------------------------------