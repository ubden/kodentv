# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# @tantrumdev wrote this file.  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

import os,sys,urllib,urlparse,json,random
import traceback,xbmcgui,xbmcplugin
from resources.lib.modules import control,log_utils
from urllib2 import urlopen, Request

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
artPath = control.artPath()
addonFanart = control.addonFanart()


class radionet:
    USER_AGENT = 'XBMC Addon Radio'
    PLAYLIST_PREFIXES = ('m3u', 'pls', 'asx', 'xml')


    def __init__(self):
        self.user_agent = 'XBMC Addon Radio'
        self.country = control.setting('radio.country').lower()
        self.station_count = int(float(control.setting('radio.count')))
        self.austria_link = 'https://radio.at/info/'
        self.brazil_link = 'https://br.radio.net/info/'
        self.columbia_link = 'https://co.radio.net/info/'
        self.denamrk_link = 'https://radio.dk/info/'
        self.france_link = 'https://radio.fr/info/'
        self.germany_link = 'http://radio.de/info/'
        self.italy_link = 'https://radio.it/info/'
        self.mexico_link = 'https://mx.radio.net/info/'
        self.poland_link = 'https://radio.pl/info/'
        self.portugal_link = 'https://radio.pt/info/'
        self.spain_link = 'https://radio.es/info/'
        self.sweden_link = 'https://radio.se/info/'
        self.usa_link = 'http://rad.io/info/'
        self.localstations_path = {'path': 'account/getmostwantedbroadcastlists', 'param': {'sizeoflists': self.station_count}}
        self.recommended_path = {'path': 'broadcast/editorialreccomendationsembedded', 'param': None}
        self.tophundred_path = {'path': 'menu/broadcastsofcategory', 'param': {'category': '_top'}}
        self.genre_path = {'path': 'menu/valuesofcategory', 'param': {'category': '_genre'}}
        self.topic_path = {'path': 'menu/valuesofcategory', 'param': {'category': '_topic'}}
        self.country_path = {'path': 'menu/valuesofcategory', 'param': {'category': '_country'}}
        self.city_path = {'path': 'menu/valuesofcategory', 'param': {'category': '_city'}}
        self.language_path = {'path': 'menu/valuesofcategory', 'param': {'category': '_language'}}
        self.category_path = {'path': 'menu/broadcastsofcategory', 'param': None}
        self.categories = ('genre', 'topic', 'country', 'city', 'language')
        self.base_link = getattr(self, self.country + '_link')


    def root(self):
        try:
            self.addDirectoryItem('localstations', 'radio&url=localstations', 'airing-today.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem('recommended', 'radio&url=recommended', 'airing-today.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem('tophundred', 'radio&url=tophundred', 'airing-today.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem('language', 'radioCat&url=language', 'airing-today.png', 'DefaultVideoPlaylists.png')
            self.endDirectory()
        except Exception:
            pass


    def get_stations(self, url):
        try:
            tmp = getattr(self, url + '_path')
            path = tmp['path']
            param = tmp['param']
            stations = self.__radio_get(path, param)
            if 'localstations' == url:
                for local_station in stations['localBroadcasts']:
                    self.addStationToDirectory(local_station)
            else:
                for station in stations:
                    self.addStationToDirectory(station)
            self.endDirectory()
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Radio get_stations - Exception: \n' + str(failure))
            pass


    def get_categories(self, url):
        try:
            tmp = getattr(self, url + '_path')
            path = tmp['path']
            param = tmp['param']
            categories = self.__radio_get(path, param)
            for category in categories:
                item = '_%s|%s' % (url, category)
                item = item.encode('base64')
                self.addDirectoryItem(category, 'radioCatStations&url=%s' % (item), 'languages.png', 'DefaultVideoPlaylists.png')
            self.endDirectory()
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Radio get_categories - Exception: \n' + str(failure))
            pass


    def get_category_stations(self, url):
        try:
            path = self.category_path['path']
            tmp = url.decode('base64').split('|')
            param = {'category': '%s' % tmp[0], 'value': tmp[1],}
            stations = self.__radio_get(path, param)
            for station in stations:
                self.addStationToDirectory(station)
            self.endDirectory()
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Radio get_category_stations - Exception: \n' + str(failure))
            pass


    @staticmethod
    def __format_stations(stations):
        formated_stations = []
        for station in stations:
            thumbnail = (station.get('picture4TransName') or station.get('picture4Name') or station.get('picture1TransName').replace('_1_', '_4_') or station.get('picture1Name').replace('_1_', '_4_'))
            genre = station.get('genresAndTopics') or ','.join(station.get('genres', []) + station.get('topics', []),)
            formated_stations.append({'name': station['name'], 'thumbnail': station['pictureBaseURL'] + thumbnail, 'rating': station['rating'], 'genre': genre, 'bitrate': station['bitrate'], 'id': station['id'], 'current_track': station['currentTrack'], 'stream_url': station.get('streamURL', ''), 'description': station.get('description', '')})
        return formated_stations


    @staticmethod
    def __check_redirect(stream_url):
        if 'addrad.io' in stream_url:
            return True
        if '.nsv' in stream_url:
            return True
        return False


    @staticmethod
    def __check_paylist(stream_url):
        prefixes = ('m3u', 'pls', 'asx', 'xml')
        for prefix in prefixes:
            if stream_url.lower().endswith(prefix):
                return True
        return False


    def __radio_get(self, path, param=None):
        try:
            url = urlparse.urljoin(self.base_link, path)
            if param:
                url += '?%s' % urllib.urlencode(param)
            response = self.__urlopen(url)
            json_data = json.loads(response)
            return json_data
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Radio __URLOPEN - Exception: \n' + str(failure))
            return None


    def __urlopen(self, url):
        req = Request(url)
        req.add_header('User-Agent', self.user_agent)
        try:
            response = urlopen(req).read()
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Radio __URLOPEN - Exception: \n' + str(failure))
        return response


    def get_station_by_station_id(self, station_id, resolve_playlists=True):
        path = 'broadcast/getbroadcastembedded'
        param = {'broadcast': str(station_id)}
        station = self.__radio_get(path, param)
        if self.__check_redirect(station['streamURL']):
            station['streamURL'] = self.__follow_redirect(station['streamURL'])
        if resolve_playlists and self.__check_paylist(station['streamURL']):
            station['streamURL'] = self.__resolve_playlist(station)
        stations = (station, )
        return self.__format_stations(stations)[0]


    def __follow_redirect(self, url):
        req = Request(url)
        req.add_header('User-Agent', self.user_agent)
        response = urlopen(req)
        return response.geturl()


    def __resolve_playlist(self, station):
        servers = []
        stream_url = station['streamURL']
        if stream_url.lower().endswith('m3u'):
            response = self.__urlopen(stream_url)
            servers = [l for l in response.splitlines() if l.strip() and not l.strip().startswith('#')]
        elif stream_url.lower().endswith('pls'):
            response = self.__urlopen(stream_url)
            servers = [l.split('=')[1] for l in response.splitlines() if l.lower().startswith('file')]
        elif stream_url.lower().endswith('asx'):
            response = self.__urlopen(stream_url)
            servers = [l.split('href="')[1].split('"')[0] for l in response.splitlines() if 'href' in l]
        elif stream_url.lower().endswith('xml'):
            servers = [stream_url['streamUrl'] for stream_url in station.get('streamUrls', []) if 'streamUrl' in stream_url]
        if servers:
            return random.choice(servers)
        return stream_url


    def play_station(self, station_id):
        station = self.get_station_by_station_id(station_id)
        item = xbmcgui.ListItem(label=station['name'], path=station['stream_url'], iconImage=station['thumbnail'], thumbnailImage=station['thumbnail'])
        item.setInfo(type="Music", infoLabels={"Title": station['name']})
        return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


    def addStationToDirectory(self, station, context=None, queue=False, isAction=True, isFolder=False):
        try:
            name = str(station['name']).encode('utf-8')
        except Exception:
            name = 'Unknown Station'
        query = 'radioPlayStation&url=%s' % (str(station['id']))
        url = '%s?action=%s' % (sysaddon, query) if isAction is True else query
        thumbnail = (station.get('picture4TransName') or station.get('picture4Name') or station.get('picture1TransName').replace('_1_', '_4_') or station.get('picture1Name').replace('_1_', '_4_'))
        thumb = station['pictureBaseURL'] + thumbnail
        cm = []
        if context is not None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setProperty('IsPlayable', 'true')
        item.setArt({'icon': thumb, 'thumb': thumb})
        if addonFanart is not None:
            item.setProperty('Fanart_Image', addonFanart)
        iInfo = {'title': station.get('name', ''), 'rating': str(station.get('rating', '0.0')), 'genre': station.get('genre', ''), 'size': int(station.get('bitrate', 0)), 'comment': station.get('current_track', '')}
        item.setInfo('Music', iInfo)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)


    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except Exception:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction is True else query
        thumb = os.path.join(artPath, thumb) if artPath is not None else icon
        cm = []
        if context is not None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if addonFanart is not None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)


    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


