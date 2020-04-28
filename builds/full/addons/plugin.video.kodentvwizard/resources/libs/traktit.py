################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
import time
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta
from resources.libs import wizard as wiz

ADDON_ID       = uservar.ADDON_ID
ADDONTITLE     = uservar.ADDONTITLE
ADDON          = wiz.addonId(ADDON_ID)
DIALOG         = xbmcgui.Dialog()
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME,      'addons')
USERDATA       = os.path.join(HOME,      'userdata')
PLUGIN         = os.path.join(ADDONS,    ADDON_ID)
PACKAGES       = os.path.join(ADDONS,    'packages')
ADDONDATA      = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADDOND         = os.path.join(USERDATA,  'addon_data')
TRAKTFOLD      = os.path.join(ADDONDATA, 'trakt')
ICON           = os.path.join(PLUGIN,    'icon.png')
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
KEEPTRAKT      = wiz.getS('keeptrakt')
TRAKTSAVE      = wiz.getS('traktlastsave')
COLOR1         = uservar.COLOR1
COLOR2         = uservar.COLOR2
ORDER          = ['trakt', 'placenta', 'bubbles', 'covenant', 'elysium', 'exodus', 'genesisreborn', 'gurzil', 'meta', 'metalliq', 'neptune', 'no-name', 'numbers', 'poseidon','ProjectCypher', 'salts', 'specto', 'streamhub', 'titus', 'uranus', 'ugottoc']

