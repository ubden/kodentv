# -*- coding: utf-8 -*-
"""
    OTB Wrestling Test
    Copyright (C) 2018,
    Version 1.0.1
    OTB

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


    Returns the OTB Wrestling List

    <dir>
    <title>OTB Wrestling</title>
    <wrestle>all</wrestle>
    </dir>
   
    --------------------------------------------------------------

"""



import requests,re,os,xbmc,xbmcaddon
import base64,pickle,koding,time,sqlite3
from koding import route
from ..plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list, display_data, clean_url
from resources.lib.external.airtable.airtable import Airtable
from unidecode import unidecode

CACHE_TIME = 86400  # change to wanted cache time in seconds

bec = base64.b64encode
bdc = base64.b64decode
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
home_folder = xbmc.translatePath('special://home/')
user_data_folder = os.path.join(home_folder, 'userdata')
addon_data_folder = os.path.join(user_data_folder, 'addon_data')
database_path = os.path.join(addon_data_folder, addon_id)
database_loc = os.path.join(database_path, 'database.db')
yai = bec(AddonName)
tid = bdc('YXBwTWx5NjFhY0hvd2FFRXk=')
tnm = bdc('b3RiXyx3cmVzdGxlX2lkcw==')
atk = bdc('a2V5T0hheHNUR3pIVTlFRWg=')

