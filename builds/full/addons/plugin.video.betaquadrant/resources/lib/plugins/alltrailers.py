# -*- coding: utf-8 -*-
"""

    Copyright (C) 2019, Tony H
    -- 7-16-19 Version 1.0.1 --

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

    -------------------------------------------------------------

    Usage Examples:

Movies coming out on dvd with release date:

<dir>
<title>Metacritic DVD Releases</title>
<metacritic>dvd</metacritic>
</dir>

Movies in theaters now:

<dir>
<title>Metacritic In Theaters</title>
<metacritic>theaters/0</metacritic>
</dir>

Movies coming soon with release date:

<dir>
<title>Metacritic Coming Soon</title>
<metacritic>coming/0</metacritic>
</dir>

TV Show trailers:

<dir>
<title>Metacritic TV Show Trailers</title>
<metacritic>tvshow/0</metacritic>
</dir>

"""    

import requests,re,os,xbmc,xbmcaddon,xbmcgui
import base64,pickle,koding,time,sqlite3,urllib
import urlparse
from koding import route
from ..plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list,  display_data, clean_url
from resources.lib.external.airtable.airtable import Airtable
from unidecode import unidecode
import random, ssl, copy, time
from collections import OrderedDict
from requests.sessions import Session
from requests.adapters import HTTPAdapter
from requests.compat import urlparse, urlunparse
from requests.exceptions import RequestException
from urllib3.util.ssl_ import create_urllib3_context, DEFAULT_CIPHERS

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_data_folder = xbmc.translatePath('special://home/userdata/addon_data')
addon_data = os.path.join(addon_data_folder, addon_id)
database_loc = os.path.join(addon_data, 'database.db')
base_link = 'https://www.metacritic.com'
DEFAULT_CIPHERS += ":!ECDHE+SHA:!AES128-SHA"


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"
]

DEFAULT_USER_AGENT = random.choice(USER_AGENTS)

DEFAULT_HEADERS = OrderedDict(
    (
        ("Host", None),
        ("Connection", "keep-alive"),
        ("Upgrade-Insecure-Requests", "1"),
        ("User-Agent", DEFAULT_USER_AGENT),
        (
            "Accept",
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        ),
        ("Accept-Language", "en-US,en;q=0.9"),
        ("Accept-Encoding", "gzip, deflate"),
    )
)

