# -*- coding: utf-8 -*-
# --[ hightimes v1.0 ]--|--[ From JewBMX ]--
# PotHead Indexer made with HighTimes podcasts so far.

import re, os, sys, urllib
import xbmcgui, xbmcplugin
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
addonFanart = control.addonFanart()
addonThumb = control.addonThumb()
artPath = control.artPath()
eDlog = xbmcgui.Dialog()


class hightimes:  # High Times Podcast Network
    def __init__(self):
        self.list = []
        self.htpn_link = 'https://hightimes.com/htpn/'
        self.artHTPN = 'https://github.com/jewbmx/xml/blob/master/img/hightimes.png?raw=true'
        self.artFreeWeed = 'https://3ncb884ou5e49t9eb3fpeur1-wpengine.netdna-ssl.com/wp-content/uploads/2018/06/Free-Weed-Danny-1.jpg'


    def root(self):
        self.addDirectoryItem('High Times Podcast Network - FreeWeed', 'getFreeWeed', self.artFreeWeed, 'DefaultVideoPlaylists.png')
        self.endDirectory()


    def getFreeWeed(self):
        try:
            html = client.request(self.htpn_link)
            shows = re.compile('<iframe.+?src="(.+?)"').findall(html)
            for url in shows:
                if not 'player.pippa.io' in url:
                    continue
                html = client.request(url)
                regex = ',"title":"(.+?)","duration":(.+?),"audio":"(.+?)","cover":"(.+?)"'
                channels = re.compile(regex, flags=re.DOTALL|re.IGNORECASE).findall(html)
                for title, info, url, art in channels:
                    art =  "https:" + art if not art.startswith('http') else art
                    self.list.append({'name': title, 'url': url, 'description': info, 'image': art, 'action': 'highPlay'})
            self.addDirectory(self.list)
        except Exception as e:
            eDlog.notification('[B]HighTimes Error[/B]', str(e), xbmcgui.NOTIFICATION_INFO, 5000)
            log_utils.log('HighTimes Exception - ' + str(e))
            pass


    def play(self, url):
        try:
            control.execute('PlayMedia(%s)' % url)
        except Exception as e:
            eDlog.notification('[B]HighTimes Error[/B]', str(e), xbmcgui.NOTIFICATION_INFO, 5000)
            log_utils.log('HighTimes Exception - ' + str(e))
            return


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
                    except:
                        pass
                    item.setProperty('IsPlayable', 'false')
                else:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % i['url']
                    except:
                        pass
                    item.setProperty('IsPlayable', 'true')
                    item.setInfo("mediatype", "video")
                    item.setInfo("audio", '')
                item.setArt({'icon': thumb, 'thumb': thumb})
                if addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
            except:
                pass
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        if thumb.startswith('http'):
            thumb = thumb
        else:
            thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if queue == True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if not context == None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)


    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


"""

#############                                #############
#######################################
#############                               #############


# https://toppodcast.com/podcast_feeds/the-delic/


#############                                #############
#######################################
#############                               #############


plugin://plugin.video.youtube/user/HIGHTIMESPresents/
https://m.youtube.com/channel/UCFQ7vc-dWlSUZd6OqsAepMA
https://m.youtube.com/playlist?list=OLAK5uy_kJvc0BXqeyWaH5kmzkT48FbVwwAmbxPMc


#############                                #############
#######################################
#############                               #############


https://tv.hightimes.com/searchs?q=OG
https://tv.hightimes.com/pages/home/d/explore
https://tv.hightimes.com/channels/details/series_1

https://tv.hightimes.com/series/59aacwBBs1ke-farm-to-table-cannabis-with-the-hydroponic-chef/details?channel=series_1
https://tv.hightimes.com/watch/channel/series_1/series/59aacwBBs1ke-farm-to-table-cannabis-with-the-hydroponic-chef/episode/AGulPx9vmUTM-farm-to-table-cannabis---episode-1

https://tv.hightimes.com/pages/guide/dir/creators
https://tv.hightimes.com/channels/details/harry-dabs


#############                                #############
#######################################
#############                               #############

"""

