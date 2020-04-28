"""

    Copyright (C) 2018

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

    Version:
        July 29, 2019
            - Added customizable setting to display all titles in a chosen color.
            - Added missing thumbnails for items from each category.
        Sep 24th, 2018
            - Updated so that thumbnails are displayed for all items in each category (Movies, Shows, Cable Channels).
        May 9th, 2018
            - Updated so that Movies, TV Shows & Cable Channels are displayed in separate categories with the contents listed in alphabetical order.
            - Updated get_shows mode so that this plugin can co-exit with the arconaitv.py plugin.

    -------------------------------------------------------------

    *** COLORS ***
        Set your desired color for the MYCOLOR variable within "" on line 80 below and all items will be displayed in that color.
        The color values must be lowercase alphanumeric (example: red, limegreen) or anycase of Hex (example: ffff0000, FF00FF00).
        If the MYCOLOR variable is left blank, it will display as the default color set within the skin you're using.

    -------------------------------------------------------------

    Usage Examples:

	* Returns a list of 24/7 Movies
    <dir>
      <title>24/7 Movies</title>
      <arconaitv2>movies</arconaitv2>
    </dir>

	* Returns a list of 24/7 TV Shows
    <dir>
      <title>24/7 TV Shows</title>
      <arconaitv2>shows</arconaitv2>
    </dir>

	* Returns a list of 24/7 Cable Channels
    <dir>
      <title>24/7 Channels</title>
      <arconaitv2>cable</arconaitv2>
    </dir>

"""

import requests, re, os, traceback, xbmc, xbmcaddon, xbmcgui
import base64, pickle, koding, time, sqlite3
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
home_folder = xbmc.translatePath('special://home/')
user_data_folder = os.path.join(home_folder, 'userdata')
addon_data_folder = os.path.join(user_data_folder, 'addon_data')
database_path = os.path.join(addon_data_folder, addon_id)
database_loc = os.path.join(database_path, 'database.db')
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

MYCOLOR = ""

