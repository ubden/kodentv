# -*- coding: utf-8 -*-
"""

    Copyright (C) 2018 TonyH
    Version 2.1.2 

    2-8-20
    -- Added resolver to the plugin. No longer needs sports devil to play the links --
    -- New xml tags are needed for this version, they are listed below --

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

-------------
    Display only Tv Shows:
<dir>
<title>Arconaitv 24-7</title>
<arconaitv>main/shows</arconaitv>
</dir>

-------------
    Display only Networks:
<dir>
<title>Arconaitv 24-7</title>
<arconaitv>main/networks</arconaitv>
</dir>    

-------------
    Display only Movies:
<dir>
<title>Arconaitv 24-7</title>
<arconaitv>main/movies</arconaitv>
</dir>     

-------------
    Display Tv Shows and Networks:
<dir>
<title>Arconaitv 24-7</title>
<arconaitv>main/shows/networks</arconaitv>
</dir>

------------
    Display Tv Shows and Movies:
<dir>
<title>Arconaitv 24-7</title>
<arconaitv>main/shows/movies</arconaitv>
</dir>

------------
    Display Networks and Movies:
<dir>
<title>Arconaitv 24-7</title>
<arconaitv>main/networks/movies</arconaitv>
</dir>

------------
    Display Tv Shows and Networks and Movies:
<dir>
<title>Arconaitv 24-7</title>
<arconaitv>main/shows/networks/movies</arconaitv>
</dir>                 
 

"""    

import requests,re,os,xbmc,xbmcaddon,xbmcgui
import base64,pickle,koding,time,sqlite3
from koding import route
from ..plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list, display_data, clean_url
from resources.lib.external.airtable.airtable import Airtable
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

class ARCONAITV(Plugin):
    name = "arconaitv"

    def process_item(self, item_xml):
        if "<arconaitv>" in item_xml:
            item = JenItem(item_xml)
            if "main" in item.get("arconaitv",""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_shows",
                    'url': item.get("arconaitv", ""),
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
            elif "ArcLink" in item.get("arconaitv",""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_arconaitv_links",
                    'url': item.get("arconaitv", ""),
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

@route(mode='get_shows', args=["url"])
def get_shows(url):
    pins = ""
    xml = ""
    try:  
        url2 = "https://www.arconaitv.us/"
        headers = {'User_Agent':User_Agent}
        html = requests.get(url2,headers=headers).content
        if url == "main/shows":
            tv_shows(html)
        elif url == "main/networks":
            networks(html)
        elif url == "main/movies":
            movies(html)
        elif url == "main/shows/networks":
            tv_shows(html)        
            networks(html)
        elif url == "main/shows/movies":
            tv_shows(html)
            movies(html)
        elif url == "main/networks/movies":
            networks(html)
            movies(html)
        elif url == "main/shows/networks/movies":
            tv_shows(html)
            networks(html)
            movies(html)
        # elif url == "":
        #     pass                                                                                
    except:
        pass
 

def tv_shows(html):
    pins = "PLuginarconaitvshows"
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:     
        xml = ""
        try:
            block = re.compile('<div class="stream-nav shows" id="shows">(.+?)<div class="acontainer">',re.DOTALL).findall(html)
            match = re.compile('href=(.+?) title=(.+?)>',re.DOTALL).findall(str(block))
            xml += "<item>"\
                   "<title>[COLOR blue][B]----TV SHOWS----[/B][/COLOR]</title>"\
                   "<thumbnail>http://iconbug.com/data/2b/256/c6cbe045e598958b1efacc78b4127205.png</thumbnail>"\
                   "<fanart>https://lerablog.org/wp-content/uploads/2014/05/tv-series.jpg</fanart>"\
                   "<link></link>"\
                   "</item>"        
            for link,name in match:
                name = name.replace("\\'","")
                name = remove_non_ascii(name)
                link = link.replace("\\'","")
                link = "https://www.arconaitv.us/"+link
                image2 = get_thumb(name,html)            
                if image2:
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>https://lerablog.org/wp-content/uploads/2014/05/tv-series.jpg</fanart>"\
                           "<summary>Random Episodes</summary>"\
                           "<arconaitv>ArcLink**%s**%s**%s</arconaitv>"\
                           "</plugin>" % (name,image2,link,name,image2)                       
                elif not image2:
                    image3 = get_other(name,html)
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>https://lerablog.org/wp-content/uploads/2014/05/tv-series.jpg</fanart>"\
                           "<summary>Random Episodes</summary>"\
                           "<arconaitv>ArcLink**%s**%s**%s</arconaitv>"\
                           "</plugin>" % (name,image3,link,name,image3)
        except:
            pass               
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), "movies", pins)                        

