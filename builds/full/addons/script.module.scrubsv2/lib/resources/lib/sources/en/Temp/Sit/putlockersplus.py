# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 06-17-2019 by JewBMX in Scrubs.

import re, base64
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en'] #_Down,________Ok,___________Clean,_______Craptcha,______Slow__
		self.domains = ['putlockers.plus', 'putlockers.fm', 'putlockers.ws', 'putlockers.gs', 'putlockerz.io']
		self.base_link = 'http://www0.putlockers.plus'
		self.search_link = '/search-movies/%s.html'
		self.scraper = cfscrape.create_scraper()
		# old  putlocker.tl


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			find = cleantitle.geturl(title)
			find = find + '-' + year
			query = find.replace('-','+')
			url = self.base_link + self.search_link % query
			r = self.scraper.get(url).content
			match = re.compile('<a href="http://www0.putlockers.plus/watch/(.+?)-' + find + '.html"').findall(r)
			for url_id in match:
				url = 'http://www0.putlockers.plus/watch/' + url_id + '-' + find + '.html'
				r = self.scraper.get(url).content
				return url
		except:
			return


	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			url = cleantitle.geturl(tvshowtitle)
			url = url.replace('-','+')
			return url
		except:
			return
 
 
	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			query = url + '+season+' + season
			find = query.replace('+','-')
			url = self.base_link + self.search_link % query
			r = self.scraper.get(url).content
			match = re.compile('<a href="http://www0.putlockers.plus/watch/(.+?)-' + find + '.html"').findall(r)
			for url_id in match:
				url = 'http://www0.putlockers.plus/watch/' + url_id + '-' + find + '.html'
				r = self.scraper.get(url).content
				match = re.compile('<a class="episode episode_series_link" href="(.+?)">' + episode + '</a>').findall(r)
				for url in match:
					return url
		except:
			return


	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			if url == None:
				return sources
			r = self.scraper.get(url).content
			try:
				match = re.compile('<p class="server_version"><img src="http://www0.putlockers.plus/themes/movies/img/icon/server/(.+?).png" width="16" height="16" /> <a href="(.+?)">').findall(r)
				for host, url in match:
					if url == None:
						return sources
					quality = source_utils.check_url(url)
					valid, host = source_utils.is_host_valid(host, hostDict)
					if source_utils.limit_hosts() is True and host in str(sources):
						continue
					if valid:
					    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
			except:
				return
		except Exception:
			return
		return sources


	def resolve(self, url):
		r = self.scraper.get(url).content
		match = re.compile('decode\("(.+?)"').findall(r)
		for info in match:
			info = base64.b64decode(info)
			match = re.compile('src="(.+?)"').findall(info)
			for url in match:
				return url

