import xbmc,xbmcaddon,xbmcgui,requests
from resources.modules import control,tools

dir= xbmc.translatePath('special://home/addons/plugin.video.MediaHubIPTV/resources/modules/')

username     = control.setting('Username')
password     = control.setting('Password')
def tinyurlGet(m3u,epg):
		request  = 'https://tinyurl.com/create.php?source=indexpage&url='+m3u+'&submit=Make+TinyURL%21&alias='
		request2 = 'https://tinyurl.com/create.php?source=indexpage&url='+epg+'&submit=Make+TinyURL%21&alias='
		m3u = tools.OPEN_URL(request)
		epg = tools.OPEN_URL(request2)
		shortm3u = tools.regex_from_to(m3u,'<div class="indent"><b>','</b>')
		shortepg = tools.regex_from_to(epg,'<div class="indent"><b>','</b>')
		return shortm3u,shortepg
		
def showlinks():
	xbmc.executebuiltin('ActivateWindow(busydialog)')
	M3U,EPG = Get()
	
	text    = readfile(dir,'shortlinkstext.txt')
	info    = text%(M3U,EPG)
	xbmc.executebuiltin('Dialog.Close(busydialog)')
	
	popupd(info)
	
def readfile(url,file):
            import os
            file = open(os.path.join(url, file))
            data = file.read()
            file.close()
            return data
	
def popupd(announce):
	import time,xbmcgui
	class TextBox():
		WINDOW=10147
		CONTROL_LABEL=1
		CONTROL_TEXTBOX=5
		def __init__(self,*args,**kwargs):
			xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
			self.win=xbmcgui.Window(self.WINDOW) # get window
			xbmc.sleep(500) # give window time to initialize
			self.setControls()
		def setControls(self):
			self.win.getControl(self.CONTROL_LABEL).setLabel('[COLOR ghostwhite][B]Live[/COLOR][COLOR red] Hub[/COLOR][/B]') # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)