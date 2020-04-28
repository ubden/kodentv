# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcvfs, xbmcgui
import json
import re
from modules.utils import get_release_quality, get_file_info,  clean_file_name, to_utf8
from scrapers import build_internal_scrapers_label, label_settings
from modules import settings
# from modules.utils import logger

__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
window = xbmcgui.Window(10000)

class LocalLibrarySource:
    def __init__(self):
        self.scrape_provider = 'local'
        self.sources = []

    def results(self, info):
        try:
            self.info = info
            self.db_type = self.info.get("db_type")
            self.title = self.info.get("title")
            self.year = self.info.get("year")
            self.season = self.info.get("season")
            self.episode = self.info.get("episode")
            self.db_info = self._get_library_video(self.db_type, self.title, self.year, self.season, self.episode)
            if not self.db_info: return self.sources
            self.label_settings = label_settings(self.info['scraper_settings'], self.scrape_provider)
            file_name = self.db_info.get("name")
            file_id = self.db_info.get("file_id")
            file_dl = self.db_info.get("file_id")
            size = self._get_size(file_dl)
            details = get_file_info(file_name)
            video_quality = get_release_quality(file_name, file_dl)
            label, multiline_label = build_internal_scrapers_label(self.label_settings, file_name, details, size, video_quality)
            self.sources.append({'name': file_name,
                            'label': label,
                            'multiline_label': multiline_label,
                            'quality': video_quality,
                            'size': size,
                            'url_dl': file_dl,
                            'url': file_dl,
                            'id': file_id,
                            'local': True,
                            'direct': True,
                            'source': self.scrape_provider,
                            'scrape_provider': self.scrape_provider})
            window.setProperty('local_source_results', json.dumps(self.sources))
        except Exception as e:
            from modules.utils import logger
            logger('FEN local scraper Exception', e)
        return self.sources

    def _get_library_video(self, db_type, title, year, season=None, episode=None):
        try:
            name = None
            years = (str(year), str(int(year)+1), str(int(year)-1))
            if db_type == 'movie':
                r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["imdbnumber", "title", "originaltitle", "file"]}, "id": 1}' % years)
                r = to_utf8(r)
                r = json.loads(r)['result']['movies']
                try:
                    r = [i for i in r if clean_file_name(title).lower() in clean_file_name(to_utf8(i['title'])).lower()]
                    r = [i for i in r if not to_utf8(i['file']).endswith('.strm')][0]
                except: return None
                r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["streamdetails", "file"], "movieid": %s }, "id": 1}' % str(r['movieid']))
                r = to_utf8(r)
                r = json.loads(r)['result']['moviedetails']
            else:
                r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title"]}, "id": 1}' % years)
                r = to_utf8(r)
                r = json.loads(r)['result']['tvshows']
                try:
                    r = [i for i in r if clean_file_name(title).lower() in (clean_file_name(to_utf8(i['title'])).lower() if not ' (' in to_utf8(i['title']) else clean_file_name(to_utf8(i['title'])).lower().split(' (')[0])][0]
                except: return None
                r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["file"], "tvshowid": %s }, "id": 1}' % (str(season), str(episode), str(r['tvshowid'])))
                r = to_utf8(r)
                r = json.loads(r)['result']['episodes']
                try:
                    r = [i for i in r if not to_utf8(i['file']).endswith('.strm')][0]
                except:
                    return None
                r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"properties": ["streamdetails", "file"], "episodeid": %s }, "id": 1}' % str(r['episodeid']))
                r = to_utf8(r)
                r = json.loads(r)['result']['episodedetails']
            url = r['file'].encode('utf-8')
            try: name = url.split('/')[-1:][0]
            except: name = None
            if not name:
                try: name = url.split('\\')[-1:][0]
                except: name = None
            if not name:
                name = title
            return {'name': name, 'file_id': url}
        except: pass

    def _get_size(self, file):
        f = xbmcvfs.File(file) ; s = f.size() ; f.close()
        size = float(s)/1073741824
        return size