class ARCONAITV(Plugin):
    name = "arconaitv2"

    def process_item(self, item_xml):
        if "<arconaitv2>" in item_xml:
            item = JenItem(item_xml)
            if "movies" in item.get("arconaitv2", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_movies2",
                    'url': item.get("arconaitv2", ""),
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
            elif "shows" in item.get("arconaitv2", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_shows2",
                    'url': item.get("arconaitv2", ""),
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
            elif "cable" in item.get("arconaitv2", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_cable2",
                    'url': item.get("arconaitv2", ""),
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


@route(mode='get_movies2', args=["url"])
def get_movies2(url):
    pins = "PLuginarconaitvtwomovies"
    Items = fetch_from_db2(pins)
    if Items:
        display_data(Items)
    else:
        xml = ""
        try:
            url = "https://www.arconaitv.us/"
            headers = {'User_Agent':User_Agent}
            html = requests.get(url,headers=headers).content
            block5 = re.compile('<div class="stream-nav movies" id="movies">(.+?)<div class="acontainer">',re.DOTALL).findall(html)
            match5 = re.compile('href=(.+?) title=(.+?)>',re.DOTALL).findall(str(block5))
            for link5,title5 in match5:
                title5 = title5.replace("\\'", "")
                title5 = remove_non_ascii(title5)
                link5 = link5.replace("\\'", "")
                link5 = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=https://www.arconaitv.us/" + link5
                image5 = get_other(title5,html)
                if not MYCOLOR == "":
                    myTitle = "[COLOR %s]%s[/COLOR]" % (MYCOLOR, title5)
                else:
                    myTitle = title5
                if image5:
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<link>"\
                           "<sublink>%s</sublink>"\
                           "</link>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>http://listtoday.org/wallpaper/2015/12/movies-in-theaters-1-desktop-background.jpg</fanart>"\
                           "<summary>Random Movies</summary>"\
                           "</plugin>" % (myTitle,link5,image5)
                elif not image5:
                    if title5 == "Action":
                        image6 = "http://icons.iconarchive.com/icons/sirubico/movie-genre/256/Action-3-icon.png"
                    elif title5 == "Animated Movies":
                        image6 = "http://www.filmsite.org/images/animated-genre.jpg"
                    elif title5 == "Christmas Movies":
                        image6 = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/i/2edc83ba-8598-4234-b910-4871b3492ce2/d9l7n0r-e34d8a12-13c6-4e06-9ebb-cfa4bac9370a.jpg"
                    elif title5 == "Comedy Movies":
                        image6 = "https://thumb9.shutterstock.com/display_pic_with_logo/882263/116548462/stock-photo-clap-film-of-cinema-comedy-genre-clapperboard-text-illustration-116548462.jpg"
                    elif title5 == "Cult Classics":
                        image6 = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/aec91c80-1de1-4757-89d3-d17feae16eed/d24l4z0-2d912894-0324-4e13-97df-8e7a42864fb0.jpg/v1/fill/w_1024,h_853,q_75,strp/young_frankenstein_by_cowboy_lucas_d24l4z0-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9ODUzIiwicGF0aCI6IlwvZlwvYWVjOTFjODAtMWRlMS00NzU3LTg5ZDMtZDE3ZmVhZTE2ZWVkXC9kMjRsNHowLTJkOTEyODk0LTAzMjQtNGUxMy05N2RmLThlN2E0Mjg2NGZiMC5qcGciLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.uVkrlf2L5aPm9MTCpFav9kDpD4eFHwkkyjGaZEmJrxE"
                    elif title5 == "Documentaries ":
                        image6 = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRc8s5haFPMPgDNmfetzNm06V3BB918tV8TG5JiJe7FaEqn-Cgx"
                    elif title5 == "Harry Potter ":
                        image6 = "http://icons.iconarchive.com/icons/aaron-sinuhe/tv-movie-folder/256/Harry-Potter-2-icon.png"
                    elif title5 == "Horror Movies":
                        image6 = "http://www.filmsite.org/images/horror-genre.jpg"
                    elif title5 == "James Bond ":
                        image6 = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/552e231a-ce52-428e-bed4-9546bacf191f/d8yxgtm-3092fb23-b741-4b9d-855d-497d15a84d79.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzU1MmUyMzFhLWNlNTItNDI4ZS1iZWQ0LTk1NDZiYWNmMTkxZlwvZDh5eGd0bS0zMDkyZmIyMy1iNzQxLTRiOWQtODU1ZC00OTdkMTVhODRkNzkucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.oT3Khot2QoNy1wOR3n6XZ390GL_pIL6rB5b9K5zQaTU"
                    elif title5 == "Lord of the Rings":
                        image6 = "https://pre00.deviantart.net/b9cd/th/pre/f/2012/043/0/4/the_lord_of_the_rings_golden_movie_logo_by_freeco-d4phvpy.jpg"
                    elif title5 == "Mafia Movies":
                        image6 = "https://cdn.pastemagazine.com/www/blogs/lists/2012/04/05/godfather-lead.jpg"
                    elif title5 == "Monster Movies":
                        image6 = "https://media.timeout.com/images/54076/630/472/image.jpg"
                    elif title5 == "Movie Night":
                        image6 = "http://jesseturri.com/wp-content/uploads/2013/03/Movie-Night-Logo.jpg"
                    elif title5 == "Movies with Arc":
                        image6 = "https://upload.wikimedia.org/wikipedia/en/thumb/a/a3/Zombieland-poster.jpg/220px-Zombieland-poster.jpg"
                    elif title5 == "Musical Movies":
                        image6 = "http://ww1.prweb.com/prfiles/2016/03/18/13294162/Broadway_Movie_Musical_Logo.jpg"
                    elif title5 == "Mystery Movies":
                        image6 = "http://icons.iconarchive.com/icons/limav/movie-genres-folder/256/Mystery-icon.png"
                    elif title5 == "Random Movies":
                        image6 = "https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/a2/93/b8/a293b81e-9781-5129-32e9-38fb63ff52f8/source/256x256bb.jpg"
                    elif title5 == "Romance Movies":
                        image6 = "http://icons.iconarchive.com/icons/limav/movie-genres-folder/256/Romance-icon.png"
                    elif title5 == "SciFi Movies":
                        image6 = "https://pbs.twimg.com/profile_images/684995547611054081/shfn1qd0.png"
                    elif title5 == "Star Trek Movies":
                        image6 = "https://topicimages.mrowl.com/large/katera/chris_hemsworth/movies/2009_star_trek_1.jpg"
                    elif title5 == "Star Wars ":
                        image6 = "http://icons.iconarchive.com/icons/aaron-sinuhe/tv-movie-folder/256/Star-Wars-2-icon.png"
                    elif title5 == "Studio Ghibli":
                        image6 = "https://orig00.deviantart.net/ec8a/f/2017/206/5/a/studio_ghibli_collection_folder_icon_by_dahlia069-dbho9mx.png"
                    elif title5 == "War Movies":
                        image6 = "http://icons.iconarchive.com/icons/limav/movie-genres-folder/512/War-icon.png"
                    elif title5 == "Western Movies":
                        image6 = "https://cdn1.player.fm/images/2222581/series/bXGU8mLKL2LsAKe0/512.jpg"
                    else:
                        image6 = "http://www.userlogos.org/files/logos/nickbyalongshot/film.png"

                    if not MYCOLOR == "":
                        myTitle = "[COLOR %s]%s[/COLOR]" % (MYCOLOR, title5)
                    else:
                        myTitle = title5
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<link>"\
                           "<sublink>%s</sublink>"\
                           "</link>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>http://listtoday.org/wallpaper/2015/12/movies-in-theaters-1-desktop-background.jpg</fanart>"\
                           "<summary>Random Movies</summary>"\
                           "</plugin>" % (myTitle,link5,image6)
        except Exception:
            failure = traceback.format_exc()
            xbmcgui.Dialog().textviewer('Exception',str(failure))
            pass
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='get_shows2', args=["url"])
def get_shows2(url):
    pins = "PLuginarconaitvtwoshows"
    Items = fetch_from_db2(pins)
    if Items:
        display_data(Items)
    else:
        xml = ""
        try:
            url = "https://www.arconaitv.us/"
            headers = {'User_Agent':User_Agent}
            html = requests.get(url,headers=headers).content
            block1 = re.compile('<div class="stream-nav shows" id="shows">(.+?)<div class="acontainer">',re.DOTALL).findall(html)
            match1 = re.compile('href=(.+?) title=(.+?)>',re.DOTALL).findall(str(block1))
            for link1,title1 in match1:
                title1 = title1.replace("\\'", "")
                title1 = remove_non_ascii(title1)
                link1 = link1.replace("\\'", "")
                link1 = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=https://www.arconaitv.us/" + link1
                image1 = get_thumb(title1,html)
                if not MYCOLOR == "":
                    myTitle = "[COLOR %s]%s[/COLOR]" % (MYCOLOR, title1)
                else:
                    myTitle = title1
                if image1:
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<link>"\
                           "<sublink>%s</sublink>"\
                           "</link>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>https://lerablog.org/wp-content/uploads/2014/05/tv-series.jpg</fanart>"\
                           "<summary>Random Episodes</summary>"\
                           "</plugin>" % (myTitle,link1,image1)
                elif not image1:
                    if title1 == "Simpsons S13+":
                        image2 = "http://icons.iconarchive.com/icons/nellanel/simpsons-folder/512/The-Simpsons-Season-13-icon.png"
                    elif title1 == "Two and Half Men":
                        image2 = "https://3.bp.blogspot.com/-JB2VNEAxvYo/W8c2odcMKkI/AAAAAAAACZk/m-lkHFcX--o1jPi4apM2kr73-ZNs5xswgCLcBGAs/s1600/dvd-two-and-a-half-men-dois-homens-e-meio-dublado-legendado-D_NQ_NP_743462-MLB27990032904_082018-F.jpg"
                    else:
                        image2 = get_other(title1,html)
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<link>"\
                           "<sublink>%s</sublink>"\
                           "</link>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>https://lerablog.org/wp-content/uploads/2014/05/tv-series.jpg</fanart>"\
                           "<summary>Random Episodes</summary>"\
                           "</plugin>" % (myTitle,link1,image2)
        except Exception:
            failure = traceback.format_exc()
            xbmcgui.Dialog().textviewer('Exception',str(failure))
            pass
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='get_cable2', args=["url"])
def get_cable2(url):
    pins = "PLuginarconaitvtwonetworks"
    Items = fetch_from_db2(pins)
    if Items:
        display_data(Items)
    else:
        xml = ""
        try:
            url = "https://www.arconaitv.us/"
            headers = {'User_Agent':User_Agent}
            html = requests.get(url,headers=headers).content
            block4 = re.compile('<div class="stream-nav cable" id="cable">(.+?)<div class="acontainer">',re.DOTALL).findall(html)
            match4 = re.compile('href=(.+?) title=(.+?)>',re.DOTALL).findall(str(block4))
            for link4,title4 in match4:
                title4 = title4.replace("\\'", "")
                title4 = remove_non_ascii(title4)
                link4 = link4.replace("\\'", "")
                link4 = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=https://www.arconaitv.us/" + link4
                image4 = get_thumb(title4,html)
                if not MYCOLOR == "":
                    myTitle = "[COLOR %s]%s[/COLOR]" % (MYCOLOR, title4)
                else:
                    myTitle = title4
                if image4:
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<link>"\
                           "<sublink>%s</sublink>"\
                           "</link>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>http://static.wixstatic.com/media/7217cd_6b6840f1821147ffa0380918a2110cdd.jpg</fanart>"\
                           "<summary>Random TV Shows</summary>"\
                           "</plugin>" % (myTitle,link4,image4)
                elif not image4:
                    if title4 == "ABC":
                        image5 = "https://vignette.wikia.nocookie.net/superfriends/images/f/f2/Abc-logo.jpg/revision/latest?cb=20090329152831"
                    elif title4 == "Animal Planet":
                        image5 = "https://seeklogo.com/images/D/discovery-animal-planet-logo-036312EA16-seeklogo.com.png"
                    elif title4 == "BBC America":
                        image5 = "https://pbs.twimg.com/profile_images/1145808101146333184/0kCJBuSE.png"
                    elif title4 == "Bravo Tv":
                        image5 = "https://kodi.tv/sites/default/files/styles/medium_crop/public/addon_assets/plugin.video.bravo/icon/icon.png?itok=VXH52Iyf"
                    elif title4 == "CNBC":
                        image5 = "https://i2.wp.com/republicreport.wpengine.com/wp-content/uploads/2014/06/cnbc1.png?resize=256%2C256"
                    elif title4 == "FOX 43 WMPT":
                        image5 = "https://lh3.googleusercontent.com/E-lunv2Udf0Csbp4ZJQCgM9Owf3WDRXreSjdmFTuWgaXlThlEXiKfKjK_l5jdegTfg"
                    elif title4 == "MavTV":
                        image5 = "https://cdn.canadasatellite.ca/media/catalog/product/cache/e4d64343b1bc593f1c5348fe05efa4a6/m/a/mav_tv.jpg"
                    elif title4 == "MSNBC":
                        image5 = "https://data.apksum.com/48/com.themediationnet.app/1.0/icon.png"
                    elif title4 == "NASA HD":
                        image5 = "https://images-eu.ssl-images-amazon.com/images/I/6111kA98OPL.png"
                    elif title4 == "NBC":
                        image5 = "https://designobserver.com/media/images/mondrian/39684-NBC_logo_m.jpg"
                    elif title4 == "SYFY":
                        image5 = "https://kodi.tv/sites/default/files/styles/medium_crop/public/addon_assets/plugin.video.syfy/icon/icon.png?itok=ZLTAqywa"
                    elif title4 == "USA Network ":
                        image5 = "https://crunchbase-production-res.cloudinary.com/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/v1442500192/vzcordlt6w0xsnhcsloa.png"
                    elif title4 == "WWOR-TV":
                        image5 = "https://i.ytimg.com/vi/TlhcM0jciZo/hqdefault.jpg"
                    else:
                        image5 = get_other(title4,html)

                    if not MYCOLOR == "":
                        myTitle = "[COLOR %s]%s[/COLOR]" % (MYCOLOR, title4)
                    else:
                        myTitle = title4
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<link>"\
                           "<sublink>%s</sublink>"\
                           "</link>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>http://static.wixstatic.com/media/7217cd_6b6840f1821147ffa0380918a2110cdd.jpg</fanart>"\
                           "<summary>Random TV Shows</summary>"\
                           "</plugin>" % (myTitle,link4,image5)
        except Exception:
            failure = traceback.format_exc()
            xbmcgui.Dialog().textviewer('Exception',str(failure))
            pass
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


def remove_non_ascii(text):
    return unidecode(text)


def get_thumb(name,html):
    block2 = re.compile('<div class="content">(.+?)<div class="stream-nav shows" id="shows">',re.DOTALL).findall(html)
    match2 = re.compile('<img src=(.+?) alt=(.+?) />',re.DOTALL).findall(str(block2))
    for image,name2 in match2:
        if name in name2:
            image = image.replace("\\'", "")
            image = "https://www.arconaitv.us" + image
            return image


def get_other(name,html):
    block3 = re.compile("<div class='row stream-list-featured'>(.+?)<div class='row stream-list'>",re.DOTALL).findall(html)
    match3 = re.compile('title=(.+?) class.+?<img src=(.+?) alt',re.DOTALL).findall(str(block3))
    for name3,image3 in match3:
        if name in name3:
            image3 = image3.replace("\\'", "")
            image3 = "https://www.arconaitv.us" + image3
            return image3

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