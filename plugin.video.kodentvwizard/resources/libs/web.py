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
#import time
import xbmc
#import os
#import xbmcgui
#import urllib2
import webbrowser
import base64

BASEURL = base64.b64decode('aHR0cHM6Ly93d3cudWJkZW4uY29t')
DONATIONS_URL1   = 'http://www.ubden.com'
DONATIONS_URL2   = 'http://www.ubden.com'
DONATIONS_URL3   = 'http://www.ubden.com'

def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'

myplatform = platform()


def function27():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( DONATIONS_URL1 ) )
    else:
        opensite = webbrowser . open( DONATIONS_URL1 )
        
def function28():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( DONATIONS_URL2 ) )
    else:
        opensite = webbrowser . open( DONATIONS_URL2 )

def function29():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( DONATIONS_URL3 ) )
    else:
        opensite = webbrowser . open( DONATIONS_URL3 )