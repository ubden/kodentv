# -*- coding: utf-8 -*-

'''
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
'''

import re,requests,urlparse
from resources.lib.modules import cleantitle,source_utils

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['iwannawatch.is']
        self.base_link = 'https://www.iwannawatch.is'
        self.search_link = '/wp-admin/admin-ajax.php?action=bunyad_live_search&query=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url  % (search_id.replace(' ', '+').replace('-', '+').replace('++', '+'))
            headers = {'User-Agent': User_Agent}
            search_results = requests.get(url,headers=headers,timeout=10).content
            match = re.compile('<li>.+?<a href="(.+?)".+?title="(.+?)".+?<a href=.+?>(.+?)<',re.DOTALL).findall(search_results)
            for row_url, row_title, release in match:
                if cleantitle.get(title) in cleantitle.get(row_title):
                    if year in str(release):
                        return row_url
            return
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            headers = {'User-Agent': User_Agent}
            html = requests.get(url, headers=headers, timeout=10).content
            try:
                qual = re.compile('<div class="cf">.+?class="quality">(.+?)</td>',re.DOTALL).findall(html)
                for i in qual:
                    quality = source_utils.check_url(i)
                links = re.compile('li class=.+?data-href="(.+?)"',re.DOTALL).findall(html)
                for link in links:
                    if 'http' not in link:
                        link = 'http:'+link
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if link in str(sources):
                        continue
                    if valid:
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
                return sources
            except:
                return
        except Exception:
            return
        return sources

    def resolve(self, url):
        return url