def networks(html):
    pins = "PLuginarconaitvnetworks"
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:     
        xml = ""
        try:
            block4 = re.compile('<div class="stream-nav cable" id="cable">(.+?)<div class="acontainer">',re.DOTALL).findall(html)
            match4 = re.compile('href=(.+?) title=(.+?)>',re.DOTALL).findall(str(block4))
            xml += "<item>"\
                   "<title>[COLOR blue][B]----NETWORKS----[/B][/COLOR]</title>"\
                   "<thumbnail>https://pmcdeadline2.files.wordpress.com/2010/09/networks.jpg</thumbnail>"\
                   "<fanart>http://static.wixstatic.com/media/7217cd_6b6840f1821147ffa0380918a2110cdd.jpg</fanart>"\
                   "<link></link>"\
                   "</item>"
            for link,name in match4:
                name = name.replace("\\'","")
                name = remove_non_ascii(name)
                link = link.replace("\\'","")
                link = "https://www.arconaitv.us/"+link
                image2 = get_thumb(name,html)            
                if image2:
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>http://static.wixstatic.com/media/7217cd_6b6840f1821147ffa0380918a2110cdd.jpg</fanart>"\
                           "<summary>Random TV Shows</summary>"\
                           "<arconaitv>ArcLink**%s**%s**%s</arconaitv>"\
                           "</plugin>" % (name,image2,link,name,image2)                       
                elif not image2:
                    image3 = get_other(name,html)
                    if name == "ABC":
                        image3 = "https://vignette.wikia.nocookie.net/superfriends/images/f/f2/Abc-logo.jpg/revision/latest?cb=20090329152831"
                    elif name == "Animal Planet":
                        image3 = "https://seeklogo.com/images/D/discovery-animal-planet-logo-036312EA16-seeklogo.com.png"
                    elif name == "Bravo Tv":
                        image3 = "https://kodi.tv/sites/default/files/styles/medium_crop/public/addon_assets/plugin.video.bravo/icon/icon.png?itok=VXH52Iyf"
                    elif name == "CNBC":
                        image3 = "https://i2.wp.com/republicreport.wpengine.com/wp-content/uploads/2014/06/cnbc1.png?resize=256%2C256"
                    elif name == "NBC":
                        image3 = "https://designobserver.com/media/images/mondrian/39684-NBC_logo_m.jpg"
                    elif name == "SYFY":
                        image3 = "https://kodi.tv/sites/default/files/styles/medium_crop/public/addon_assets/plugin.video.syfy/icon/icon.png?itok=ZLTAqywa"
                    elif name == "USA Network ":
                        image3 = "https://crunchbase-production-res.cloudinary.com/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/v1442500192/vzcordlt6w0xsnhcsloa.png"
                    elif name == "WWOR-TV":
                        image3 = "https://i.ytimg.com/vi/TlhcM0jciZo/hqdefault.jpg"
                    elif name == "BBC America":
                        image3 = "https://watchuktvabroad.net/dev/wp-content/uploads/2014/05/bbc1-icon.png"
                    elif name == "MavTV":
                        image3 = "https://yt3.ggpht.com/a-/ACSszfGbltb7pvCn52Ojd3vEHPk_2v_1_HJosa_h=s900-mo-c-c0xffffffff-rj-k-no"
                    elif name == "MSNBC":
                        image3 = "https://upload.wikimedia.org/wikipedia/commons/7/74/MSNBC_logo.png"
                    elif name == "NASA HD":
                        image3 = "http://pluspng.com/img-png/nasa-logo-png-nasa-logo-3400.png"                                                                                                                                                
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>http://static.wixstatic.com/media/7217cd_6b6840f1821147ffa0380918a2110cdd.jpg</fanart>"\
                           "<summary>Random TV Shows</summary>"\
                           "<arconaitv>ArcLink**%s**%s**%s</arconaitv>"\
                           "</plugin>" % (name,image3,link,name,image3)
        except:
            pass                   
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), "movies", pins)

