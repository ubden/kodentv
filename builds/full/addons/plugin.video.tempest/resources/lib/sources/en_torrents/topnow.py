# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.
# Was xpause fix by Tempest on 10-13-2019

import re
import traceback
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import debrid
from resources.lib.modules import source_utils
from resources.lib.modules import log_utils
from resources.lib.modules import rd_check, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['topnow.se']
        self.base_link = 'http://topnow.se'
        self.search_link = '/%s'
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status() is False: return
        if debrid.torrent_enabled() is False: return
        try:
            mtitle = cleantitle.geturl(title)
            url = self.base_link + self.search_link % mtitle
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources

            html = client.request(url, headers=self.headers)
            link = re.findall('href="(magnet:.+?)"', html, re.DOTALL)
            for link in link:
                link = str(client.replaceHTMLCodes(link).split('&tr')[0])
                quality, info = source_utils.get_release_quality(link, link)
                try:
                    size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', html)[-1]
                    div = 1 if size.endswith(('GB', 'GiB')) else 1024
                    size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                    size = '%.2f GB' % size
                    info.append(size)
                except:
                    pass
                info = ' | '.join(info)
                if control.setting('torrent.rd_check') == 'true':
                    checked = rd_check.rd_cache_check(link)
                    if checked:
                        sources.append(
                            {'source': 'Cached Torrent', 'quality': quality, 'language': 'en','url': checked,
                             'info': info, 'direct': False, 'debridonly': True})
                else:
                    sources.append(
                        {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': link, 'info': info,
                         'direct': False, 'debridonly': True})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Topnow Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
