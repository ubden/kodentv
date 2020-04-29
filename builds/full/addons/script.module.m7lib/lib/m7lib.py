"""
    m7lib

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

    Checkout the Free Live TV addon for an example of how to use m7lib
    https://github.com/mhancoc7/kodi-addons/tree/master/_repo/plugin.video.freelivetv.tva
"""

import os
import json
import base64
import re
import xbmc
import xbmcplugin
import xbmcgui
import sys
import string
import random

try:
    # Python 3
    from urllib.request import urlopen, Request
except ImportError:
    # Python 2
    from urllib2 import urlopen, Request

try:
    # Python 3
    from html.parser import HTMLParser
except ImportError:
    # Python 2
    from HTMLParser import HTMLParser

convert_special_characters = HTMLParser()
dlg = xbmcgui.Dialog()

stream_failed = "Unable to get stream. Please try again later."
stream_plug = "aHR0cHM6Ly9tN2xpYi5kZXYvYXBpL3YxLw=="
explore_org_base = "aHR0cHM6Ly9vbWVnYS5leHBsb3JlLm9yZy9hcGkvZ2V0X2NhbV9ncm91cF9pbmZvLmpzb24/aWQ9Nzk="
tubi_tv_base = "aHR0cHM6Ly90dWJpdHYuY29tL296"


class Common:

    @staticmethod
    def dlg_failed(mode):
        dlg.ok(mode, stream_failed)
        exit()

    @staticmethod
    def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
        # Added '# nosec' to suppress bandit warning since this is not used for security/cryptographic purposes.
        return ''.join(random.choice(chars) for x in range(size))  # nosec

    @staticmethod
    # Parse string and extracts first match as a string
    # The default is to find the first match. Pass a 'number' if you want to match a specific match. So 1 would match
    # the second and so forth
    def find_single_match(text, pattern, number=0):
        try:
            matches = re.findall(pattern, text, flags=re.DOTALL)
            result = matches[number]
        except AttributeError:
            result = ""
        return result

    @staticmethod
    # Parse string and extracts multiple matches using regular expressions
    def find_multiple_matches(text, pattern):
        matches = re.findall(pattern, text, re.DOTALL)
        return matches

    @staticmethod
    # Open URL
    def open_url(url, user_agent=True):
        if url.lower().startswith('http'):
            # Added '# nosec' to suppress bandit warnings since the code is not accepting non-http schemes
            req = Request(url)  # nosec
        else:
            raise ValueError
        if user_agent is not False:
            req.add_header('User-Agent',
                           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11'
                           '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        # Added '# nosec' to suppress bandit warnings since the code is not accepting non-http schemes
        response = urlopen(req)  # nosec
        link = response.read()
        response.close()
        return link

    @staticmethod
    # Section, Genre, or Channel logos
    def get_logo(channel, logo_type=None):
        if logo_type == "section":
            return xbmc.translatePath(
                os.path.join('special://home/addons/script.module.m7lib', 'lib', 'resources', 'images', 'sections',
                             channel + ".png"))
        elif logo_type == "genre":
            return xbmc.translatePath(
                os.path.join('special://home/addons/script.module.m7lib', 'lib', 'resources', 'images', 'genres',
                             channel + ".png"))

    @staticmethod
    # Available channels
    def get_channels():
        req = Common.open_url(base64.b64decode(stream_plug).decode("UTF-8") + "channels")
        channel_list = json.loads(req)
        return channel_list

    @staticmethod
    # Available sections
    def get_sections():
        section_list = ["All Channels", "Genres"]
        return section_list

    @staticmethod
    # Available genres
    def get_genres():
        req = Common.open_url(base64.b64decode(stream_plug).decode("UTF-8") + "genres")
        genre_list = json.loads(req)
        return genre_list

    @staticmethod
    def add_channel(mode, icon, fanart, title=None, live=True):
        if live is True:
            u = sys.argv[0] + "?mode=" + str(mode) + "&pvr=.pvr"
        else:
            u = sys.argv[0] + "?mode=" + str(mode)
        if title is not None:
            item = title
        else:
            item = mode
        liz = xbmcgui.ListItem(str(item), iconImage=icon, thumbnailImage=icon)
        liz.setArt({'thumb': icon, 'poster': icon, 'banner': icon, 'fanart': fanart})
        liz.setProperty("IsPlayable", "true")
        liz.setInfo('video', {'Title': item})
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
        return ok

    @staticmethod
    def add_section(mode, icon, fanart, title=None):
        u = sys.argv[0] + "?mode=" + str(mode) + "&rand=" + Common.random_generator()
        if title is not None:
            item = title
        else:
            item = mode
        liz = xbmcgui.ListItem(str(item), iconImage=icon, thumbnailImage=icon)
        liz.setArt({'thumb': icon, 'poster': icon, 'banner': icon, 'fanart': fanart})
        liz.setProperty("IsPlayable", "true")
        liz.setInfo('video', {'Title': item})
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
        return ok

    @staticmethod
    # Return the Channel ID from YouTube URL
    def get_youtube_channel_id(url):
        return url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]

    @staticmethod
    # Return the full YouTube plugin url
    def get_playable_youtube_url(channel_id):
        return 'plugin://plugin.video.youtube/play/?video_id=%s' % channel_id

    @staticmethod
    # Play stream
    # Optional: set xbmc_player to True to use xbmc.Player() instead of xbmcplugin.setResolvedUrl()
    def play(stream, channel=None, xbmc_player=False):
        if xbmc_player:
            li = xbmcgui.ListItem(channel)
            xbmc.Player().play(stream, li, False)
        else:
            item = xbmcgui.ListItem(channel, path=stream)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

    @staticmethod
    # Get and Play stream
    def get_stream_and_play(mode):
        stream = None
        req = Common.open_url(base64.b64decode(stream_plug).decode("UTF-8") + "channels/?slug=" + mode)
        stream = json.loads(req)['stream']

        if stream is not None:
            Common.play(stream)
        else:
            Common.dlg_failed(mode)