def movies(html):
    pins = "PLuginarconaitvmovies"
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:     
        xml = ""
        try:
            block5 = re.compile('<div class="stream-nav movies" id="movies">(.+?)<div class="acontainer">',re.DOTALL).findall(html)
            match5 = re.compile('href=(.+?) title=(.+?)>',re.DOTALL).findall(str(block5))                       
            xml += "<item>"\
                   "<title>[COLOR blue][B]----MOVIES----[/B][/COLOR]</title>"\
                   "<thumbnail>https://archive.org/services/img/movies-icon_201707</thumbnail>"\
                   "<fanart>http://listtoday.org/wallpaper/2015/12/movies-in-theaters-1-desktop-background.jpg</fanart>"\
                   "<link></link>"\
                   "</item>"
            for link,name in match5:
                name = name.replace("\\'","")
                name = remove_non_ascii(name)
                link = link.replace("\\'","")
                link = "https://www.arconaitv.us/"+link
                image3 = get_other(name,html)                                                                                      
                if image3:
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>http://listtoday.org/wallpaper/2015/12/movies-in-theaters-1-desktop-background.jpg</fanart>"\
                           "<summary>Random Movies</summary>"\
                           "<arconaitv>ArcLink**%s**%s**%s</arconaitv>"\
                           "</plugin>" % (name,image3,link,name,image3)
                elif not image3:
                    #image3 = "http://www.userlogos.org/files/logos/nickbyalongshot/film.png"
                    image3 = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/0d920358-1c79-4669-b107-2b22e0dd7dcd/d8nntky-04e9b7c7-1d09-44d8-8c24-855a19988294.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzBkOTIwMzU4LTFjNzktNDY2OS1iMTA3LTJiMjJlMGRkN2RjZFwvZDhubnRreS0wNGU5YjdjNy0xZDA5LTQ0ZDgtOGMyNC04NTVhMTk5ODgyOTQucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.To4Xk896HVjziIt-LjTSotZR0x7NVCbroAIkiSpik84"
                    # if name == "Action":
                    #     image3 = "http://icons.iconarchive.com/icons/sirubico/movie-genre/256/Action-3-icon.png"
                    # if name == "Animation Movies":
                    #     image3 = "http://www.filmsite.org/images/animated-genre.jpg"
                    # if name == "Christmas Movies":
                    #     image3 = "http://img.sj33.cn/uploads/allimg/201009/20100926224051989.png"
                    # if name == "Comedy Movies":
                    #     image3 = "https://thumb9.shutterstock.com/display_pic_with_logo/882263/116548462/stock-photo-clap-film-of-cinema-comedy-genre-clapperboard-text-illustration-116548462.jpg"
                    # if name == "Documentaries ":
                    #     image3 = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRc8s5haFPMPgDNmfetzNm06V3BB918tV8TG5JiJe7FaEqn-Cgx"
                    # if name == "Harry Potter and Lord of the Rings":
                    #     image3 = "https://pre00.deviantart.net/b9cd/th/pre/f/2012/043/0/4/the_lord_of_the_rings_golden_movie_logo_by_freeco-d4phvpy.jpg"
                    # if name == "Horror Movies":
                    #     image3 = "http://www.filmsite.org/images/horror-genre.jpg"
                    # if name == "Mafia Movies":
                    #     image3 = "https://cdn.pastemagazine.com/www/blogs/lists/2012/04/05/godfather-lead.jpg"
                    # if name == "Movie Night":
                    #     image3 = "http://jesseturri.com/wp-content/uploads/2013/03/Movie-Night-Logo.jpg"
                    # if name == "Musical Movies":
                    #     image3 = "http://ww1.prweb.com/prfiles/2016/03/18/13294162/Broadway_Movie_Musical_Logo.jpg"
                    # if name == "Mystery Movies":
                    #     image3 = "http://icons.iconarchive.com/icons/limav/movie-genres-folder/256/Mystery-icon.png"
                    # if name == "Random Movies":
                    #     image3 = "https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/a2/93/b8/a293b81e-9781-5129-32e9-38fb63ff52f8/source/256x256bb.jpg"
                    # if name == "Romance Movies":
                    #     image3 = "http://icons.iconarchive.com/icons/limav/movie-genres-folder/256/Romance-icon.png"
                    # if name == "Star Wars and Star Trek":
                    #     image3 = "http://icons.iconarchive.com/icons/aaron-sinuhe/tv-movie-folder/256/Star-Wars-2-icon.png"
                    # if name == "Studio Ghibli":
                    #     image3 = "https://orig00.deviantart.net/ec8a/f/2017/206/5/a/studio_ghibli_collection_folder_icon_by_dahlia069-dbho9mx.png"                                      
                                                                                                                                                                                                                                                                    
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>http://listtoday.org/wallpaper/2015/12/movies-in-theaters-1-desktop-background.jpg</fanart>"\
                           "<summary>Random Movies</summary>"\
                           "<arconaitv>ArcLink**%s**%s**%s</arconaitv>"\
                           "</plugin>" % (name,image3,link,name,image3)
        except:
            pass                   
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), "movies", pins)                                                  
            
