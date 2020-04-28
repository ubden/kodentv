# -*- coding: utf-8 -*-
"""
    OTB Radio.py
    Copyright (C) 2018, OTB
    Version 1.1.0
    Jen 2x plugin

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

    Search the Radio List

    <dir>
    <title>Search OTB Radio</title>
    <otb_radio>search</otb_radio>
    </dir>

    Returns the Radio list (Recommend you use the Country tags below, the tables
    are huge)

    <dir>
    <title>OTB Radio</title>
    <otb_radio>all</otb_radio>
    </dir>

    

    ---------------------

    Possible Genre's are:
    UK
    USA

    -----------------------

    Country tags (Recommended)

    <dir>
    <title>OTB UK Radio 1</title>
    <otb_radio>genre/UK1</otb_radio>
    </dir>

    <dir>
    <title>OTB UK Radio 2</title>
    <otb_radio>genre/UK2</otb_radio>
    </dir>

    <dir>
    <title>OTB USA Radio 1</title>
    <otb_radio>genre/USA1</otb_radio>
    </dir>

    <dir>
    <title>OTB USA Radio 2</title>
    <otb_radio>genre/USA2</otb_radio>
    </dir>

    <dir>
    <title>OTB USA Radio 3</title>
    <otb_radio>genre/USA3</otb_radio>
    </dir>
    
    <dir>
    <title>OTB USA Radio 4</title>
    <otb_radio>genre/USA4</otb_radio>
    </dir>

    <dir>
    <title>OTB USA Radio 5</title>
    <otb_radio>genre/USA5</otb_radio>
    </dir>    
    
    <dir>
    <title>OTB Radio Search</title>
    <otb_radio>search</otb_radio>>
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
tid = bdc('YXBwTzZqamU0cHlzOEJ6WFc=')
tnm = bdc('b3RiXyxyYWRpb19pZHM=')
atk = bdc('a2V5T0hheHNUR3pIVTlFRWg=')


class OTB_Radio_List(Plugin):
    name = "otb_radio_list"

    def process_item(self, item_xml):
        if "<otb_radio>" in item_xml:
            item = JenItem(item_xml)
            if "all" in item.get("otb_radio", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_radio",
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
            elif "genre" in item.get("otb_radio", ""):    
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_radio2",
                    'url': item.get("otb_radio", ""),
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
            elif "search" in item.get("otb_radio", ""):    
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_radio_search",
                    'url': item.get("otb_radio", ""),
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
    print name
    print fanart
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

@route(mode='open_otb_radio')
def open_movies():
    xml = ""
    pins = "PLuginotbradioall"
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
        at = Airtable('appEQMKxvYhvxB6fY', 'Radio Stations', api_key='keyikW1exArRfNAWj')
        match = at.get_all(maxRecords=1200, sort=['name'])
        for field in match:
            try:
                res = field['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                summary = clean_summary(summary)
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
        at2 = Airtable('appjrEMH0kEoM8GeQ', 'Radio Stations 2', api_key='keyikW1exArRfNAWj')
        match2 = at2.get_all(maxRecords=1200, sort=['name'])      
        for field2 in match2:
            try:
                res = field2['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                summary = clean_summary(summary)
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
        at3 = Airtable('appgveAIgb4kfsMoe', 'Radio Stations 3', api_key='keyikW1exArRfNAWj')
        match3 = at3.get_all(maxRecords=1200, sort=['name'])      
        for field3 in match3:
            try:
                res = field3['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                summary = clean_summary(summary)
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
        at4 = Airtable('appWZAAh8GXRyo6SN', 'Radio Stations 4', api_key='keyikW1exArRfNAWj')
        match4 = at4.get_all(maxRecords=1200, sort=['name'])      
        for field4 in match4:
            try:
                res = field4['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                summary = clean_summary(summary)
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
        at5 = Airtable('appgqVj0DBZjvGtrt', 'Radio Stations 5', api_key='keyikW1exArRfNAWj')
        match5 = at5.get_all(maxRecords=1200, sort=['name'])      
        for field5 in match5:
            try:
                res = field5['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                summary = clean_summary(summary)
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
        at6 = Airtable('appWSAjWWuFRZ2cZb', 'Radio Stations 6', api_key='keyikW1exArRfNAWj')
        match6 = at6.get_all(maxRecords=1200, sort=['name'])      
        for field6 in match6:
            try:
                res = field6['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                summary = clean_summary(summary)
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
        at7 = Airtable('app41uxtTRva32pvc', 'Radio Stations 7', api_key='keyikW1exArRfNAWj')
        match7 = at7.get_all(maxRecords=1200, sort=['name'])      
        for field7 in match7:
            try:
                res = field7['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                summary = clean_summary(summary)
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

@route(mode='open_otb_radio2',args=["url"])
def open_action_movies(url):
    xml = ""
    genre = url.split("/")[-1]                                            
    pins = "PLuginotbradio"+str(genre)
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
        if genre == "UK1":     
            at = Airtable('appEQMKxvYhvxB6fY', 'Radio Stations', api_key='keyikW1exArRfNAWj')
            try:
                match = at.search('type', genre, sort=['name'])
                for field in match:
                    res = field['fields']   
                    name = res['name']
                    name = remove_non_ascii(name)
                    summary = res['summary']
                    summary = remove_non_ascii(summary)
                    summary = clean_summary(summary)
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
        elif genre == "UK2":       
            at2 = Airtable('appjrEMH0kEoM8GeQ', 'Radio Stations 2', api_key='keyikW1exArRfNAWj')
            try:
                match2 = at2.search('type', genre, sort=['name'])
                for field2 in match2:
                    res = field2['fields']   
                    name = res['name']
                    name = remove_non_ascii(name)
                    summary = res['summary']
                    summary = remove_non_ascii(summary)
                    summary = clean_summary(summary)
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
        elif genre == "USA1":        
            at3 = Airtable('appgveAIgb4kfsMoe', 'Radio Stations 3', api_key='keyikW1exArRfNAWj')
            match3 = at3.search('type', genre, sort=['name'])      
            for field3 in match3:
                try:
                    res = field3['fields']   
                    name = res['name']
                    name = remove_non_ascii(name)
                    summary = res['summary']
                    summary = remove_non_ascii(summary)
                    summary = clean_summary(summary)
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
        elif genre == "USA2":            
            at4 = Airtable('appWZAAh8GXRyo6SN', 'Radio Stations 4', api_key='keyikW1exArRfNAWj')
            match4 = at4.search('type', genre, sort=['name'])     
            for field4 in match4:
                try:
                    res = field4['fields']   
                    name = res['name']
                    name = remove_non_ascii(name)
                    summary = res['summary']
                    summary = remove_non_ascii(summary)
                    summary = clean_summary(summary)
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
        elif genre == "USA3":            
            at5 = Airtable('appgqVj0DBZjvGtrt', 'Radio Stations 5', api_key='keyikW1exArRfNAWj')
            match5 = at5.search('type', genre, sort=['name'])     
            for field5 in match5:
                try:
                    res = field5['fields']   
                    name = res['name']
                    name = remove_non_ascii(name)
                    summary = res['summary']
                    summary = remove_non_ascii(summary)
                    summary = clean_summary(summary)
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
        elif genre == "USA4":            
            at6 = Airtable('appWSAjWWuFRZ2cZb', 'Radio Stations 6', api_key='keyikW1exArRfNAWj')
            match6 = at6.search('type', genre, sort=['name'])     
            for field6 in match6:
                try:
                    res = field6['fields']   
                    name = res['name']
                    name = remove_non_ascii(name)
                    summary = res['summary']
                    summary = remove_non_ascii(summary)
                    summary = clean_summary(summary)
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
        elif genre == "USA5":            
            at7 = Airtable('app41uxtTRva32pvc', 'Radio Stations 7', api_key='keyikW1exArRfNAWj')
            match7 = at7.search('type', genre, sort=['name'])     
            for field7 in match7:
                try:
                    res = field7['fields']   
                    name = res['name']
                    name = remove_non_ascii(name)
                    summary = res['summary']
                    summary = remove_non_ascii(summary)
                    summary = clean_summary(summary)
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


@route(mode='open_otb_radio_search')
def open_bml_search():
    xml = ""
    pins = ""
    show = koding.Keyboard(heading='Station Name or Number')
    movie_list = []
    at = Airtable('appEQMKxvYhvxB6fY', 'Radio Stations', api_key='keyikW1exArRfNAWj')
    match = at.get_all(maxRecords=1200, sort=['name'])
    for field in match:
        res = field['fields']        
        name = res['name']
        movie_list.append(name)
    at2 = Airtable('appjrEMH0kEoM8GeQ', 'Radio Stations 2', api_key='keyikW1exArRfNAWj')
    match2 = at2.get_all(maxRecords=1200, sort=['name'])  
    for field2 in match2:       
        res2 = field2['fields']        
        name2 = res2['name']
        movie_list.append(name2)
    at3 = Airtable('appgveAIgb4kfsMoe', 'Radio Stations 3', api_key='keyikW1exArRfNAWj')
    match3 = at3.get_all(maxRecords=1200, sort=['name'])  
    for field3 in match3:       
        res3 = field3['fields']        
        name3 = res3['name']
        movie_list.append(name3)
    at4 = Airtable('appWZAAh8GXRyo6SN', 'Radio Stations 4', api_key='keyikW1exArRfNAWj')
    match4 = at4.get_all(maxRecords=1200, sort=['name'])  
    for field4 in match4:       
        res4 = field4['fields']        
        name4 = res4['name']
        movie_list.append(name4)
    at5 = Airtable('appgqVj0DBZjvGtrt', 'Radio Stations 5', api_key='keyikW1exArRfNAWj')
    match5 = at5.get_all(maxRecords=1200, sort=['name'])  
    for field5 in match5:       
        res5 = field5['fields']        
        name5 = res5['name']
        movie_list.append(name5)
    at6 = Airtable('appWSAjWWuFRZ2cZb', 'Radio Stations 6', api_key='keyikW1exArRfNAWj')
    match6 = at6.get_all(maxRecords=1200, sort=['name'])  
    for field6 in match6:       
        res6 = field6['fields']        
        name6 = res6['name']
        movie_list.append(name6)
    at7 = Airtable('app41uxtTRva32pvc', 'Radio Stations 7', api_key='keyikW1exArRfNAWj')
    match7 = at7.get_all(maxRecords=1200, sort=['name'])  
    for field7 in match7:       
        res7 = field7['fields']        
        name7 = res7['name']
        movie_list.append(name7)
    search_result = koding.Fuzzy_Search(show, movie_list)
    if not search_result:
        xbmc.log("--------no results--------",level=xbmc.LOGNOTICE)
        xml += "<item>"\
            "<title>[COLOR=orange][B]Station was not found[/B][/COLOR]</title>"\
            "</item>"
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)    
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
                summary = clean_summary(summary)
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
                summary = clean_summary(summary)
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
                summary = clean_summary(summary)
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
                summary = clean_summary(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
        except:
            pass
        try:
            match2 = at5.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                summary = clean_summary(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
        except:
            pass
        try:
            match2 = at6.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                summary = clean_summary(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
        except:
            pass
        try:
            match2 = at7.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                summary = clean_summary(summary)
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
        
def clean_summary(title):
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    #title = re.sub('\\\|/|\(|\)|\[|\]|\{|\}|-|:|;|\*|\?|"|\'|<|>|\_|\.|\?', ' ', title)
    return title
