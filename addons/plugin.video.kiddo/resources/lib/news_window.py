"""
    All original work on this module credited to Les][smor

    service.py for Jen Template
    Copyright (C) 2018

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

    -------------------------------------------------------------

    Version:
        2018-11-15:
            Updated for working with local files in addon path structure
            Path used in settings.xml for local is like below example:
                default="file://updates.txt" - When in Root Folder of addon
                default="file://xml/updates.xml" - When in XML folder of addon
            Putting the string $version$ in your file will cause the module to insert
                the version of the addon in that position
            Putting the string $changelog$ in your file will look for a changelog.txt in
                the top folder of your addon and insert it's contents in that position.

        2018-05-21:
            Updated to be self updating via settings.xml - NO Need To Change This File Anymore
            Takes into account if end-user API keys are stored in settings, and doesn't update it
                if they are.

        2018-05-19:
            Updated documentation in Header
            Added ability to disable service after updating API Keys (reduces load on Kodi startup)
            Removed old stuff


    Usage:
        Set this in your Jen v1.6 or higher and it should keep your end user's API Keys and Root XML
            in order automatically. Takes into account when user's have entered their own API keys



"""

import os
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import koding
from koding import Download
from koding import route, Run


addon_id = xbmcaddon.Addon().getAddonInfo('id')
ownAddon = xbmcaddon.Addon(id=addon_id)
message_xml_url = ownAddon.getSetting('http://cellardoortv.com/kiddo/message/message.xml')


@route(mode="dialog_example")
def Dialog_Example():

    koding_test = message_xml_url
    if 'file' in koding_test:
        temp = xbmc.translatePath(('special://home/addons/%s' % (addon_id)))
        koding_test = os.path.join(temp, koding_test.replace('file://', '')).decode('utf-8')
    main_text = koding.Text_File(path=koding_test, mode='r')
    main_text = main_text.replace('$version$', str(ownAddon.getAddonInfo('version')))
    if '$changelog$' in main_text:
        temp = xbmc.translatePath(('special://home/addons/%s' % (addon_id)))
        koding_test = os.path.join(temp, 'changelog.txt').decode('utf-8')
        changelog = koding.Text_File(path=koding_test, mode='r')
        main_text = main_text.replace('$changelog$', changelog)

    my_buttons = ['Close']
    my_choice = koding.Custom_Dialog(
        main_content=main_text, pos='center', size='900x600', buttons=my_buttons, transparency=90,
        highlight_color='yellow', header='Latest News')
    if my_choice == 0:
        return