class Stream:

    # Begin Explore.org #
    @staticmethod
    def get_explore_org_streams():
        stream_list = []
        url = base64.b64decode(explore_org_base).decode('UTF-8')
        open_url = Common.open_url(url).decode("UTF-8")
        json_results = json.loads(open_url)['data']['feeds']
        for stream in sorted(json_results, key=lambda k: k['title']):
            if stream["is_inactive"] is False and stream["is_offline"] is False and stream["video_id"] is not None:
                if stream["thumb"] == "":
                    icon = "https://i.ytimg.com/vi/" + stream["video_id"] + "/hqdefault.jpg"
                else:
                    icon = stream["thumb"]
                if stream["thumbnail_large_url"] == "":
                    fanart = "https://i.ytimg.com/vi/" + stream["video_id"] + "/hqdefault.jpg"
                else:
                    fanart = stream["thumbnail_large_url"]
                stream_list.append({"id": stream["video_id"], "icon": icon, "fanart": fanart,
                                    "title": stream["title"].encode(encoding='UTF-8', errors='strict')})
        return stream_list
    # End Explore.org #

    # Begin Tubi TV #
    @staticmethod
    def get_tubi_tv_categories():
        cat_list = []
        url = base64.b64decode(tubi_tv_base) + '/containers/'
        req = Common.open_url(url).decode('UTF-8')
        json_results = json.loads(req)
        for category in range(0, len(json_results['list'])):
            try:
                icon = json_results['hash'][json_results['list'][category]]['thumbnail']
            except StandardError:
                icon = "none"
            cat_list.append({"id": json_results['list'][category],
                             "icon": icon,
                             "title": json_results['hash'][json_results['list'][category]]['title'].encode('UTF-8', 'ignore')})
        return cat_list

    @staticmethod
    def get_tubi_tv_content(category):
        content_list = []
        url = base64.b64decode(tubi_tv_base) + '/containers/' + category + '/content?cursor=1&limit=200'
        req = Common.open_url(url).decode('UTF-8')
        json_results = json.loads(req)

        for movie in json_results['contents'].keys():
            try:
                content_list.append({"id": json_results['contents'][movie]['id'],
                                     "icon": json_results['contents'][movie]['posterarts'][0],
                                     "title": json_results['contents'][movie]['title'].decode('UTF-8'),
                                     "type": json_results['contents'][movie]['type']})
            except StandardError:
                pass
        return content_list

    @staticmethod
    def get_tubi_tv_episodes(show):
        episode_list = []
        url = base64.b64decode(tubi_tv_base) + '/videos/0' + show + '/content'
        req = Common.open_url(url).decode('UTF-8')
        json_results = json.loads(req)

        for season in range(0, len(json_results['children'])):
            try:
                for episode in range(0, len(json_results['children'][season]['children'])):
                    episode_list.append({"id": json_results['children'][season]['children'][episode]['id'],
                                         "icon":
                                             json_results['children'][season]['children'][episode]['thumbnails'][0],
                                         "title": json_results['children'][season]['children'][episode]['title'].decode('UTF-8')})
            except StandardError:
                pass
        return episode_list

    @staticmethod
    def get_tubi_tv_search(text):
        search_list = []
        url = base64.b64decode(tubi_tv_base) + '/search/' + text
        req = Common.open_url(url).decode('UTF-8')
        json_results = json.loads(req)

        for result in json_results:
            try:
                search_list.append({"id": result['id'],
                                     "icon": result['posterarts'][0],
                                     "title": result['title'].decode('UTF-8'),
                                     "type": result['type']})
            except StandardError:
                pass
        return search_list

    @staticmethod
    def get_tubi_tv_stream(stream_id):
        req = Common.open_url(base64.b64decode(tubi_tv_base) + '/videos/' + stream_id + '/content')
        return json.loads(req)['url']
    # End Tubi TV #
