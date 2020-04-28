"""

    Copyright (C) 2018, MuadDib

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
    Changelog:
        2019.6.28:
            - Added opening page listing all categories

        2019.6.28:
            - Converted to Jen 2.0

        2018.7.2:
            - Added Clear Cache function
            - Minor update on fetch cache returns

        2018.6.21:
            - Added caching to primary menus (Cache time is 3 hours)


    Usage Examples:
<dir>
    <title>Collection of Best Porn Categories</title>
    <cobp>allcats</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Squirting</title>
    <cobp>category/squirting</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Big Ass</title>
    <cobp>category/Big Ass</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Amateur</title>
    <cobp>category/Amateur</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Anal</title>
    <cobp>category/Anal</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Asian</title>
    <cobp>category/Asian</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-BBC</title>
    <cobp>category/BBC</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Big Dick</title>
    <cobp>category/Big Dick</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Big Tits</title>
    <cobp>category/Big Tits</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Blonde</title>
    <cobp>category/Blonde</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Blowjobs</title>
    <cobp>category/Blowjobs</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-British</title>
    <cobp>category/British</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Brunette</title>
    <cobp>category/Brunette</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Casting</title>
    <cobp>category/Casting</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Couple</title>
    <cobp>category/Couple</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Cream Pie</title>
    <cobp>category/Cream Pie</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Czech</title>
    <cobp>category/Czech</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-German</title>
    <cobp>category/German</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Girlfriend</title>
    <cobp>category/Girlfriend</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Glamcore</title>
    <cobp>category/Glamcore</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Hairy</title>
    <cobp>category/Hairy</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Japanese</title>
    <cobp>category/Japanese</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Latin</title>
    <cobp>category/Latin</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Milf</title>
    <cobp>category/Milf</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Old And Young</title>
    <cobp>category/Old And Young</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Redheads</title>
    <cobp>category/Redheads</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Russian</title>
    <cobp>category/Russian</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Schoolgirl</title>
    <cobp>category/Schoolgirl</cobp>
</dir>

<dir>
    <title>Collection of Best Porn-Teen</title>
    <cobp>category/Teen</cobp>
</dir>



"""

import requests,re,json,os,urlparse,base64
import koding
import __builtin__
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util import dom_parser
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list, display_data, clean_url
from unidecode import unidecode

CACHE_TIME = 3600  # change to wanted cache time in seconds
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
home_folder = xbmc.translatePath('special://home/')
user_data_folder = os.path.join(home_folder, 'userdata')
addon_data_folder = os.path.join(user_data_folder, 'addon_data')
database_path = os.path.join(addon_data_folder, addon_id)
database_loc = os.path.join(database_path, 'database.db')
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

class COBP(Plugin):
    name = "cobp"

    def process_item(self, item_xml):
        if "<cobp>" in item_xml:
            item = JenItem(item_xml)
            if "http" in item.get("cobp", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "PlayVideo",
                    'url': item.get("cobp", ""),
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
            elif "category" in item.get("cobp", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "COBP",
                    'url': item.get("cobp", ""),
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

            elif "allcats" in item.get("cobp", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "all_cats",
                    'url': item.get("cobp", ""),
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


@route(mode='COBP', args=["url"])
def get_stream(url):
    cat = url.split("/")[-1]
    pins = "PLugincobp"+cat
    Items = fetch_from_db2(pins)
    if Items:
        display_data(Items)  
    xml = ""
    try:
        url = urlparse.urljoin('http://collectionofbestporn.com/', url)
        headers = {'User_Agent':User_Agent}
        html = requests.get(url,headers=headers).content
        vid_divs = dom_parser.parseDOM(html, 'div', attrs={'class':'video-item col-sm-5 col-md-4 col-xs-10'})
        count = 0
        for vid_section in vid_divs:
            thumb_div = dom_parser.parseDOM(vid_section, 'div', attrs={'class':'video-thumb'})[0]
            thumbnail = re.compile('<img src="(.+?)"',re.DOTALL).findall(str(thumb_div))[0]
            vid_page_url = re.compile('href="(.+?)"',re.DOTALL).findall(str(thumb_div))[0]

            title_div = dom_parser.parseDOM(vid_section, 'div', attrs={'class':'title'})[0]
            title = remove_non_ascii(re.compile('title="(.+?)"',re.DOTALL).findall(str(title_div))[0])
            count += 1

            xml += "<item>"\
                   "    <title>%s</title>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "    <cobp>%s</cobp>"\
                   "    <summary>%s</summary>"\
                   "</item>" % (title,thumbnail,vid_page_url, title)

            if count == 24:
                pagination = dom_parser.parseDOM(html, 'li', attrs={'class':'next'})[0]
                next_page = dom_parser.parseDOM(pagination, 'a', ret='href')[0]
                xml += "<dir>"\
                       "    <title>Next Page</title>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "    <cobp>%s</cobp>"\
                       "</dir>" % (addon_icon,next_page)
    except:
        pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='PlayVideo', args=["url"])
def play_source(url):
    try:
        headers = {'User_Agent':User_Agent}
        vid_html = requests.get(url,headers=headers).content

        sources = dom_parser.parseDOM(vid_html, 'source', ret='src')
        vid_url = sources[len(sources)-1]

        xbmc.executebuiltin("PlayMedia(%s)" % vid_url)
    except:
        return

@route(mode='all_cats', args=["url"])
def get_stream(url):
    pins = "PLugincobpall"
    Items = fetch_from_db2(pins)
    if Items:
        display_data(Items)  
    xml = ""
    try:
        url = "https://collectionofbestporn.com/channels/"
        headers = {'User_Agent':User_Agent}
        html = requests.get(url, headers = headers).content
        block = re.compile('<h2>Categories</h2>(.+?)<footer>',re.DOTALL).findall(html)
        match = re.compile('<div class="video-thumb">.+?<a href="(.+?)".+?<img src="(.+?)".+?title="(.+?)"',re.DOTALL).findall(str(block))
        for link, image, name in match:
            xml += "<dir>"\
                   "    <title>%s</title>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "    <cobp>category/%s</cobp>"\
                   "    <summary></summary>"\
                   "</dir>" % (name,image,name)            
    except:
        pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

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
        if float(created_time) + CACHE_TIME <= time.time():
            koding.Remove_Table(url2)
            db = sqlite3.connect('%s' % (database_loc))        
            cursor = db.cursor()
            db.execute("vacuum")
            db.commit()
            db.close()
            return result
        else:
            pass                     
        return result
    else:
        return []

def remove_non_ascii(text):
    return unidecode(text)
