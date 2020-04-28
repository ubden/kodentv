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
import json
import urllib, urlparse, re

from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdbest.net', 'ffull.net']
        self.base_link = 'https://vikv.net/'
        self.embed_link = 'https://api.hdv.fun/embed/{}'
        self.frames_link = 'https://api.hdv.fun/'
        self.sub_link = 'https://sub1.hdv.fun/vtt1/{}.vtt'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except :
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            imdb = data['imdb']
            url = self.embed_link.format(imdb)
            data = client.request(url, referer=self.base_link)
            frames_link = re.findall('''\$\.post\('(.+?)',{'imdb''', data, re.DOTALL)[0]
            frames_link = urlparse.urljoin(self.frames_link, frames_link) if frames_link.startswith('/') else frames_link
            try:
                get_ip = client.request('https://whatismyipaddress.com')
                ip = re.findall('''/ip/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})['"]''', get_ip, re.DOTALL)[0]
            except IndexError:
                ip = '0'
            post = {'imdb': imdb, 'ip': ip}
            frames = client.request(frames_link, post=post)
            frames = json.loads(frames)
            for url in frames:
                try:
                    subs = url['sub']
                    sub = re.findall('''sub_id['"]:\s*(\d+)\,.+?lg['"]:\s*u['"]greek['"]''', str(subs))[0]
                except :
                    subs = url['sub']
                    sub = re.findall('''sub_id['"]:\s*(\d+)\,.+?lg['"]:\s*u['"]english['"]''', str(subs))[0]

                sub = self.sub_link.format(sub)
                link = url['src'][0]['src']
                quality = url['src'][0]['label']

                url = link.replace(' ', '%20') + '|User-Agent={}&Referer={}'.format(
                    urllib.quote(client.agent()), 'https://redirector.googlevideo.com/')
                quality, info = source_utils.get_release_quality(quality)

                sources.append(
                    {'source': 'GVIDEO', 'quality': quality, 'language': 'en', 'url': url, 'sub': sub,
                     'direct': True, 'debridonly': False})

            return sources
        except :
            return sources

    def resolve(self, url):
        return url