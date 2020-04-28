# -*- coding: utf-8 -*-
#
# Copyright (C) 2016,2018 RACC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals, absolute_import

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
from xbmcgui import ListItem
from routing import Plugin

import sys
import os
import traceback
import requests
import requests_cache
import json
import re
from datetime import timedelta
from base64 import b64decode

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
try:
    from urllib.parse import quote as orig_quote
except ImportError:
    from urllib import quote as orig_quote


addon = xbmcaddon.Addon()
plugin = Plugin()
plugin.name = addon.getAddonInfo("name")
user_agent = "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTS Build/LVY48F)"
USER_DATA_DIR = xbmc.translatePath(addon.getAddonInfo("profile")).decode("utf-8")
CACHE_TIME = int(addon.getSetting("cache_time"))
CACHE_FILE = os.path.join(USER_DATA_DIR, "cache")
expire_after = timedelta(hours=CACHE_TIME)

if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

s = requests_cache.CachedSession(CACHE_FILE, allowable_methods=("GET", "POST"), expire_after=expire_after, old_data_on_error=True)
s.hooks = {"response": lambda r, *args, **kwargs: r.raise_for_status()}
s.headers.update({"User-Agent": user_agent})

# USER = 'SolidStreamz'
# PASS = '@!SolidStreamz!@'
# data_url = 'http://solidstreamz.com/api/streamzdata.php'

USER = "PTVSPORTS"
PASS = "!%%!SPORTSptv!%%!"
data_url = "http://www.solidstreamz.com/ptvsport/streamzdatadb.php"

r = s.post(data_url, headers={"User-Agent": user_agent}, auth=(USER, PASS), timeout=5)
res_b64 = r.text
res = json.loads(b64decode(res_b64[:2] + res_b64[3:]).decode("utf-8"), strict=False)
if "Username" in res["DATA"][0]:
    api_url = "{0}/panel_api.php?mode=live&username={1}&password={2}".format(res["DATA"][0]["MainURL"], res["DATA"][0]["Username"], res["DATA"][0]["Password"])
else:
    api_url = res["DATA"][0]["MainURL"]


def quote(s, safe=""):
    return orig_quote(s.encode("utf-8"), safe.encode("utf-8"))


@plugin.route("/")
def root():
    r = s.get(api_url, headers={"User-Agent": user_agent}, timeout=5)
    api_res = r.json()
    list_items = []
    categories = []
    for ch in api_res["available_channels"].keys():
        categories.append((api_res["available_channels"][ch]["category_id"], api_res["available_channels"][ch]["category_name"]))

    categories = set(categories)
    while categories:
        cat = categories.pop()
        li = ListItem(cat[1])
        url = plugin.url_for(list_channels, cat_id=cat[0])
        list_items.append((url, li, True))

    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route("/list_channels/<cat_id>")
def list_channels(cat_id=None):
    r = s.get(api_url, headers={"User-Agent": user_agent}, timeout=5)
    api_res = r.json()

    list_items = []
    for ch in api_res["available_channels"].keys():
        if api_res["available_channels"][ch]["category_id"] == cat_id:
            li = ListItem(api_res["available_channels"][ch]["name"])
            li.setProperty("IsPlayable", "true")
            li.setArt({"thumb": "{0}|User-Agent={1}".format(api_res["available_channels"][ch]["stream_icon"], quote(user_agent))})
            li.setInfo(type="Video", infoLabels={"Title": api_res["available_channels"][ch]["name"], "mediatype": "video"})
            try:
                li.setContentLookup(False)
            except:
                pass
            url = plugin.url_for(play, ch=ch)
            list_items.append((url, li, False))

    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route("/play/<ch>/play.pvr")
def play(ch):

    def get_auth(token):
        _pattern = re.compile("<script>([^<]+)</script>", re.M)
        with s.cache_disabled():
            r = s.post(token)
        _split = re.search(_pattern, r.text).group(1).strip().split("\n")
        _upperCase = urlparse(token).path.split("/")[1].upper()
        _c = ord(_upperCase[0]) - ord("@")
        _s2 = _split[ord(_upperCase[(len(_upperCase) - 1)]) - ord("@") - 1].split("?")[1]
        _n = len(_s2) - 1
        _in = list(_s2)
        _in.pop(_n - (_c + int(0x0005)))
        _in.pop(_n - (_c + int(0x000f)))
        _in.pop(_n - (_c + int(0x0019)))
        _in.pop(_n - (_c + ord("#")))
        return "".join(_in)

    r = s.get(api_url, headers={"User-Agent": user_agent}, timeout=5)
    api_res = r.json()

    image = "{0}|User-Agent={1}".format(api_res["available_channels"][ch]["stream_icon"], quote(user_agent))
    title = api_res["available_channels"][ch]["name"]
    if "direct_source" in api_res["available_channels"][ch]:
        _source = api_res["available_channels"][ch]["direct_source"]
    else:
        _source = api_res["available_channels"][ch]["stream_list"][0]["stream_url"]

    if _source:
        media_url = "{0}?{1}|User-Agent={2}".format(_source, get_auth(res["DATA"][0]["Token"]), quote(res["DATA"][0].get("UserAgent", user_agent)))
    else:
        ts_url = "http://{0}:{1}/live/{2}/{3}/{4}.ts".format(
            api_res["server_info"]["url"], api_res["server_info"]["port"], api_res["user_info"]["username"], api_res["user_info"]["password"], ch
        )
        # with s.cache_disabled():
        # r = s.get(ts_url, headers = {'User-Agent': res['DATA'][0]['UserAgent']}, allow_redirects=False)
        # _location = r.headers['Location']
        # if 'playlist.m3u8' in _location:
        # media_url = '{0}?{1}|User-Agent={2}'.format(_location, get_auth(res['DATA'][0]['Token']), quote(res['DATA'][0]['UserAgent']))
        # else:
        # media_url = '{0}|User-Agent={1}'.format(_location, quote(res['DATA'][0]['UserAgent']))

        media_url = "{0}|User-Agent={1}".format(ts_url, quote(res["DATA"][0].get("UserAgent", user_agent)))

    if "playlist.m3u8" in media_url:
        if addon.getSetting("inputstream") == "true":
            li = ListItem(title, path=media_url)
            li.setArt({"thumb": image, "icon": image})
            li.setMimeType("application/vnd.apple.mpegurl")
            li.setProperty("inputstreamaddon", "inputstream.adaptive")
            li.setProperty("inputstream.adaptive.manifest_type", "hls")
            li.setProperty("inputstream.adaptive.stream_headers", media_url.split("|")[-1])
        else:
            li = ListItem(title, path=media_url)
            li.setArt({"thumb": image, "icon": image})
            li.setMimeType("application/vnd.apple.mpegurl")
            try:
                li.setContentLookup(False)
            except:
                pass
    else:
        li = ListItem(title, path=media_url)
        li.setArt({"thumb": image, "icon": image})

    xbmcplugin.setResolvedUrl(plugin.handle, True, li)


if __name__ == "__main__":
    try:
        plugin.run(sys.argv)
    except requests.exceptions.RequestException as e:
        dialog = xbmcgui.Dialog()
        dialog.notification(plugin.name, str(e), xbmcgui.NOTIFICATION_ERROR)
        traceback.print_exc()
        xbmcplugin.endOfDirectory(plugin.handle, False)
