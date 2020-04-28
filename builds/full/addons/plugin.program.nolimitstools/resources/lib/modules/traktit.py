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
import time
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta

from resources.lib.modules import uservar
from resources.lib.modules import wizard as wiz

ADDONTITLE     = uservar.ADDONTITLE
ADDON_ID       = uservar.ADDON_ID
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
ORDER          = ['anarchy', 'bubbles', 'covenant', 'death', 'exodus', 'exoshark', 'gurzil', 'metalliq', 'neptune', 'notsure', 'piranha', 'poseidon', 'resistance', 'salts', 'saltshd', 'saltsrd', 'specto', 'streamhub', 'thedelorean', 'trakt', 'ugottoc', 'wtfork']

TRAKTID = { 
	'anarchy': {
		'name'     : 'AnArchy',
		'plugin'   : 'plugin.video.AnArchy',
		'saved'    : 'anarchy',
		'path'     : os.path.join(ADDONS, 'plugin.video.AnArchy'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.AnArchy', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.AnArchy', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'anarchy_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.AnArchy', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.AnArchy/?action=authTrakt)'},
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
		'data'     : ['accounts.informants.trakt.enabled', 'accounts.informants.trakt.notifications', 'accounts.informants.trakt.refresh', 'accounts.informants.trakt.token', 'accounts.informants.trakt.user', 'accounts.informants.trakt.watched'],
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
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.covenant/?action=authTrakt)'},
	'death': {
		'name'     : 'Death Streams',
		'plugin'   : 'plugin.video.blamo',
		'saved'    : 'death',
		'path'     : os.path.join(ADDONS, 'plugin.video.blamo'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.blamo', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.blamo', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'death_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.blamo', 'settings.xml'),
		'default'  : 'trakt_user',
		'data'     : ['trakt_bookmark', 'trakt_oauth_token', 'trakt_offline', 'trakt_refresh_token', 'trakt_timeout', 'trakt_user'],
		'activate' : 'RunPlugin(plugin://plugin.video.blamo/?mode=auth_trakt)'},
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
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.exodus/?action=authTrakt)'},
	'exoshark': {
		'name'     : 'ExoShark',
		'plugin'   : 'plugin.video.exoshark',
		'saved'    : 'exoshark',
		'path'     : os.path.join(ADDONS, 'plugin.video.exoshark'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.exoshark', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.exoshark', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'exoshark_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.exoshark', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.exoshark/?action=authTrakt)'},
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
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.gurzil/?action=authTrakt)'},
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
		'data'     : ['trakt_access_token', 'trakt_api_client_id', 'trakt_api_client_secret', 'trakt_expires_at', 'trakt_period', 'trakt_refresh_token'],
		'activate' : 'RunPlugin(plugin://plugin.video.metalliq/authenticate_trakt)'},
	'neptune': {
		'name'     : 'Neptune Rising',
		'plugin'   : 'plugin.video.neptune',
		'saved'    : 'neptune',
		'path'     : os.path.join(ADDONS, 'plugin.video.neptune'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.neptune', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.neptune', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'neptune_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.neptune', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.neptune/?action=authTrakt)'},
	'notsure': {
		'name'     : 'Not Sure',
		'plugin'   : 'plugin.video.sedundnes',
		'saved'    : 'notsure',
		'path'     : os.path.join(ADDONS, 'plugin.video.sedundnes'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.sedundnes', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.sedundnes', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'notsure_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.sedundnes', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.sedundnes/?action=authTrakt)'},
	'piranha': {
		'name'     : 'Piranha',
		'plugin'   : 'plugin.video.piranha',
		'saved'    : 'piranha',
		'path'     : os.path.join(ADDONS, 'plugin.video.piranha'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.piranha', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.piranha', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'piranha_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.piranha', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.piranha/?action=authTrakt)'},
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
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.poseidon/?action=authTrakt)'},
	'resistance': {
		'name'     : 'Resistance',
		'plugin'   : 'plugin.video.resistance',
		'saved'    : 'resistance',
		'path'     : os.path.join(ADDONS, 'plugin.video.resistance'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.resistance', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.resistance', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'resistance_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.resistance', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.resistance/?action=authTrakt)'},
	'salts': {
		'name'     : 'Salts',
		'plugin'   : 'plugin.video.salts',
		'saved'    : 'salts',
		'path'     : os.path.join(ADDONS, 'plugin.video.salts'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.salts', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.salts', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'salts_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.salts', 'settings.xml'),
		'default'  : 'trakt_user',
		'data'     : ['trakt_bookmark', 'trakt_oauth_token', 'trakt_offline', 'trakt_refresh_token', 'trakt_timeout', 'trakt_user'],
		'activate' : 'RunPlugin(plugin://plugin.video.salts/?mode=auth_trakt)'},
	'saltshd': {
		'name'     : 'Salts HD Lite',
		'plugin'   : 'plugin.video.saltshd.lite',
		'saved'    : 'saltshd',
		'path'     : os.path.join(ADDONS, 'plugin.video.saltshd.lite'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.saltshd.lite', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.saltshd.lite', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'saltshd_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.saltshd.lite', 'settings.xml'),
		'default'  : 'trakt_user',
		'data'     : ['trakt_bookmark', 'trakt_oauth_token', 'trakt_offline', 'trakt_refresh_token', 'trakt_timeout', 'trakt_user'],
		'activate' : 'RunPlugin(plugin://plugin.video.saltshd.lite/?mode=auth_trakt)'},
	'saltsrd': {
		'name'     : 'Salts RD Lite',
		'plugin'   : 'plugin.video.saltsrd.lite',
		'saved'    : 'saltsrd',
		'path'     : os.path.join(ADDONS, 'plugin.video.saltsrd.lite'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.saltsrd.lite', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.saltsrd.lite', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'saltsrd_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.saltsrd.lite', 'settings.xml'),
		'default'  : 'trakt_user',
		'data'     : ['trakt_bookmark', 'trakt_oauth_token', 'trakt_offline', 'trakt_refresh_token', 'trakt_timeout', 'trakt_user'],
		'activate' : 'RunPlugin(plugin://plugin.video.saltsrd.lite/?mode=auth_trakt)'},
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
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.specto/?action=authTrakt)'},
	'streamhub': {
		'name'     : 'StreamHub',
		'plugin'   : 'plugin.video.streamhub',
		'saved'    : 'streamhub',
		'path'     : os.path.join(ADDONS, 'plugin.video.streamhub'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.streamhub', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.streamhub', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'streamhub_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.streamhub', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.streamhub/?action=authTrakt)'},
	'thedelorean': {
		'name'     : 'The DeLorean',
		'plugin'   : 'plugin.video.TheDeLorean',
		'saved'    : 'thedelorean',
		'path'     : os.path.join(ADDONS, 'plugin.video.TheDeLorean'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.TheDeLorean', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.TheDeLorean', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'TheDeLorean_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.TheDeLorean', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.TheDeLorean/?action=authTrakt)'},
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
		'data'     : ['authorization', 'user'],
		'activate' : 'RunScript(script.trakt, action=auth_info)'},
	'ugottoc': {
		'name'     : 'UGOTTOC',
		'plugin'   : 'plugin.video.ugottoc',
		'saved'    : 'ugottoc',
		'path'     : os.path.join(ADDONS, 'plugin.video.ugottoc'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.ugottoc', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.ugottoc', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'ugottoc_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.ugottoc', 'settings.xml'),
		'default'  : 'trakt_account',
		'data'     : ['trakt_account', 'trakt_authorized', 'trakt_client_id', 'trakt_oauth_token', 'trakt_offline_mode', 'trakt_refresh_token', 'trakt_secret'],
		'activate' : 'RunPlugin(plugin://plugin.video.ugottoc/?mode=authorize_trakt)'},
	'wtfork': {
		'name'     : 'What The Fork?',
		'plugin'   : 'plugin.video.wtfork',
		'saved'    : 'wtfork',
		'path'     : os.path.join(ADDONS, 'plugin.video.wtfork'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.wtfork', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.wtfork', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'wtfork_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.wtfork', 'settings.xml'),
		'default'  : 'trakt_user',
		'data'     : ['trakt_bookmark', 'trakt_oauth_token', 'trakt_offline', 'trakt_refresh_token', 'trakt_timeout', 'trakt_user'],
		'activate' : 'RunPlugin(plugin://plugin.video.wtfork/?mode=auth_trakt)'}
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
			else: wiz.log('[Trakt Info] %s(%s) is not installed' % (TRAKTID[log]['name'],TRAKTID[log]['plugin']), xbmc.LOGERROR)
		wiz.setS('traktlastsave', str(THREEDAYS))
	else:
		if TRAKTID[who]:
			if os.path.exists(TRAKTID[who]['path']):
				updateTrakt(do, who)
		else: wiz.log('[Trakt Info] Invalid Entry: %s' % who, xbmc.LOGERROR)

def clearSaved(who, over=False):
	if who == 'all':
		for trakt in TRAKTID:
			clearSaved(trakt,  True)
	elif TRAKTID[who]:
		file = TRAKTID[who]['file']
		if os.path.exists(file):
			os.remove(file)
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, TRAKTID[who]['name']),'[COLOR %s]Trakt Info: Removed![/COLOR]' % COLOR2, 2000, TRAKTID[who]['icon'])
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
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Trakt Info: Saved![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Trakt Info] Unable to Update %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Trakt Info: Not Registered![/COLOR]' % COLOR2, 2000, icon)
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
				wiz.log("[Trakt Info] Unable to Restore %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		#else: wiz.LogNotify(name,'Trakt Info: [COLOR red]Not Found![/COLOR]', 2000, icon)
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
				wiz.log("[Trakt Info] Unable to Clear Addon %s (%s)" % (who, str(e)), xbmc.LOGERROR)
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
				if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to save the [COLOR %s]Trakt[/COLOR] data for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "Addon: [COLOR green][B]%s[/B][/COLOR]" % u, "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B][COLOR %s]Save Trakt[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]No, Cancel[/COLOR][/B]" % COLOR1):
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
					if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to import the [COLOR %s]Trakt[/COLOR] data for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "File: [COLOR green][B]%s[/B][/COLOR]" % m[0], "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B]Import Trakt[/B]", nolabel="[B]No, Cancel[/B]"):
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
		else: DIALOG.ok("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '%s is not currently installed.' % TRAKTID[who]['name'])
	else: 
		wiz.refresh()
		return
	check = 0
	while traktUser(who) == None:
		if check == 30: break
		check += 1
		time.sleep(10)
	wiz.refresh()