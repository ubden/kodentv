"""
    m3u.py --- Jen Plugin for accessing m3u data
    Copyright (C) 2018, Mister X, Modified by Tony H
        Some functions taken from Livestream pro
        Requires f4mTester with some m3u8's
    version 1.0.3

    7-12-19 - Added Livestream pro functions
    7-8-19 - Added cache function and modified regex - TH
    6-9-19 - Modified regex and added User Agent - TH

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


    Usage Examples:
    <dir>
    <title>M3U NAME</title>
    <thumbnail></thumbnail>
    <m3u>M3U LINK</m3u>
    <fanart></fanart>
    <info> </info>
    </dir>
"""

import urllib2, urllib
import requests,re,os,xbmc,xbmcaddon
import base64,pickle,koding,time,sqlite3
from koding import route
from ..plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list, display_data, clean_url
from resources.lib.external.airtable.airtable import Airtable
from unidecode import unidecode
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP

CACHE_TIME = 86400  # change to wanted cache time in seconds

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
home_folder = xbmc.translatePath('special://home/')
user_data_folder = os.path.join(home_folder, 'userdata')
addon_data_folder = os.path.join(user_data_folder, 'addon_data')
database_path = os.path.join(addon_data_folder, addon_id)
database_loc = os.path.join(database_path, 'database.db')
tsdownloader=False
hlsretry=False
#debug = addon_id.getSetting('debug')
UserAgent = "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"

class M3U(Plugin):
    name = "m3u"

    def process_item(self, item_xml):
        if "<m3u>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "m3u",
                'url': item.get("m3u", ""),
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
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item



@route(mode='m3u', args=["url"])
def m3u(url):
    xml = ""
    clsin = url.split("/")[-1]
    pins = "PLuginm3u" + clsin
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:
        if not xml:
            xml = ""
            if '.m3u' in url:
                listhtml = getHtml(url)
                match = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(listhtml)
                for other,channel_name,stream_url in match:
                    if 'tvg-logo' in other:
                        thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
                        if thumbnail:
                            if thumbnail.startswith('http'):
                                thumbnail = thumbnail
                    else:
                        thumbnail = ''
                    if 'type' in other:
                        mode_type = re_me(other,'type=[\'"](.*?)[\'"]')
                        if mode_type == 'yt-dl':
                            stream_url = stream_url +"&mode=18"
                        elif mode_type == 'regex':
                            url = stream_url.split('&regexs=')
                            regexs = parse_regex(getSoup('',data=url[1]))
                            xml += "<item>"\
                                   "<title>%s</title>"\
                                   "<link>%s</link>"\
                                   "<thumbnail></thumbnail>"\
                                   "</item>" % (channel_name, url[0])
                            addLink(url[0], channel_name,thumbnail,'','','','','',None,regexs,total)
                            continue
                        elif mode_type == 'ftv':
                            stream_url = 'plugin://plugin.video.F.T.V/?name='+urllib.quote(channel_name) +'&url=' +stream_url +'&mode=125&ch_fanart=na'
                    elif tsdownloader and '.ts' in stream_url:
                        stream_url = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(stream_url)+'&amp;streamtype=TSDOWNLOADER&name='+urllib.quote(channel_name)
                    elif hlsretry and '.m3u8' in stream_url:
                        stream_url = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(stream_url)+'&amp;streamtype=HLSRETRY&name='+urllib.quote(channel_name)
                    else:
                        stream_url = stream_url + UserAgent                             
                    xml += "<item>"\
                           "<title>%s</title>"\
                           "<link>%s</link>"\
                           "<thumbnail>%s</thumbnail>"\
                           "</item>" % (channel_name, stream_url, thumbnail)

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


def getHtml(url, referer=None, hdr=None, data=None):
    """GRAB HTML FROM THE LINK"""
    USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }
    if not hdr:
        req = urllib2.Request(url, data, headers)
    else:
        req = urllib2.Request(url, data, hdr)
    if referer:
        req.add_header('Referer', referer)
    response = urllib2.urlopen(req, timeout=60)
    data = response.read()
    response.close()
    return data

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