def get_thumb(name,html):
    block2 = re.compile('<div class="content">(.+?)<div class="stream-nav shows" id="shows">',re.DOTALL).findall(html)
    match2 = re.compile('<img src=(.+?) alt=(.+?) />',re.DOTALL).findall(str(block2))
    for image,name2 in match2:
        if name in name2:
            image = image.replace("\\'", "")
            image = "https://www.arconaitv.us"+image
            return image

def get_other(name,html):
    block3 = re.compile("<div class='row stream-list-featured'>(.+?)<div class='row stream-list'>",re.DOTALL).findall(html)
    match3 = re.compile('title=(.+?) class.+?<img src=(.+?) alt',re.DOTALL).findall(str(block3))
    for name3,image3 in match3:
        if name in name3:
            image3 = image3.replace("\\'", "")
            image3 = "https://www.arconaitv.us"+image3
            return image3            
  
@route(mode='get_arconaitv_links', args=["url"])  
def get_link(url):
    koding.Show_Busy(status=True)
    url2 = url.split("**")[-3]
    name = url.split("**")[-2]
    image = url.split("**")[-1]
    html = requests.get(url2).content
    match = re.compile('eval\(function(.+?)</script>',re.DOTALL).findall(html)
    

    def _filterargs(source):
        """Juice from a source file the four args needed by decoder."""
        argsregex = (r"}\s*\('(.*)',\s*(.*?),\s*(\d+),\s*'(.*?)'\.split\('\|'\)")
        args = re.search(argsregex, source, re.DOTALL).groups()

        try:
            payload, radix, count, symtab = args
            radix = 36 if not radix.isdigit() else int(radix)
            return payload, symtab.split('|'), radix, int(count)
        except ValueError:
            raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

    def _replacestrings(source):
        """Strip string lookup table (list) and replace values in source."""
        match = re.search(r'var *(_\w+)\=\["(.*?)"\];', source, re.DOTALL)

        if match:
            varname, strings = match.groups()
            startpoint = len(match.group(0))
            lookup = strings.split('","')
            variable = '%s[%%d]' % varname
            for index, value in enumerate(lookup):
                source = source.replace(variable % index, '"%s"' % value)
            return source[startpoint:]
        return source

    def unpack(source):
        """Unpacks P.A.C.K.E.R. packed js code."""
        payload, symtab, radix, count = _filterargs(source)

        if count != len(symtab):
            raise UnpackingError('Malformed p.a.c.k.e.r. symtab.')

        try:
            unbase = Unbaser(radix)
        except TypeError:
            raise UnpackingError('Unknown p.a.c.k.e.r. encoding.')

        def lookup(match):
            """Look up symbols in the synthetic symtab."""
            word = match.group(0)
            return symtab[unbase(word)] or word

        source = re.sub(r'\b\w+\b', lookup, payload)
        return _replacestrings(source)

    class Unbaser(object):
        """Functor for a given base. Will efficiently convert
        strings to natural numbers."""
        ALPHABET = {
            62: '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
            95: (' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                 '[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
        }

        def __init__(self, base):
            self.base = base

            # If base can be handled by int() builtin, let it do it for us
            if 2 <= base <= 36:
                self.unbase = lambda string: int(string, base)
            else:
                if base < 62:
                    self.ALPHABET[base] = self.ALPHABET[62][0:base]
                elif 62 < base < 95:
                    self.ALPHABET[base] = self.ALPHABET[95][0:base]
                # Build conversion dictionary cache
                try:
                    self.dictionary = dict((cipher, index) for index, cipher in enumerate(self.ALPHABET[base]))
                except KeyError:
                    raise TypeError('Unsupported base encoding.')

                self.unbase = self._dictunbaser

        def __call__(self, string):
            return self.unbase(string)

        def _dictunbaser(self, string):
            """Decodes a  value to an integer."""
            ret = 0
            for index, cipher in enumerate(string[::-1]):
                ret += (self.base ** index) * self.dictionary[cipher]
            return ret

    test = "eval(function"+match[0]
    res = (unpack(test))
    link = re.compile("src:(.+?),",re.DOTALL).findall(res)
    link = link[0].replace("\\'", "")
    User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
    flink = link +"|User-Agent="+User_Agent
    koding.Show_Busy(status=False )
    info = xbmcgui.ListItem(name, thumbnailImage=image)
    xbmc.Player().play(flink,info)
    stop()

def remove_non_ascii(text):
    return unidecode(text)
           
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