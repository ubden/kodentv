"""
    OTB Audiobook.py
    Copyright (C) 2018, Team OTB
    Version 1.0.7

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

    Search the Audiobook List

    <dir>
    <title>Search OTB Audiobook</title>
    <otb_audb>search</otb_audb>
    </dir>

    Returns the Audionbook list

    <dir>
    <title>OTB Audiobook List</title>
    <otb_audb>all</otb_audb>
    </dir>

    

    ---------------------

    Possible Genre's are:
    Adventure
    Biography
    Children
    Fantasy
    Fiction
    History
    Horror
    Mystery
    Non-Fiction
    Science Fiction
    Thriller

    -----------------------

    Genre tag examples

    <dir>
    <title>Fiction</title>
    <otb_audb>genre/Fiction</otb_audb>
    </dir>

    <dir>
    <title>Mystery</title>
    <otb_audb>genre/Mystery</otb_audb>
    </dir>    
    
    --------------------------------------------------------------

"""


import requests,re,os,xbmc,xbmcaddon
import base64,pickle,koding,time,sqlite3
import base64
from koding import route
from ..plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list, display_data, clean_url
from resources.lib.external.airtable.airtable import Airtable
from unidecode import unidecode

CACHE_TIME = 3600  # change to wanted cache time in seconds

bec = base64.b64encode
bdc = base64.b64decode
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
AddonName = xbmcaddon.Addon(AddonName).getAddonInfo('id')
yai = bec(AddonName)
tid = bdc('YXBwZ0YySXMxRmhFME5FT3E=')
tnm = bdc('b3RiX2F1ZGlvYm9va3NfaWRz')
atk = bdc('a2V5T0hheHNUR3pIVTlFRWg=')


class OTB_Audiobook_List(Plugin):
    name = "otb_audiobook_list"

    def process_item(self, item_xml):
        if "<otb_audb>" in item_xml:
            item = JenItem(item_xml)
            if "all" in item.get("otb_audb", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_audb",
                    'url': "",
                    'folder': True,
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
            elif "genre" in item.get("otb_audb", ""):    
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_audb2",
                    'url': item.get("otb_audb", ""),
                    'folder': True,
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
            elif "search" in item.get("otb_audb", ""):    
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_audb_search",
                    'url': item.get("otb_audb", ""),
                    'folder': True,
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

def display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5):
    xml = ""
    if link2 == "-":
        xml += "<item>"\
             "<title>%s</title>"\
             "<meta>"\
             "<content>movie</content>"\
             "<title></title>"\
             "<year></year>"\
             "<thumbnail>%s</thumbnail>"\
             "<fanart>%s</fanart>"\
             "<summary>%s</summary>"\
             "</meta>"\
             "<link>"\
             "<sublink>%s</sublink>"\
             "</link>"\
             "</item>" % (name,thumbnail,fanart,summary,link1)
    elif link3 == "-":
        xml += "<item>"\
             "<title>%s</title>"\
             "<meta>"\
             "<content>movie</content>"\
             "<title></title>"\
             "<year></year>"\
             "<thumbnail>%s</thumbnail>"\
             "<fanart>%s</fanart>"\
             "<summary>%s</summary>"\
             "</meta>"\
             "<link>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "</link>"\
             "</item>" % (name,thumbnail,fanart,summary,link1,link2) 
    elif link4 == "-":
        xml += "<item>"\
             "<title>%s</title>"\
             "<meta>"\
             "<content>movie</content>"\
             "<title></title>"\
             "<year></year>"\
             "<thumbnail>%s</thumbnail>"\
             "<fanart>%s</fanart>"\
             "<summary>%s</summary>"\
             "</meta>"\
             "<link>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "</link>"\
             "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3)
    elif link5 == "-":
        xml += "<item>"\
             "<title>%s</title>"\
             "<meta>"\
             "<content>movie</content>"\
             "<title></title>"\
             "<year></year>"\
             "<thumbnail>%s</thumbnail>"\
             "<fanart>%s</fanart>"\
             "<summary>%s</summary>"\
             "</meta>"\
             "<link>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "</link>"\
             "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4)
    else:
        xml += "<item>"\
             "<title>%s</title>"\
             "<meta>"\
             "<content>movie</content>"\
             "<title></title>"\
             "<year></year>"\
             "<thumbnail>%s</thumbnail>"\
             "<fanart>%s</fanart>"\
             "<summary>%s</summary>"\
             "</meta>"\
             "<link>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "</link>"\
             "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4,link5)
    return (xml)

