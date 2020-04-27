# -*- coding: utf-8 -*-
"""
    OTB_DIY
    Copyright (C) 2018,
    Version 1.0.0
    Team OTB
    Jen 1

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

    Returns the OTB DIY list-

    <dir>
    <title>OTB DIY</title>
    <otb_diy>all</otb_diy>
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

"""
----------------------------------------------------------
"""
table_id = "app8g4AI6nWZoQpnr"
table_name = "OTB DIY"
workspace_api_key = "keyikW1exArRfNAWj"
"""
----------------------------------------------------------
"""

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
tid = bdc('YXBwWDNHQUdxMFBKSGNNSVk=')
tnm = bdc('b3RiX2RpeV9pZHM=')
atk = bdc('a2V5T0hheHNUR3pIVTlFRWg=')

class OTB_DIY(Plugin):
    name = "otb2_dg"

    def process_item(self, item_xml):
        if "<otb_diy>" in item_xml:
            item = JenItem(item_xml)
            if "all" in item.get("otb_diy", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_diy_shows",
                    'url': item.get("otb_diy", ""),
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
            elif "show|" in item.get("otb_diy", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_diy_selected_show",
                    'url': item.get("otb_diy", ""),
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

@route(mode='open_otb_diy_shows')
def open_otb_diy_shows():
    pins = "PLuginotbdiy"
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
        at = Airtable(table_id, table_name, api_key=workspace_api_key)
        match = at.get_all(maxRecords=1200, sort=['name'])
        for field in match:
            try:
                res = field['fields']
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                summary = res['summary']
                if not summary:
                    summary = ""
                else:
                    summary = remove_non_ascii(summary)                        
                name = res['name']
                name = remove_non_ascii(name)                                               
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
                       "<otb_diy>show|%s</otb_diy>"\
                       "</item>" % (name,thumbnail,fanart,summary,res['link1'])
            except:
                pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

@route(mode='open_otb_diy_selected_show',args=["url"])
def open_selected_show(url):
    pins = "PLuginotbdiy"+url
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
        title = url.split("|")[-2]
        key = url.split("|")[-1]
        result = title
        at = Airtable(key, title, api_key=workspace_api_key)
        match = at.get_all(maxRecords=1200, sort=['name'])
        for field in match:
            try:
                res = field['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                print "############ name ###########"+name
                summary = res['summary']
                summary = remove_non_ascii(summary)
                fanart = res['fanart']
                thumbnail = res['thumbnail']
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']                                                
                if link2 == "-":
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
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1)
                elif link3 == "-":
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
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1,link2) 
                elif link4 == "-":
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
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3)
                
                else:
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
        