def parse_regex(reg_item):
                try:
                    regexs = {}
                    for i in reg_item:
                        regexs[i('name')[0].string] = {}
                        regexs[i('name')[0].string]['name']=i('name')[0].string
                        #regexs[i('name')[0].string]['expres'] = i('expres')[0].string
                        try:
                            regexs[i('name')[0].string]['expres'] = i('expres')[0].string
                            if not regexs[i('name')[0].string]['expres']:
                                regexs[i('name')[0].string]['expres']=''
                        except:
                            addon_log("Regex: -- No Referer --")
                        regexs[i('name')[0].string]['page'] = i('page')[0].string
                        try:
                            regexs[i('name')[0].string]['referer'] = i('referer')[0].string
                        except:
                            addon_log("Regex: -- No Referer --")
                        try:
                            regexs[i('name')[0].string]['connection'] = i('connection')[0].string
                        except:
                            addon_log("Regex: -- No connection --")

                        try:
                            regexs[i('name')[0].string]['notplayable'] = i('notplayable')[0].string
                        except:
                            addon_log("Regex: -- No notplayable --")

                        try:
                            regexs[i('name')[0].string]['noredirect'] = i('noredirect')[0].string
                        except:
                            addon_log("Regex: -- No noredirect --")
                        try:
                            regexs[i('name')[0].string]['origin'] = i('origin')[0].string
                        except:
                            addon_log("Regex: -- No origin --")
                        try:
                            regexs[i('name')[0].string]['accept'] = i('accept')[0].string
                        except:
                            addon_log("Regex: -- No accept --")
                        try:
                            regexs[i('name')[0].string]['includeheaders'] = i('includeheaders')[0].string
                        except:
                            addon_log("Regex: -- No includeheaders --")

                            
                        try:
                            regexs[i('name')[0].string]['listrepeat'] = i('listrepeat')[0].string
#                            print 'listrepeat',regexs[i('name')[0].string]['listrepeat'],i('listrepeat')[0].string, i
                        except:
                            addon_log("Regex: -- No listrepeat --")
                    
                            

                        try:
                            regexs[i('name')[0].string]['proxy'] = i('proxy')[0].string
                        except:
                            addon_log("Regex: -- No proxy --")
                            
                        try:
                            regexs[i('name')[0].string]['x-req'] = i('x-req')[0].string
                        except:
                            addon_log("Regex: -- No x-req --")

                        try:
                            regexs[i('name')[0].string]['x-addr'] = i('x-addr')[0].string
                        except:
                            addon_log("Regex: -- No x-addr --")                            
                            
                        try:
                            regexs[i('name')[0].string]['x-forward'] = i('x-forward')[0].string
                        except:
                            addon_log("Regex: -- No x-forward --")

                        try:
                            regexs[i('name')[0].string]['agent'] = i('agent')[0].string
                        except:
                            addon_log("Regex: -- No User Agent --")
                        try:
                            regexs[i('name')[0].string]['post'] = i('post')[0].string
                        except:
                            addon_log("Regex: -- Not a post")
                        try:
                            regexs[i('name')[0].string]['rawpost'] = i('rawpost')[0].string
                        except:
                            addon_log("Regex: -- Not a rawpost")
                        try:
                            regexs[i('name')[0].string]['htmlunescape'] = i('htmlunescape')[0].string
                        except:
                            addon_log("Regex: -- Not a htmlunescape")


                        try:
                            regexs[i('name')[0].string]['readcookieonly'] = i('readcookieonly')[0].string
                        except:
                            addon_log("Regex: -- Not a readCookieOnly")
                        #print i
                        try:
                            regexs[i('name')[0].string]['cookiejar'] = i('cookiejar')[0].string
                            if not regexs[i('name')[0].string]['cookiejar']:
                                regexs[i('name')[0].string]['cookiejar']=''
                        except:
                            addon_log("Regex: -- Not a cookieJar")
                        try:
                            regexs[i('name')[0].string]['setcookie'] = i('setcookie')[0].string
                        except:
                            addon_log("Regex: -- Not a setcookie")
                        try:
                            regexs[i('name')[0].string]['appendcookie'] = i('appendcookie')[0].string
                        except:
                            addon_log("Regex: -- Not a appendcookie")

                        try:
                            regexs[i('name')[0].string]['ignorecache'] = i('ignorecache')[0].string
                        except:
                            addon_log("Regex: -- no ignorecache")
                        #try:
                        #    regexs[i('name')[0].string]['ignorecache'] = i('ignorecache')[0].string
                        #except:
                        #    addon_log("Regex: -- no ignorecache")

                    regexs = urllib.quote(repr(regexs))
                    return regexs
                    #print regexs
                except:
                    regexs = None
                    addon_log('regex Error: '+name.encode('utf-8', 'ignore'))