@route(mode='open_otb_audb')
def open_movies():
    pins = "PLuginotbaudiobook"
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:    
        xml = ""
        lai = []
        at1 = Airtable(tid, tnm, api_key=atk)
        m1 = at1.get_all(maxRecords=1200, view='Grid view') 
        for f1 in m1:
            r1 = f1['fields']   
            n1 = r1['au1']
            lai.append(n1)
        if yai in lai:
            pass
        else:
            exit()     
        at = Airtable('appwblOWrmZ5uwcce', 'OTB Audiobooks', api_key='keyem86gyhcLFSLqh')
        match = at.get_all(maxRecords=1200, sort=['name'])
        for field in match:
            try:
                res = field['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']  
                link5 = res['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                    
            except:
                pass    
        at2 = Airtable('appOKb0JBT9M0MivF', 'OTB Audiobooks 2', api_key='keyem86gyhcLFSLqh')
        match2 = at2.get_all(maxRecords=1200, sort=['name'])      
        for field2 in match2:
            try:
                res = field2['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']
                link5 = res['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
            except:
                pass
        at3 = Airtable('appGoC0VblD0MCcvw', 'OTB Audiobooks 3', api_key='keyem86gyhcLFSLqh')
        match3 = at3.get_all(maxRecords=1200, sort=['name'])      
        for field3 in match3:
            try:
                res = field3['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']
                link5 = res['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
            except:
                pass
        at4 = Airtable('appYbxBoLWcYY9LSI', 'OTB Audiobooks 4', api_key='keyem86gyhcLFSLqh')
        match4 = at4.get_all(maxRecords=1200, sort=['name'])      
        for field4 in match4:
            try:
                res = field4['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']
                link5 = res['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
            except:
                pass
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

@route(mode='open_otb_audb2',args=["url"])
def open_action_movies(url):
    genre = url.split("/")[-1]
    pins = "PLuginotbaudiobook" + genre
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else: 
        xml = ""
        lai = []
        at1 = Airtable(tid, tnm, api_key=atk)
        m1 = at1.get_all(maxRecords=1200, view='Grid view') 
        for f1 in m1:
            r1 = f1['fields']   
            n1 = r1['au1']
            lai.append(n1)
        if yai in lai:
            pass
        else:
            exit()    
        at = Airtable('appwblOWrmZ5uwcce', 'OTB Audiobooks', api_key='keyem86gyhcLFSLqh')
        try:
            match = at.search('type', genre, sort=['name'])
            for field in match:
                res = field['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']
                link5 = res['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
        except:
            pass 
        at2 = Airtable('appOKb0JBT9M0MivF', 'OTB Audiobooks 2', api_key='keyem86gyhcLFSLqh')
        try:
            match2 = at2.search('type', genre, sort=['name'])
            for field2 in match2:
                res = field2['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']
                link5 = res['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                  
        except:
            pass
        at3 = Airtable('appGoC0VblD0MCcvw', 'OTB Audiobooks 3', api_key='keyem86gyhcLFSLqh')
        match3 = at3.search('type', genre, sort=['name'])      
        for field3 in match3:
            try:
                res = field3['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']
                link5 = res['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
            except:
                pass
        at4 = Airtable('appYbxBoLWcYY9LSI', 'OTB Audiobooks 4', api_key='keyem86gyhcLFSLqh')
        match4 = at4.search('type', genre, sort=['name'])     
        for field4 in match4:
            try:
                res = field4['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']
                link5 = res['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
            except:
                pass
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='open_otb_audb_search')
def open_bml_search():
    pins = ""
    xml = ""
    lai = []
    at1 = Airtable(tid, tnm, api_key=atk)
    m1 = at1.get_all(maxRecords=1200, view='Grid view') 
    for f1 in m1:
        r1 = f1['fields']   
        n1 = r1['au1']
        lai.append(n1)
    if yai in lai:
        pass
    else:
        exit()
    show = koding.Keyboard(heading='Movie Name')
    movie_list = []
    at = Airtable('appwblOWrmZ5uwcce', 'OTB Audiobooks', api_key='keyem86gyhcLFSLqh')
    match = at.get_all(maxRecords=1200, sort=['name'])
    for field in match:
        res = field['fields']        
        name = res['name']
        movie_list.append(name)
    at2 = Airtable('appOKb0JBT9M0MivF', 'OTB Audiobooks 2', api_key='keyem86gyhcLFSLqh')
    match2 = at2.get_all(maxRecords=1200, sort=['name'])  
    for field2 in match2:       
        res2 = field2['fields']        
        name2 = res2['name']
        movie_list.append(name2)
    at3 = Airtable('appGoC0VblD0MCcvw', 'OTB Audiobooks 3', api_key='keyem86gyhcLFSLqh')
    match3 = at3.get_all(maxRecords=1200, sort=['name'])  
    for field3 in match3:       
        res3 = field3['fields']        
        name3 = res3['name']
        movie_list.append(name3)
    at4 = Airtable('appYbxBoLWcYY9LSI', 'OTB Audiobooks 4', api_key='keyem86gyhcLFSLqh')
    match4 = at4.get_all(maxRecords=1200, sort=['name'])  
    for field4 in match4:       
        res4 = field4['fields']        
        name4 = res4['name']
        movie_list.append(name4) 
    search_result = koding.Fuzzy_Search(show, movie_list)
    if not search_result:
        xbmc.log("--------no results--------",level=xbmc.LOGNOTICE)
        xml += "<item>"\
            "<title>[COLOR=orange][B]Movie was not found[/B][/COLOR]</title>"\
            "</item>"
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type())    
    for item in search_result:
        item2 = str(item)
        item2 = remove_non_ascii(item2)           
        try:
            match2 = at.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)
        except:
            pass        
        try:
            match2 = at2.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
        except:
            pass
        try:
            match2 = at3.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
        except:
            pass
        try:
            match2 = at4.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
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
        
