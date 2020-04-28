# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, xbmcgui
import sys
import datetime
import json
import requests
import time
import re
from threading import Thread
# from tikimeta.utils import logger

__addon_id__ = 'script.module.tikimeta'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__addon_profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__handle__ = int(sys.argv[1])
window = xbmcgui.Window(10000)

class TvdbAPI:
    def __init__(self, api_key, jw_token):
        self.result = {}
        self.episodes_result = []
        self.cast = []
        self.seasons_summary = []
        self.timeout = 15.0
        self.base_url = 'https://api.thetvdb.com/'
        self.base_image_url = 'https://www.thetvdb.com/banners/'
        self.api_key = api_key
        self.jw_token = jw_token
        if not self.jw_token or self.jw_token == '': self.get_new_jwtoken()

    def make_headers(self, language=None):
        headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'User-agent': 'Mozilla/5.0',
                    'Authorization': 'Bearer %s' % self.jw_token
                    }
        if language: headers['Accept-Language'] = language
        return headers

    def pause_token_renew(self):
        if not window.getProperty('tikimeta.fetching.tvdb.jwtoken') == 'true':
            return False
        for i in range(0, 20):
            if window.getProperty('tikimeta.fetching.tvdb.jwtoken') == 'true':
                time.sleep(1)
            else:
                self.jw_token = window.getProperty('tikimeta.new.tvdb.jwtoken')
                return True

    def pause_token_new(self):
        if not window.getProperty('tikimeta.fetching.new.tvdb.jwtoken') == 'true':
            return False
        for i in range(0, 20):
            if window.getProperty('tikimeta.fetching.new.tvdb.jwtoken') == 'true':
                time.sleep(1)
            else:
                self.jw_token = window.getProperty('tikimeta.new.tvdb.jwtoken')
                return True

    def get_new_jwtoken(self):
        pause_token_new = self.pause_token_new()
        if not pause_token_new:
            window.setProperty('tikimeta.fetching.new.tvdb.jwtoken', 'true')
            window.clearProperty('tikimeta.new.tvdb.jwtoken')
        else: return
        url = '%slogin' % self.base_url
        data = json.dumps({'apikey': self.api_key})
        headers = self.make_headers()
        if 'Authorization' in headers:
            headers.pop('Authorization')
        response = json.loads(requests.post(url, data=data, headers=headers).text)
        self.jw_token = response['token']
        __addon__.setSetting('tvdb.jwtoken', self.jw_token)
        __addon__.setSetting('tvdb.jwtoken_expiry', str(time.time() + (24 * (60 * 60))))
        window.setProperty('tikimeta.new.tvdb.jwtoken', self.jw_token)
        window.clearProperty('tikimeta.fetching.new.tvdb.jwtoken')

    def renew_jwtoken(self):
        pause_token_renew = self.pause_token_renew()
        if not pause_token_renew:
            window.setProperty('tikimeta.fetching.tvdb.jwtoken', 'true')
            window.clearProperty('tikimeta.new.tvdb.jwtoken')
        else: return
        url = '%srefresh_token' % self.base_url
        headers = self.make_headers()
        response = json.loads(requests.post(url, headers=headers).text)
        if 'Error' in response:
            window.clearProperty('tikimeta.fetching.tvdb.jwtoken')
            self.get_new_jwtoken()
        else:
            self.jw_token = response['token']
            __addon__.setSetting('tvdb.jwtoken', self.jw_token)
            __addon__.setSetting('tvdb.jwtoken_expiry', str(time.time() + (24 * (60 * 60))))
            window.setProperty('tikimeta.new.tvdb.jwtoken', self.jw_token)
            window.clearProperty('tikimeta.fetching.tvdb.jwtoken')
        return

    def _get(self, url, language=None):
        data = None
        response = None
        headers = self.make_headers(language)
        url = self.base_url + url
        try:
            try:
                response = requests.get(url, headers=headers, timeout=self.timeout)
                response = response.text
            except requests.exceptions.RequestException as e:
                from tikimeta.utils import logger
                logger('TVDb Error', e)
            if response:
                if 'not authorized' in response.lower():
                    self.renew_jwtoken()
                    headers = self.make_headers(language)
                    response = requests.get(url, headers=headers, timeout=self.timeout)
                    response = response.text
                response = json.loads(response)
                if response.get("data"):
                    data = response
        except: pass
        return data

    def get_series_episodes_summary(self, tvdb_id):
        summary = None
        try: summary = self._get("series/%s/episodes/summary" % tvdb_id)['data']
        except: pass
        return summary

    def get_series(self, tvdb_id, language):
        series_info = self._get("series/%s" % tvdb_id, language)['data']
        if not series_info['overview']:
            series_info = self._get("series/%s" % tvdb_id, 'en')['data']
        return series_info

    def get_series_overview(self, tvdb_id, language):
        series_info = None
        try:
            series_info = self.get_series(tvdb_id, language)
            if not series_info['overview']:
                series_info = self.get_series(tvdb_id, 'en')
            series_info = series_info['overview']
        except: pass
        return series_info

    def get_all_episodes(self, tvdb_id, language):
        def _get_multipage(page, language):
            data = self._get("series/%s/episodes?page=%s" % (tvdb_id, page), language)
            self.results.extend(data['data'])
        def _fetch_info():
            threads = []
            self.results = []
            try:
                data = self._get("series/%s/episodes?page=1" % tvdb_id, language)
                if not data: return None
                total_pages = data['links']['last']
                data = data['data']
                self.results.extend(data)
                if total_pages > 1:
                    for i in range(2, total_pages+1): threads.append(Thread(target=_get_multipage, args=(i, language)))
                    [i.start() for i in threads]
                    [i.join() for i in threads]
            except: pass
            return self.results
        if not tvdb_id: return None
        episode_results = _fetch_info()
        if language != 'en':
            language = 'en'
            grab_english = False
            for i in episode_results:
                if i['overview'] == None:
                    grab_english = True
                    break
            if grab_english:
                import copy
                foreign_results = copy.deepcopy(episode_results)
                episode_results = _fetch_info()
                for index, item in enumerate(foreign_results, start=0):
                    if item['overview'] == None:
                        item['overview'] = episode_results[index]['overview']
                episode_results = foreign_results
        return episode_results

    def get_series_by_imdb_id(self, imdb_id):
        data = self._get("search/series?imdbId=%s" % imdb_id)
        if data: return data['data'][0]
        else: return None

    def get_series_by_name(self, name):
        data = self._get("search/series?name=%s" % name)
        if data: return data['data'][0]
        else: return None