def addon_log(string):
    #if debug == 'true':
    #    xbmc.log("[%s]: %s" %(AddonName, string))
    xbmc.log("[%s]: %s" %(AddonName, string),level=xbmc.LOGDEBUG)

def re_me(data, re_patten):
    match = ''
    m = re.search(re_patten, data)
    if m != None:
        match = m.group(1)
    else:
        match = ''
    return match

def getSoup(url,data=None):
        global viewmode,tsdownloader, hlsretry
        tsdownloader=False
        hlsretry=False
        if url.startswith('http://') or url.startswith('https://'):
            enckey=False
            if '$$TSDOWNLOADER$$' in url:
                tsdownloader=True
                url=url.replace("$$TSDOWNLOADER$$","")
            if '$$HLSRETRY$$' in url:
                hlsretry=True
                url=url.replace("$$HLSRETRY$$","")
            if '$$LSProEncKey=' in url:
                enckey=url.split('$$LSProEncKey=')[1].split('$$')[0]
                rp='$$LSProEncKey=%s$$'%enckey
                url=url.replace(rp,"")
                
            data =makeRequest(url)
            if enckey:
                    import pyaes
                    enckey=enckey.encode("ascii")
                    print enckey
                    missingbytes=16-len(enckey)
                    enckey=enckey+(chr(0)*(missingbytes))
                    print repr(enckey)
                    data=base64.b64decode(data)
                    decryptor = pyaes.new(enckey , pyaes.MODE_ECB, IV=None)
                    data=decryptor.decrypt(data).split('\0')[0]
                    #print repr(data)
            if re.search("#EXTM3U",data) or 'm3u' in url:
#                print 'found m3u data'
                return data
        elif data == None:
            if not '/'  in url or not '\\' in url:
#                print 'No directory found. Lets make the url to cache dir'
                url = os.path.join(communityfiles,url)
            if xbmcvfs.exists(url):
                if url.startswith("smb://") or url.startswith("nfs://"):
                    copy = xbmcvfs.copy(url, os.path.join(profile, 'temp', 'sorce_temp.txt'))
                    if copy:
                        data = open(os.path.join(profile, 'temp', 'sorce_temp.txt'), "r").read()
                        xbmcvfs.delete(os.path.join(profile, 'temp', 'sorce_temp.txt'))
                    else:
                        addon_log("failed to copy from smb:")
                else:
                    data = open(url, 'r').read()
                    if re.match("#EXTM3U",data)or 'm3u' in url:
#                        print 'found m3u data'
                        return data
            else:
                addon_log("Soup Data not found!")
                return
        if '<SetViewMode>' in data:
            try:
                viewmode=re.findall('<SetViewMode>(.*?)<',data)[0]
                xbmc.executebuiltin("Container.SetViewMode(%s)"%viewmode)
                print 'done setview',viewmode
            except: pass
        return BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)