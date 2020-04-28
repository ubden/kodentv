# -*- coding: UTF-8 -*-
# -Cleaned Up and Checked on 04-14-2020 by Tempest.**
"""
    **Created by Tempest**
    **Thanks Jewbmx for the assist.**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import requests, json, re
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import cleantitle
from resources.lib.modules import client, getSum
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdbest.net']
        self.base_link = 'https://hdbest.net'
        self.movie_link = '?q=%s+%s'
        self.session = requests.Session()
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.geturl(title)
            url = self.base_link + self.movie_link % (mtitle.replace('-', '+'), year)
            html = client.request(url, headers=self.headers)
            match = re.compile('class="thumb".+?title="(.+?)".+?href="(.+?)">').findall(html)
            for item_url, url in match:
                check = '%s (%s)' % (title, year)
                if check not in item_url:
                    continue
                return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostprDict + hostDict
            r = client.request(url, headers=self.headers)
            link = getSum.findSum(r)
            for url in link:
                if "api.hdv.fun" in url:
                    url = url.replace('https://api.hdv.fun/embed/', '')
                    apiurl = "https://api.hdv.fun/l1?imdb={}&ip=128.6.37.19".format(url)
                    movie_json = json.loads(self.session.post(apiurl).text)
                    url = movie_json[0]['src'][0]['src']
                    quainf = movie_json[0]['src'][0]['res']
                    quality, info = source_utils.get_release_quality(quainf, quainf)
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': True, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---HDbest Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