class AllTrailers(Plugin):
    name = "alltrailers"

    def process_item(self, item_xml):
        if "<metacritic>" in item_xml:
            item = JenItem(item_xml)
            if "dvd" in item.get("metacritic", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_dvd_trailers",
                    'url': item.get("metacritic", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "theaters" in item.get("metacritic",""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_theaters_trailers",
                    'url': item.get("metacritic", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "coming" in item.get("metacritic",""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_coming_trailers",
                    'url': item.get("metacritic", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item 
            elif "tvshow" in item.get("metacritic",""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_tvshow_trailers",
                    'url': item.get("metacritic", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item                                                                                  
            elif "link" in item.get("metacritic",""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_metacritic_trailer_link",
                    'url': item.get("metacritic", ""),
                    'folder': False,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item                 
 

@route(mode='get_dvd_trailers', args=["url"])
def get_game(url):
    pins = "PLuginmetacriticdvd"
    Items = fetch_from_db2(pins)
    if Items:
        display_data(Items) 
    else:   
        xml = ""       
        try:    
            url = "https://www.metacritic.com/browse/dvds/release-date/coming-soon/date"
            r = scraper.get(url).content
            m = re.compile('<td class="clamp-image-wrap">.+?<a href="(.+?)".+?<img src="(.+?)".+?alt="(.+?)".+?<span>(.+?)</span>.+?<div class="summary">(.+?)</div>',re.DOTALL).findall(r)
            for link, image, name, date, summary in m:
                link = base_link + link                  
                name = remove_non_ascii(name)
                name = clean_search(name)
                name = name.encode('utf8')
                summary = clean_search(summary)
                summary = remove_non_ascii(summary)
                summary = summary.encode('utf8')
                image = image.replace("-98","-250h")               
                xml += "<item>"\
                       "<title>%s : [COLOR=blue]DVD Release: [/COLOR]%s</title>"\
                       "<meta>"\
                       "<content>movie</content>"\
                       "<imdb></imdb>"\
                       "<title></title>"\
                       "<year></year>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>%s</fanart>"\
                       "<summary>%s</summary>"\
                       "</meta>"\
                       "<metacritic>link**%s**%s**%s</metacritic>"\
                       "</item>" % (name,date,image,image,summary,link,name,image)            
        except:
            pass
                  
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

@route(mode='get_theaters_trailers', args=["url"])
def get_game(url):
    xml = ""
    current = str(url.split("/")[-1])
    pins = "PLuginmetacritictheaters"+current
    Items = fetch_from_db2(pins)
    if Items:
        display_data(Items) 
    else:        
        try:    
            url = "https://www.metacritic.com/browse/movies/release-date/theaters/date?page="+current
            r = scraper.get(url).content
            m = re.compile('<td class="clamp-image-wrap">.+?<a href="(.+?)".+?<img src="(.+?)".+?alt="(.+?)".+?<span>(.+?)</span>.+?<div class="summary">(.+?)</div>',re.DOTALL).findall(r)
            for link, image, name, date, summary in m:
                link = base_link + link                  
                name = remove_non_ascii(name)
                name = clean_search(name)
                name = name.encode('utf8')
                summary = clean_search(summary)
                summary = remove_non_ascii(summary)
                summary = summary.encode('utf8')
                image = image.replace("-98","-250h")               
                xml += "<item>"\
                       "<title>%s : [COLOR=blue]In Theaters: [/COLOR]%s</title>"\
                       "<meta>"\
                       "<content>movie</content>"\
                       "<imdb></imdb>"\
                       "<title></title>"\
                       "<year></year>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>%s</fanart>"\
                       "<summary>%s</summary>"\
                       "</meta>"\
                       "<metacritic>link**%s**%s**%s</metacritic>"\
                       "</item>" % (name,date,image,image,summary,link,name,image)            
        except:
            pass

        next_page = int(current)+1
        xml += "<item>"\
               "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
               "<metacritic>theaters/%s</metacritic>"\
               "<thumbnail>http://www.clker.com/cliparts/a/f/2/d/1298026466992020846arrow-hi.png</thumbnail>"\
               "</item>" % (next_page)  
                  
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

@route(mode='get_coming_trailers', args=["url"])
def get_game(url):
    xml = ""
    current = url.split("/")[-1]
    pins = "PLuginmetacriticcoming"+current
    Items = fetch_from_db2(pins)
    if Items:
        display_data(Items) 
    else:          
        try:    
            url = "https://www.metacritic.com/browse/movies/release-date/coming-soon/date?page="+current
            r = scraper.get(url).content
            m = re.compile('<td class="clamp-image-wrap">.+?<a href="(.+?)".+?<img src="(.+?)".+?alt="(.+?)".+?<span>(.+?)</span>.+?<div class="summary">(.+?)</div>',re.DOTALL).findall(r)
            for link, image, name, date, summary in m:
                link = base_link + link                  
                name = remove_non_ascii(name)
                name = clean_search(name)
                name = name.encode('utf8')
                summary = clean_search(summary)
                summary = remove_non_ascii(summary)
                summary = summary.encode('utf8')
                image = image.replace("-98","-250h")               
                xml += "<item>"\
                       "<title>%s : [COLOR=blue]Release Date: [/COLOR]%s</title>"\
                       "<meta>"\
                       "<content>movie</content>"\
                       "<imdb></imdb>"\
                       "<title></title>"\
                       "<year></year>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>%s</fanart>"\
                       "<summary>%s</summary>"\
                       "</meta>"\
                       "<metacritic>link**%s**%s**%s</metacritic>"\
                       "</item>" % (name,date,image,image,summary,link,name,image)            
        except:
            pass
        next_page = int(current)+1
        xml += "<item>"\
               "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
               "<metacritic>coming/%s</metacritic>"\
               "<thumbnail>http://www.clker.com/cliparts/a/f/2/d/1298026466992020846arrow-hi.png</thumbnail>"\
               "</item>" % (next_page)             
                  
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

@route(mode='get_tvshow_trailers', args=["url"])
def get_game(url):
    xml = ""
    current = url.split("/")[-1]     
    pins = "PLuginmetacritictvshow"+current
    Items = fetch_from_db2(pins)
    if Items:
        display_data(Items) 
    else:          
        try:    
            url = "https://www.metacritic.com/browse/tv-shows/trailers/date?page="+current
            r = scraper.get(url).content
            m = re.compile('<h3 class="trailer_title">.+?<a href="(.+?)".+?<img src="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(r)
            for oglink, image, name in m:
                f = oglink.split("trailers/")[0]
                p = oglink.split("/")[-1]
                link = base_link + f + "season-1/trailers/" + p                 
                name = remove_non_ascii(name)
                name = clean_search(name)
                name = name.encode('utf8')
                t = scraper.get(link).content
                n = re.compile('<span itemprop="description">(.+?)</span>',re.DOTALL).findall(t)
                summary = n[0]
                summary = clean_search(summary)
                summary = remove_non_ascii(summary)
                summary = summary.encode('utf8')                                
                xml += "<item>"\
                       "<title>%s</title>"\
                       "<meta>"\
                       "<content>movie</content>"\
                       "<imdb></imdb>"\
                       "<title></title>"\
                       "<year></year>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>%s</fanart>"\
                       "<summary>%s</summary>"\
                       "</meta>"\
                       "<metacritic>link**%s**%s**%s</metacritic>"\
                       "</item>" % (name,image,image,summary,link,name,image)            
        except:
            pass
        next_page = int(current)+1
        xml += "<item>"\
               "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
               "<metacritic>tvshow/%s</metacritic>"\
               "<thumbnail>http://www.clker.com/cliparts/a/f/2/d/1298026466992020846arrow-hi.png</thumbnail>"\
               "</item>" % (next_page)         
                  
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)
                   

@route(mode='get_metacritic_trailer_link', args=["url"])
def get_game(url):
    try:
        koding.Show_Busy(status=True)
        link1 = url.split("**")[-3]
        name = url.split("**")[-2]
        thumbnail = url.split("**")[-1]        
        t = scraper.get(link1).content
        m2 = re.compile('<div class="video_and_autoplay">.+?data-mcvideourl="(.+?)"',re.DOTALL).findall(t)
        final_link = m2[0]
        koding.Show_Busy(status=False )
        info = xbmcgui.ListItem(name, thumbnailImage=thumbnail)
        xbmc.Player().play(final_link,info)
    except:
        pass
           

def fetch_from_db2(url):
    koding.reset_db()
    url2 = clean_url(url)
    match = koding.Get_All_From_Table(url2)
    if match:
        match = match[0]
        if not match["value"]:
            return None   
        match_item = match["value"]
        try:
                result = pickle.loads(base64.b64decode(match_item))
        except:
                return None
        created_time = match["created"]
        print created_time + "created"
        print time.time() 
        print CACHE_TIME
        test_time = float(created_time) + CACHE_TIME 
        print test_time
        if float(created_time) + CACHE_TIME <= time.time():
            koding.Remove_Table(url2)
            db = sqlite3.connect('%s' % (database_loc))        
            cursor = db.cursor()
            db.execute("vacuum")
            db.commit()
            db.close()
            display_list2(result, "video", url2)
        else:
            pass                     
        return result
    else:
        return []

def remove_non_ascii(text):
    return unidecode(text)

def clean_search(title):
    if title == None: return
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&').replace("&#039;","")
    title = re.sub('\\\|/|\(|\)|\[|\]|\{|\}|-|:|;|\*|\?|"|\'|<|>|\_|\.|\?', ' ', title)
    title = ' '.join(title.split())
    return title     

class CloudflareAdapter(HTTPAdapter):
    """ HTTPS adapter that creates a SSL context with custom ciphers """

    def get_connection(self, *args, **kwargs):
        conn = super(CloudflareAdapter, self).get_connection(*args, **kwargs)

        if conn.conn_kw.get("ssl_context"):
            conn.conn_kw["ssl_context"].set_ciphers(DEFAULT_CIPHERS)
        else:
            context = create_urllib3_context(ciphers=DEFAULT_CIPHERS)
            conn.conn_kw["ssl_context"] = context

        return conn

class CloudflareScraper(Session):
    def __init__(self, *args, **kwargs):
        self.tries = 0
        self.prev_resp = None
        self.delay = kwargs.pop("delay", None)
        # Use headers with a random User-Agent if no custom headers have been set
        headers = OrderedDict(kwargs.pop("headers", DEFAULT_HEADERS))

        # Set the User-Agent header if it was not provided
        headers.setdefault("User-Agent", DEFAULT_USER_AGENT)

        super(CloudflareScraper, self).__init__(*args, **kwargs)

        # Define headers to force using an OrderedDict and preserve header order
        self.headers = headers

        self.mount("https://", CloudflareAdapter())

    @staticmethod
    def is_cloudflare_iuam_challenge(resp, allow_empty_body=False):
        return (
            resp.status_code in (503, 429)
            and resp.headers.get("Server", "").startswith("cloudflare")
            and (allow_empty_body or (b"jschl_vc" in resp.content and b"jschl_answer" in resp.content))
        )

    @staticmethod
    def is_cloudflare_captcha_challenge(resp):
        return (
            resp.status_code == 403
            and resp.headers.get("Server", "").startswith("cloudflare")
            and b"/cdn-cgi/l/chk_captcha" in resp.content
        )

    def request(self, method, url, *args, **kwargs):
        resp = super(CloudflareScraper, self).request(method, url, *args, **kwargs)

        # Check if Cloudflare captcha challenge is presented
        if self.is_cloudflare_captcha_challenge(resp):
            self.handle_captcha_challenge()

        self.prev_resp = resp

        # Check if Cloudflare anti-bot "I'm Under Attack Mode" is enabled
        if self.is_cloudflare_iuam_challenge(resp):
            if self.tries >= 3:
                exception_message = 'Failed to solve Cloudflare challenge!'
                if os.getenv('CI') == 'true':
                    exception_message += '\n' + resp.text
                raise Exception(exception_message)

            resp = self.solve_cf_challenge(resp, **kwargs)

        return resp

    def cloudflare_is_bypassed(self, url, resp=None):
        cookie_domain = ".{}".format(urlparse(url).netloc)
        return (
            self.cookies.get("cf_clearance", None, domain=cookie_domain) or
            (resp and resp.cookies.get("cf_clearance", None, domain=cookie_domain))
        )

    def handle_captcha_challenge(self):
        exception_message = 'Cloudflare returned captcha!'
        if self.prev_resp is not None and os.getenv('CI') == 'true':
            exception_message += '\n' + self.prev_resp.text
        raise Exception(exception_message)

    def solve_cf_challenge(self, resp, **original_kwargs):
        self.tries += 1
        start_time = time.time()

        body = resp.text
        parsed_url = urlparse(resp.url)
        domain = parsed_url.netloc
        submit_url = "%s://%s/cdn-cgi/l/chk_jschl" % (parsed_url.scheme, domain)

        cloudflare_kwargs = copy.deepcopy(original_kwargs)

        headers = cloudflare_kwargs.setdefault("headers", {})
        headers["Referer"] = resp.url

        try:
            params = cloudflare_kwargs["params"] = OrderedDict(
                re.findall(r'name="(s|jschl_vc|pass)"(?: [^<>]*)? value="(.+?)"', body)
            )

            for k in ("jschl_vc", "pass"):
                if k not in params:
                    raise ValueError("%s is missing from challenge form" % k)
        except Exception as e:
            # Something is wrong with the page.
            # This may indicate Cloudflare has changed their anti-bot
            # technique. If you see this and are running the latest version,
            # please open a GitHub issue so I can update the code accordingly.
            raise ValueError(
                "Unable to parse Cloudflare anti-bot IUAM page: %s %s"
                % (e.message, BUG_REPORT)
            )

        # Solve the Javascript challenge
        answer, delay = solve_challenge(body, domain)
        params["jschl_answer"] = answer

        # Requests transforms any request into a GET after a redirect,
        # so the redirect has to be handled manually here to allow for
        # performing other types of requests even as the first request.
        method = resp.request.method
        cloudflare_kwargs["allow_redirects"] = False

        # Cloudflare requires a delay before solving the challenge
        if not self.delay:
            time.sleep(max(delay - (time.time() - start_time), 0))
        else:
            time.sleep(self.delay)
            
        # Send the challenge response and handle the redirect manually
        redirect = self.request(method, submit_url, **cloudflare_kwargs)
        redirect_location = urlparse(redirect.headers["Location"])

        if not redirect_location.netloc:
            redirect_url = urlunparse(
                (
                    parsed_url.scheme,
                    domain,
                    redirect_location.path,
                    redirect_location.params,
                    redirect_location.query,
                    redirect_location.fragment,
                )
            )
            return self.request(method, redirect_url, **original_kwargs)
        return self.request(method, redirect.headers["Location"], **original_kwargs)

create_scraper = CloudflareScraper
scraper = create_scraper()                    