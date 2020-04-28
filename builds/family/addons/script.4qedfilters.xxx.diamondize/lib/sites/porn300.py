# -*- coding: utf-8 -*-
import urllib2, urllib, xbmcgui, xbmcplugin, xbmcaddon, xbmc, re, sys, os,requests
from lib import clean_name
from lib import process
ADDON_PATH = xbmc.translatePath('special://home/addons/script.4qedfilters.xxx.diamondize')
ICON = ADDON_PATH + '/icon.png'
FANART = 'special://home/addons/script.4qedfilters.xxx.diamondize/fanart.jpg'
Dialog = xbmcgui.Dialog()
List = []

#1007
def porn_300_menu():
    process.Menu('[B][COLOR lime]. [/COLOR][/B] [COLOR ghostwhite]Top Rated[/COLOR]','https://www.porn300.com/top-rated/',1009,'https://www.porn300.com/android-icon-192x192.png',FANART,'[COLORpalegreen][B]. Porn 300[/B][CR][COLORwhite]Top Rated videos from Porn 300[/COLOR]','')
    process.Menu('[B][COLOR lime]. [/COLOR][/B] [COLOR ghostwhite]Most Viewed[/COLOR]','https://www.porn300.com/most-viewed/',1009,'https://www.porn300.com/android-icon-192x192.png',FANART,'[COLORpalegreen][B]. Porn 300[/B][CR][COLORwhite]Most Viewed videos from Porn 300[/COLOR]','')
    process.Menu('[B][COLOR lime]. [/COLOR][/B] [COLOR ghostwhite]Starz[/COLOR]','https://www.porn300.com/pornstars/',1012,'https://www.porn300.com/android-icon-192x192.png',FANART,'[COLORpalegreen][B]. Porn 300[/B][CR][COLORwhite]Starz from Porn 300[/COLOR]','')
    process.Menu('[B][COLOR lime]. [/COLOR][/B] [COLOR ghostwhite]VR Vidz[/COLOR]','https://www.porn300.com/channel/vr-bangers/',1009,'https://www.porn300.com/android-icon-192x192.png',FANART,'[COLORpalegreen][B]. Porn 300[/B][CR][COLORwhite]VR Vidz from Porn 300[/COLOR]','')
    process.Menu('[B][COLOR lime]. [/COLOR][/B] [COLOR ghostwhite]Categories[/COLOR]','https://www.porn300.com',1010,'https://www.porn300.com/android-icon-192x192.png',FANART,'[COLORpalegreen][B]. Porn 300[/B][CR][COLORwhite]Categories from Porn 300[/COLOR]','')
    process.Menu('[B][COLOR lime]. [/COLOR][/B] [COLOR ghostwhite]Channels[/COLOR]','https://www.porn300.com/channels/',1013,'https://www.porn300.com/android-icon-192x192.png',FANART,'[COLORpalegreen][B]. Porn 300[/B][CR][COLORwhite]Channels from Porn 300[/COLOR]','')
    process.Menu('[B][COLOR lime]. [/COLOR][/B] [COLOR ghostwhite]Search[/COLOR]','',1011,'https://www.porn300.com/android-icon-192x192.png',FANART,'[COLORpalegreen][B]. Porn 300[/B][CR][COLORwhite]Search Porn 300[/COLOR]','')



#1008
def porn300_playlinks(url):
    html = process.OPEN_URL(url)
    match = re.compile('<div id="video-link".+?data-video="(.+?)"',re.DOTALL).findall(html)
    for link in match:
        xbmc.Player().play(link)

#1009
def porn300_vids(url):
    html = process.OPEN_URL(url)
    match = re.compile('<li class="grid__item.+?href="(.+?)".+?src="(.+?)" alt="(.+?)".+?</ul>.+?</li>',re.DOTALL).findall(html)
    for url,img,name in match:
        name = name.replace('&#039;','\'')
        url = 'https://www.porn300.com'+url
        process.PLAY(name,url,1008,img,FANART,'','')
    next_page= re.compile('<li class="pagination_item" itemprop="url"><a class="btn btn-primary--light btn-pagination" itemprop="name" href="(.+?)" title="Next">',re.DOTALL).findall(html)
    for page in next_page:
        page = 'https://www.porn300.com'+page
        process.Menu('[COLOR palegreen]Next Page[/COLOR]',page,1009,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')

#1010
def porn300_cats(url):
    html = process.OPEN_URL(url)
    match = re.compile('class="grid__item grid__item--.+?href="(.+?)".+?image" src=(.+?)alt="(.+?)".+?</ul>.+?</li>',re.DOTALL).findall(html)
    for url,img,name in match:
        url = 'https://www.porn300.com'+url
        process.Menu(name,url,1009,img,FANART,'','')



    
#1011
def porn300_search():
    Dialog = xbmcgui.Dialog()
    Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
    Search_name = Search_title.lower()
    url = 'https://www.porn300.com/search/?q='+Search_name.replace(' ','+')
    porn300_vids(url)

#1012
def porn300_starz(url):
    html = process.OPEN_URL(url)
    match = re.compile('class="grid__item grid__item--pornstar-thumb".+?href="(.+?)".+?image" src=(.+?)alt="(.+?)".+?</ul>.+?</li>',re.DOTALL).findall(html)
    for url,img,name in match:
        # vid_count = vid_count.strip()
        url = 'https://www.porn300.com'+url
        process.Menu(name,url,1009,img,FANART,'','')    

#1013
def porn300_channels(url):
    html = process.OPEN_URL(url)
    match = re.compile('class="grid__item grid__item--producer".+?href="(.+?)".+?image" src="(.+?)" alt="(.+?)".+?</a>.+?</li>',re.DOTALL).findall(html)
    for url,img,name in match:
        url = 'https://www.porn300.com'+url
        process.Menu(name,url,1009,img,FANART,'','')
    next_page= re.compile('class="paginador">.+?class="selected" href=".+?href="(.+?)".+?</li>',re.DOTALL).findall(html)
    for page in next_page:
        page = 'https://www.porn300.com'+page
        process.Menu('[COLOR palegreen]Next Page[/COLOR]',page,1013,'https://raw.githubusercontent.com/CellarDoorTV/CDTV_DOMINUS_ICONS/master/artwork/mainart/module_icon/next.png',FANART,'','') 