TRAKTID = {
	'trakt': {
		'name'     : 'Trakt',
		'plugin'   : 'script.trakt',
		'saved'    : 'trakt',
		'path'     : os.path.join(ADDONS, 'script.trakt'),
		'icon'     : os.path.join(ADDONS, 'script.trakt', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.trakt', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'trakt_trakt'),
		'settings' : os.path.join(ADDOND, 'script.trakt', 'settings.xml'),
		'default'  : 'user',
		'data'     : ['user', 'Auth_Info', 'authorization'],
		'activate' : 'RunScript(script.trakt, action=auth_info)'},
	'placenta': {
		'name'     : 'Placenta',
		'plugin'   : 'plugin.video.placenta',
		'saved'    : 'placenta',
		'path'     : os.path.join(ADDONS, 'plugin.video.placenta'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.placenta', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.placenta', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'placenta_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.placenta', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.placenta/?action=authTrakt)'},
	'bubbles': {
		'name'     : 'Bubbles',
		'plugin'   : 'plugin.video.bubbles',
		'saved'    : 'bubbles',
		'path'     : os.path.join(ADDONS, 'plugin.video.bubbles'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.bubbles', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.bubbles', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'bubbles_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.bubbles', 'settings.xml'),
		'default'  : 'accounts.informants.trakt.user',
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.bubbles/?action=traktAuthorize)'},
	'covenant': {
		'name'     : 'Covenant',
		'plugin'   : 'plugin.video.covenant',
		'saved'    : 'covenant',
		'path'     : os.path.join(ADDONS, 'plugin.video.covenant'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.covenant', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.covenant', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'covenant_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.covenant', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.covenant/?action=authTrakt)'},
	'elysium': {
		'name'     : 'Elysium',
		'plugin'   : 'plugin.video.elysium',
		'saved'    : 'elysium',
		'path'     : os.path.join(ADDONS, 'plugin.video.elysium'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.elysium', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.elysium', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'elysium_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.elysium', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.elysium/?action=authTrakt)'},
	'exodus': {
		'name'     : 'Exodus',
		'plugin'   : 'plugin.video.exodus',
		'saved'    : 'exodus',
		'path'     : os.path.join(ADDONS, 'plugin.video.exodus'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.exodus', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.exodus', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'exodus_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.exodus', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.exodus/?action=authTrakt)'},
	'genesisreborn': {
		'name'     : 'GenesisReborn',
		'plugin'   : 'plugin.video.genesisreborn',
		'saved'    : 'genesisreborn',
		'path'     : os.path.join(ADDONS, 'plugin.video.genesisreborn'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.genesisreborn', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.genesisreborn', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'genesisreborn_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.genesisreborn', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.genesisreborn/?action=authTrakt)'},
	'gurzil': {
		'name'     : 'Gurzil',
		'plugin'   : 'plugin.video.gurzil',
		'saved'    : 'gurzil',
		'path'     : os.path.join(ADDONS, 'plugin.video.gurzil'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.gurzil', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.gurzil', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'gurzil_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.gurzil', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.gurzil/?action=authTrakt)'},
	'meta': {
		'name'     : 'Meta',
		'plugin'   : 'plugin.video.meta',
		'saved'    : 'meta',
		'path'     : os.path.join(ADDONS, 'plugin.video.meta'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.meta', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.meta', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'meta_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.meta', 'settings.xml'),
		'default'  : 'trakt_access_token',
		'data'     : ['trakt_access_token', 'trakt_refresh_token', 'trakt_expires_at'],
		'activate' : 'RunPlugin(plugin://plugin.video.meta/authenticate_trakt)'},
	'metalliq': {
		'name'     : 'MetalliQ',
		'plugin'   : 'plugin.video.metalliq',
		'saved'    : 'metalliq',
		'path'     : os.path.join(ADDONS, 'plugin.video.metalliq'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.metalliq', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.metalliq', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'metalliq_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.metalliq', 'settings.xml'),
		'default'  : 'trakt_access_token',
		'data'     : ['trakt_access_token', 'trakt_refresh_token', 'trakt_expires_at'],
		'activate' : 'RunPlugin(plugin://plugin.video.metalliq/authenticate_trakt)'},
	'neptune': {
		'name'     : 'Neptune',
		'plugin'   : 'plugin.video.neptune',
		'saved'    : 'neptune',
		'path'     : os.path.join(ADDONS, 'plugin.video.neptune'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.neptune', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.neptune', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'neptune_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.neptune', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.neptune/?action=authTrakt)'},
	'no-name': {
		'name'     : 'No-Name',
		'plugin'   : 'plugin.video.no-name',
		'saved'    : 'no-name',
		'path'     : os.path.join(ADDONS, 'plugin.video.no-name'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.no-name', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.no-name', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'no-name_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.no-name', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.no-name/?action=authTrakt)'},
	'numbers': {
		'name'     : 'Numbers',
		'plugin'   : 'plugin.video.numbers',
		'saved'    : 'numbers',
		'path'     : os.path.join(ADDONS, 'plugin.video.numbers'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.numbers', 'icon.jpg'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.numbers', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'numbers_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.numbers', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.numbers/?action=authTrakt)'},
	'poseidon': {
		'name'     : 'Poseidon',
		'plugin'   : 'plugin.video.poseidon',
		'saved'    : 'poseidon',
		'path'     : os.path.join(ADDONS, 'plugin.video.poseidon'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.poseidon', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.poseidon', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'poseidon_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.poseidon', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.poseidon/?action=authTrakt)'},
	'ProjectCypher': {
		'name'     : 'ProjectCypher',
		'plugin'   : 'plugin.video.ProjectCypher',
		'saved'    : 'ProjectCypher',
		'path'     : os.path.join(ADDONS, 'plugin.video.ProjectCypher'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.ProjectCypher', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.ProjectCypher', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'ProjectCypher_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.ProjectCypher', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.ProjectCypher/?action=authTrakt)'},		
	'salts': {
		'name'     : 'Streaming All The Sources',
		'plugin'   : 'plugin.video.salts',
		'saved'    : 'salts',
		'path'     : os.path.join(ADDONS, 'plugin.video.salts'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.salts', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.salts', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'salts_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.salts', 'settings.xml'),
		'default'  : 'trakt_user',
		'data'     : ['trakt_oauth_token', 'trakt_refresh_token', 'trakt_user'],
		'activate' : 'RunPlugin(plugin://plugin.video.salts/?mode=auth_trakt)'},
	'specto': {
		'name'     : 'Specto',
		'plugin'   : 'plugin.video.specto',
		'saved'    : 'specto',
		'path'     : os.path.join(ADDONS, 'plugin.video.specto'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.specto', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.specto', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'specto_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.specto', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.token', 'trakt.refresh'],
		'activate' : 'RunPlugin(plugin://plugin.video.specto/?action=authTrakt)'},
	'streamhub': {
		'name'     : 'Streamhub',
		'plugin'   : 'plugin.video.streamhub',
		'saved'    : 'streamhub',
		'path'     : os.path.join(ADDONS, 'plugin.video.streamhub'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.streamhub', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.streamhub', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'streamhub_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.streamhub', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.streamhub/?action=authTrakt)'},
	'titus': {
		'name'     : 'Titus',
		'plugin'   : 'plugin.video.titus',
		'saved'    : 'titus',
		'path'     : os.path.join(ADDONS, 'plugin.video.titus'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.titus', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.titus', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'titus_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.titus', 'settings.xml'),
		'default'  : 'trakt_access_token',
		'data'     : ['trakt_access_token', 'trakt_refresh_token', 'trakt_expires_at'],
		'activate' : 'RunPlugin(plugin://plugin.video.titus/authenticate_trakt)'},
	'uranus': {
		'name'     : 'Uranus',
		'plugin'   : 'plugin.video.uranus',
		'saved'    : 'uranus',
		'path'     : os.path.join(ADDONS, 'plugin.video.uranus'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.uranus', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.uranus', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'uranus_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.uranus', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.uranus/?action=authTrakt)'},		
	'ugottoc': {
		'name'     : 'Ugottoc',
		'plugin'   : 'plugin.video.ugottoc',
		'saved'    : 'ugotttoc',
		'path'     : os.path.join(ADDONS, 'plugin.video.ugottoc'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.ugottoc', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.ugottoc', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'ugottoc_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.ugottoc', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.ugottoc/?action=authTrakt)'}
}

def traktUser(who):
	user=None
	if TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['path']):
			try:
				add = wiz.addonId(TRAKTID[who]['plugin'])
				user = add.getSetting(TRAKTID[who]['default'])
			except:
				return None
	return user

def traktIt(do, who):
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(TRAKTFOLD): os.makedirs(TRAKTFOLD)
	if who == 'all':
		for log in ORDER:
			if os.path.exists(TRAKTID[log]['path']):
				try:
					addonid   = wiz.addonId(TRAKTID[log]['plugin'])
					default   = TRAKTID[log]['default']
					user      = addonid.getSetting(default)
					if user == '' and do == 'update': continue
					updateTrakt(do, log)
				except: pass
			else: wiz.log('[Trakt Data] %s(%s) is not installed' % (TRAKTID[log]['name'],TRAKTID[log]['plugin']), xbmc.LOGERROR)
		wiz.setS('traktlastsave', str(THREEDAYS))
	else:
		if TRAKTID[who]:
			if os.path.exists(TRAKTID[who]['path']):
				updateTrakt(do, who)
		else: wiz.log('[Trakt Data] Invalid Entry: %s' % who, xbmc.LOGERROR)

def clearSaved(who, over=False):
	if who == 'all':
		for trakt in TRAKTID:
			clearSaved(trakt,  True)
	elif TRAKTID[who]:
		file = TRAKTID[who]['file']
		if os.path.exists(file):
			os.remove(file)
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, TRAKTID[who]['name']),'[COLOR %s]Trakt Data: Removed![/COLOR]' % COLOR2, 2000, TRAKTID[who]['icon'])
		wiz.setS(TRAKTID[who]['saved'], '')
	if over == False: wiz.refresh()

def updateTrakt(do, who):
	file      = TRAKTID[who]['file']
	settings  = TRAKTID[who]['settings']
	data      = TRAKTID[who]['data']
	addonid   = wiz.addonId(TRAKTID[who]['plugin'])
	saved     = TRAKTID[who]['saved']
	default   = TRAKTID[who]['default']
	user      = addonid.getSetting(default)
	suser     = wiz.getS(saved)
	name      = TRAKTID[who]['name']
	icon      = TRAKTID[who]['icon']

	if do == 'update':
		if not user == '':
			try:
				with open(file, 'w') as f:
					for trakt in data: 
						f.write('<trakt>\n\t<id>%s</id>\n\t<value>%s</value>\n</trakt>\n' % (trakt, addonid.getSetting(trakt)))
					f.close()
				user = addonid.getSetting(default)
				wiz.setS(saved, user)
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Trakt Data: Saved![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Trakt Data] Unable to Update %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Trakt Data: Not Registered![/COLOR]' % COLOR2, 2000, icon)
	elif do == 'restore':
		if os.path.exists(file):
			f = open(file,mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			match = re.compile('<trakt><id>(.+?)</id><value>(.+?)</value></trakt>').findall(g)
			try:
				if len(match) > 0:
					for trakt, value in match:
						addonid.setSetting(trakt, value)
				user = addonid.getSetting(default)
				wiz.setS(saved, user)
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Trakt: Restored![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Trakt Data] Unable to Restore %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		#else: wiz.LogNotify(name,'Trakt Data: [COLOR red]Not Found![/COLOR]', 2000, icon)
	elif do == 'clearaddon':
		wiz.log('%s SETTINGS: %s' % (name, settings), xbmc.LOGDEBUG)
		if os.path.exists(settings):
			try:
				f = open(settings, "r"); lines = f.readlines(); f.close()
				f = open(settings, "w")
				for line in lines:
					match = wiz.parseDOM(line, 'setting', ret='id')
					if len(match) == 0: f.write(line)
					else:
						if match[0] not in data: f.write(line)
						else: wiz.log('Removing Line: %s' % line, xbmc.LOGNOTICE)
				f.close()
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name),'[COLOR %s]Addon Data: Cleared![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Trakt Data] Unable to Clear Addon %s (%s)" % (who, str(e)), xbmc.LOGERROR)
	wiz.refresh()

def autoUpdate(who):
	if who == 'all':
		for log in TRAKTID:
			if os.path.exists(TRAKTID[log]['path']):
				autoUpdate(log)
	elif TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['path']):
			u  = traktUser(who)
			su = wiz.getS(TRAKTID[who]['saved'])
			n = TRAKTID[who]['name']
			if u == None or u == '': return
			elif su == '': traktIt('update', who)
			elif not u == su:
				if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to save the [COLOR %s]Trakt[/COLOR] data for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "Addon: [COLOR green][B]%s[/B][/COLOR]" % u, "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B][COLOR green]Save Data[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
					traktIt('update', who)
			else: traktIt('update', who)

def importlist(who):
	if who == 'all':
		for log in TRAKTID:
			if os.path.exists(TRAKTID[log]['file']):
				importlist(log)
	elif TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['file']):
			d  = TRAKTID[who]['default']
			sa = TRAKTID[who]['saved']
			su = wiz.getS(sa)
			n  = TRAKTID[who]['name']
			f  = open(TRAKTID[who]['file'],mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			m  = re.compile('<trakt><id>%s</id><value>(.+?)</value></trakt>' % d).findall(g)
			if len(m) > 0:
				if not m[0] == su:
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to import the [COLOR %s]Trakt[/COLOR] data for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "File: [COLOR green][B]%s[/B][/COLOR]" % m[0], "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B]Save Data[/B]", nolabel="[B]No Cancel[/B]"):
						wiz.setS(sa, m[0])
						wiz.log('[Import Data] %s: %s' % (who, str(m)), xbmc.LOGNOTICE)
					else: wiz.log('[Import Data] Declined Import(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)
				else: wiz.log('[Import Data] Duplicate Entry(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)
			else: wiz.log('[Import Data] No Match(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)

def activateTrakt(who):
	if TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['path']): 
			act     = TRAKTID[who]['activate']
			addonid = wiz.addonId(TRAKTID[who]['plugin'])
			if act == '': addonid.openSettings()
			else: url = xbmc.executebuiltin(TRAKTID[who]['activate'])
		else: DIALOG.ok(ADDONTITLE, '%s is not currently installed.' % TRAKTID[who]['name'])
	else: 
		wiz.refresh()
		return
	check = 0
	while traktUser(who) == None:
		if check == 30: break
		check += 1
		time.sleep(10)
	wiz.refresh()