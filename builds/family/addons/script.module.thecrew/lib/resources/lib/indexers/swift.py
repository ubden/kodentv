# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    -Mofidied by The Crew
    -Copyright (C) 2019 The Crew


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import json
import os
import requests
import sys
import time
import traceback
import urllib

# from Cryptodome.Cipher import AES
from hashlib import md5
from binascii import b2a_hex

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.modules import client, control, log_utils, pyaes

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
artPath = control.artPath()
addonIcon = control.addonIcon()
addonFanart = control.addonFanart()


class swift:
    def __init__(self):
        self.User_Agent = 'okhttp/3.10.0'
        self.Play_User_Agent = 'Lavf/56.15.102'

        self.base_api_url = 'http://swiftstreamz.com/SwiftPanel/api.php?get_category'
        self.base_dta_url = 'http://swiftstreamz.com/SwiftPanel/swiftlive.php'
        self.base_cat_url = 'http://swiftstreamz.com/SwiftPanel/api.php?get_channels_by_cat_id=%s'

        self.filter_mov = control.setting('tv.swift.filtermov')
        self.filter_spo = control.setting('tv.swift.filtersports')
        self.filter_tvl = control.setting('tv.swift.filtertv')

    def root(self):
        headers = {'Authorization': 'Basic U3dpZnRTdHJlYW16OkBTd2lmdFN0cmVhbXpA', 'User-Agent': self.User_Agent}
        response = client.request(self.base_api_url, headers=headers)
        if 'Erreur 503' in str(response):
            self.addDirectoryItem('[B]System down for maintenance[/B]',
                                  'sectionItem', 'tools.png', 'DefaultTvShows.png')
        else:
            response = json.loads(response)
            for a in response['LIVETV']:
                try:
                    name = a['category_name']
                    if self.filter_mov == 'true' and ' mov' in name.lower():
                        continue
                    if self.filter_spo == 'true' and 'sports' in name.lower():
                        continue
                    if self.filter_tvl == 'true' and ' tv' in name.lower():
                        continue
                    id = a['cid']
                    icon = a['category_image']
                    self.addDirectoryItem(name, 'swiftCat&url=%s' % (id), icon, 'DefaultTvShows.png')
                except Exception:
                    pass
        self.endDirectory(sortMethod=xbmcplugin.SORT_METHOD_LABEL)

    def swiftCategory(self, id):
        url = self.base_cat_url % (id)
        headers = {'Authorization': 'Basic @Swift11#:@Swift11#', 'User-Agent': self.User_Agent}
        response = client.request(url, headers=headers)

        items = []
        try:
            if 'Erreur 503' in str(response):
                self.addDirectoryItem('[B]System down for maintenance[/B]',
                                      'sectionItem', 'tools.png', 'DefaultTvShows.png')
            else:
                response = json.loads(response)
                for a in response['LIVETV']:
                    streams = []
                    for entry in a['stream_list']:
                        if '.m3u8' in entry['stream_url'] or '.2ts' in entry['stream_url']:
                            streams.append(entry)

                    if len(streams) == 0:
                        continue

                    name = a['channel_title']
                    icon = a['channel_thumbnail']

                    # For now, just supporting the first stream, even when multiple available. Cuz I am fat and lazy
                    url = streams[0]['stream_url']
                    token = streams[0]['token']

                    playencode = '%s|%s|%s' % (name, url, token)

                    item = control.item(label=name)
                    item.setProperty("IsPlayable", "true")
                    item.setArt({"thumb": icon, "icon": icon})
                    item.setInfo(type="video", infoLabels={"Title": name, "mediatype": "video"})
                    try:
                        item.setContentLookup(False)
                    except AttributeError:
                        pass
                    url = '%s?action=swiftPlay&url=%s' % (sysaddon, playencode.encode('base64'))

                    items.append((url, item, False))
                control.addItems(syshandle, items)
        except Exception:
            pass

        self.endDirectory('files', xbmcplugin.SORT_METHOD_LABEL)

    def swiftPlay(self, url):
        url = url.decode('base64')
        tmp = url.split('|', 2)
        title = tmp[0]
        url = tmp[1]
        token = tmp[2]

        data = {"data": get_post_data()}
        token_url = 'http://swiftstreamz.com/newapptoken%s.php' % (token)
        get_token = requests.post(token_url, headers={"User-Agent": self.User_Agent}, data=data, timeout=10)
        auth_token = get_token.text.partition('=')[2]

        auth_token = "".join(
            [
                auth_token[:-59],
                auth_token[-58:-47],
                auth_token[-46:-35],
                auth_token[-34:-23],
                auth_token[-22:-11],
                auth_token[-10:],
            ]
        )
        try:
            url = url + '?wmsAuthSign=' + auth_token + '|User-Agent=%s' % (self.Play_User_Agent)

            item = control.item(title, path=url)
            item.setArt({"thumb": addonIcon, "icon": addonIcon})
            item.setInfo(type="video", infoLabels={"Title": title})
            item.setProperty('IsPlayable', 'true')

            if 'playlist.m3u8' in url or '.2ts' in url:
                inputstream = control.setting('tv.swift.inputstream')
                if inputstream == '' or inputstream == 'true':
                    item.setMimeType("application/vnd.apple.mpegurl")
                    item.setProperty("inputstreamaddon", "inputstream.adaptive")
                    item.setProperty("inputstream.adaptive.manifest_type", "hls")
                    item.setProperty("inputstream.adaptive.stream_headers", url.split("|")[-1])
                else:
                    item.setMimeType("application/vnd.apple.mpegurl")
            else:
                item.setMimeType("video/x-mpegts")

            try:
                item.setContentLookup(False)
            except AttributeError:
                pass
            xbmcplugin.setResolvedUrl(handle=syshandle, succeeded=True, listitem=item)
        except Exception:
            from resources.lib.dialogs import ok
            ok.load('Connection Error', '[B]Error finding streams. Try again later.[/B]')
            failure = traceback.format_exc()
            log_utils.log('Swift Streamz - Exception: \n' + str(failure))
            return

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except Exception:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction is True else query
        if 'http' not in thumb:
            thumb = os.path.join(artPath, thumb) if artPath is not None else icon
        cm = []

        queueMenu = control.lang(32065).encode('utf-8')

        if queue is True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if context is not None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if addonFanart is not None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self, contentType='addons', sortMethod=xbmcplugin.SORT_METHOD_NONE):
        control.content(syshandle, contentType)
        sort_the_crew = control.setting('tv.swift.sort_the_crew')
        if sort_the_crew == '' or sort_the_crew == 'true':
            control.sortMethod(syshandle, xbmcplugin.SORT_METHOD_LABEL)
        else:
            control.sortMethod(syshandle, sortMethod)
        control.directory(syshandle, cacheToDisc=True)

    def addDirectory(self, items, queue=False, isFolder=True):
        if items is None or len(items) is 0:
            control.idle()
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif artPath is not None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                item = control.item(label=name)

                if isFolder:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % urllib.quote_plus(i['url'])
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'false')
                else:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % i['url']
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'true')
                    item.setInfo("mediatype", "video")
                    item.setInfo("audio", '')

                item.setArt({'icon': thumb, 'thumb': thumb})
                if addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
            except Exception:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


def get_post_data():
    _key = b"cLt3Gp39O3yvW7Gw"
    _iv = b"bRRhl2H2j7yXmuk4"
    cipher = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(_key, _iv))
    ciphertext = ''
    _time = str(int(time.time()))
    _hash = md5("{0}e31Vga4MXIYss1I0jhtdKlkxxwv5N0CYSnCpQcRijIdSJYg".format(_time).encode("utf-8")).hexdigest()
    _plain = "{0}&{1}".format(_time, _hash).ljust(48).encode("utf-8")
    ciphertext += cipher.feed(_plain)
    ciphertext += cipher.feed()
    return b2a_hex(ciphertext[:-16]).decode("utf-8")