class Otb_wrestle(Plugin):
    name = "otb_wrestle"

    def process_item(self, item_xml):
        if "<wrestle>" in item_xml:
            item = JenItem(item_xml)
            if "all" in item.get("wrestle", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_wrestle_list",
                    'url': item.get("wrestle", ""),
                    'folder': True,
                    'imdb': "0",
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
            elif "open|" in item.get("wrestle", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_wrestle_items",
                    'url': item.get("wrestle", ""),
                    'folder': True,
                    'imdb': "0",
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
            elif "shows|" in item.get("wrestle", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_wrestle_shows",
                    'url': item.get("wrestle", ""),
                    'folder': True,
                    'imdb': "0",
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
            elif "tv_shows|" in item.get("wrestle", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_wrestle_tv_shows",
                    'url': item.get("wrestle", ""),
                    'folder': True,
                    'imdb': "0",
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
            elif "season|" in item.get("wrestle", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_wrestle_season",
                    'url': item.get("wrestle", ""),
                    'folder': True,
                    'imdb': "0",
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
            elif "other|" in item.get("wrestle", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_wrestle_other",
                    'url': item.get("wrestle", ""),
                    'folder': True,
                    'imdb': "0",
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

@route(mode='open_otb_wrestle_list')
def open_list():
    pins = "PLuginotbwrestle"
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:
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
        xml = ""
        at = Airtable('appiyO9gNgarlyPvv', 'otb_wrestle', api_key='keyikW1exArRfNAWj')
        match = at.get_all(maxRecords=1200, view='Grid view') 
        for field in match: 
            try:
                res = field['fields']   
                name = res['Name']
                name = remove_non_ascii(name)
                link1 = res['link1']
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                summary = res ['summary']
                summary = remove_non_ascii(summary) 
                print link1                                                           
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
                       "<wrestle>open|%s</wrestle>"\
                       "</item>" % (name,thumbnail,fanart,summary,link1)
            except:
                pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

@route(mode='open_otb_wrestle_items',args=["url"])
def open_items(url):
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
    xml = ""
    title = url.split("|")[-2]
    key = url.split("|")[-1]
    at = Airtable(key, title, api_key='keyikW1exArRfNAWj')
    match = at.get_all(maxRecords=1200, view='Grid view')
    if title == "Classic":
        pins = "PLuginotbwrestle"+title
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:            
            for field in match:
                try:
                    res = field['fields']   
                    thumbnail = res['thumbnail']
                    fanart = res['fanart']
                    summary = res['summary']
                    summary = remove_non_ascii(summary)                   
                    name = res['Name']
                    name = remove_non_ascii(name)
                    link1 = res['link1']
                    link2 = res['link2']
                    link3 = res['link3']
                    link4 = res['link4']                                                 
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
                           "<link>"\
                           "<sublink>%s</sublink>"\
                           "<sublink>%s</sublink>"\
                           "<sublink>%s</sublink>"\
                           "<sublink>%s</sublink>"\
                           "</link>"\
                           "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4) 
                except:
                    pass                                                                     
                             
    elif title == "PPV":
        pins = "PLuginotbwrestle"+title
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            for field in match:
                try:
                    res = field['fields']   
                    thumbnail = res['thumbnail']
                    fanart = res['fanart']
                    summary = res['summary']
                    summary = remove_non_ascii(summary)                   
                    name = res['name']
                    name = remove_non_ascii(name)
                    link1 = res['link1']
                    link2 = res['link2']
                    link3 = res['link3']
                    link4 = res['link4']                                                
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
                           "<link>"\
                           "<sublink>%s</sublink>"\
                           "<sublink>%s</sublink>"\
                           "<sublink>%s</sublink>"\
                           "<sublink>%s</sublink>"\
                           "</link>"\
                           "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4)
                except:
                    pass                                                                     
      
    elif title == "Wrestling Specials":
        pins = "PLuginotbwrestle"+title
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            for field in match:
                try:
                    res = field['fields']   
                    thumbnail = res['thumbnail']
                    fanart = res['fanart']
                    summary = res['summary']
                    summary = remove_non_ascii(summary)                   
                    name = res['name']
                    name = remove_non_ascii(name)
                    link1 = res['link1']
                    link2 = res['link2']
                    link3 = res['link3']
                    link4 = res['link4']                                                
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
                           "<link>"\
                           "<sublink>%s</sublink>"\
                           "<sublink>%s</sublink>"\
                           "<sublink>%s</sublink>"\
                           "<sublink>%s</sublink>"\
                           "</link>"\
                           "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4)
                except:
                    pass                                                                     

    elif title == "Wrestling Shows":
        pins = "PLuginotbwrestle"+title
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            for field in match:
                try:
                    res = field['fields']   
                    thumbnail = res['thumbnail']
                    fanart = res['fanart']
                    summary = res['summary']
                    summary = remove_non_ascii(summary)                   
                    name = res['name']
                    name = remove_non_ascii(name)
                    link1 = res['link1']                                                 
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
                           "<link>"\
                           "<wrestle>shows|%s</wrestle>"\
                           "</link>"\
                           "</item>" % (name,thumbnail,fanart,summary,link1)
                except:
                    pass                                                                     

    elif title == "Wrestling Federations":
        pins = "PLuginotbwrestle"+title
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            for field in match:
                try:
                    res = field['fields']   
                    thumbnail = res['thumbnail']
                    fanart = res['fanart']
                    summary = res['summary']
                    summary = remove_non_ascii(summary)                   
                    name = res['Name']
                    name = remove_non_ascii(name)
                    link1 = res['link1']                                                 
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
                           "<link>"\
                           "<wrestle>other|%s</wrestle>"\
                           "</link>"\
                           "</item>" % (name,thumbnail,fanart,summary,link1)
                except:
                    pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='open_wrestle_shows',args=["url"])
def open_items(url):
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
    title = url.split("|")[-2]
    key = url.split("|")[-1]
    pins = "PLuginotbwrestle" + title
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:     
        xml = ""
        result = title + "_season"
        at = Airtable(key, title, api_key='keyikW1exArRfNAWj')
        match = at.search('category', result,view='Grid view')
        for field in match:
            try:
                res = field['fields']   
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                summary = res['summary']
                summary = remove_non_ascii(summary)                   
                name = res['name']
                name = remove_non_ascii(name)
                link1 = res['link1']
                url2 = title+"|"+key+"|"+name                                                 
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
                       "<link>"\
                       "<wrestle>season|%s</wrestle>"\
                       "</link>"\
                       "</item>" % (name,thumbnail,fanart,summary,url2)
            except:
                pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins) 

@route(mode='open_wrestle_season',args=["url"])
def open_items(url):
    title = url.split("|")[-3]
    key = url.split("|")[-2]
    sea_name = url.split("|")[-1]
    pins = "PLuginotbwrestle" + title + sea_name
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:     
        xml = ""
        result = title+"_"+sea_name
        at = Airtable(key, title, api_key='keyikW1exArRfNAWj')
        match = at.search('category', result,view='Grid view')
        for field in match:
            try:
                res = field['fields']
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                summary = res['summary']
                summary = remove_non_ascii(summary)                   
                name = res['name']
                name = remove_non_ascii(name)
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']
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
                       "<link>"\
                       "<sublink>%s</sublink>"\
                       "<sublink>%s</sublink>"\
                       "<sublink>%s</sublink>"\
                       "<sublink>%s</sublink>"\
                       "</link>"\
                       "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4)                                                               
            except:
                pass                  
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)    

@route(mode='open_wrestle_other',args=["url"])
def open_items(url):
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
    xml = ""
    title = url.split("|")[-2]
    key = url.split("|")[-1]
    at = Airtable(key, title, api_key='keyikW1exArRfNAWj')
    match = at.get_all(maxRecords=1200, view='Grid view')
    pins = "PLuginotbwrestle"+title+key
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:            
        for field in match:
            try:
                res = field['fields']   
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                summary = res['summary']
                summary = remove_non_ascii(summary)                   
                name = res['name']
                name = remove_non_ascii(name)
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']                                                 
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
                       "<link>"\
                       "<sublink>%s</sublink>"\
                       "<sublink>%s</sublink>"\
                       "<sublink>%s</sublink>"\
                       "<sublink>%s</sublink>"\
                       "</link>"\
                       "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4)    
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
