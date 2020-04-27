
import os,xbmc
logfile    = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.streamhub', 'log.txt'))


def log(text):
	file = open(logfile,"w+")
	file.write(str(text))

def check4update():
	import re,time,xbmc,xbmcgui
	from resources.lib.modules import client

	addonxml = xbmc.translatePath('special://home/addons/script.module.streamhub/addon.xml')
	file     = open(addonxml)
	data     = file.read()
	file.close()

	c_version = re.compile('" version="(.+?)"').findall(data)[0]
	c_version2= (c_version).replace('.','')
	
	log(c_version2)

	html = client.request('https://raw.githubusercontent.com/sClarkeIsBack/StreamHub/master/Repo_Files/addons.xml')

	o_version = re.compile('script.module.streamhub.+?version="(.+?)"').findall(html)[0]
	o_version2= (o_version).replace('.','')
	log(o_version2)
	if c_version2 < o_version2:
		update = 'https://github.com/sClarkeIsBack/StreamHub/raw/master/Repo_Files/Zips/script.module.streamhub/script.module.streamhub-%s.zip'%o_version
		install(o_version,update)
		xbmc.executebuiltin("UpdateAddonRepos")
		xbmc.executebuiltin("UpdateLocalAddons")
		time.sleep(5)
		xbmcgui.Dialog().notification('[COLOR red]StreamHub[/COLOR]','Updated Successfully')
	
	
def install(vers,url):
    import xbmc,xbmcgui,os,re,time
    from resources.lib.modules import downloader2
    addon_folder = xbmc.translatePath('special://home/addons/script.module.streamhub/')
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR red]StreamHub[/COLOR]","Installing Dependency Update v[COLOR red]%s[/COLOR]"%vers,'', 'Please Wait')
    lib=os.path.join(path, 'content.zip')
    try:
       os.remove(lib)
    except:
       pass
	   
    import shutil

    shutil.rmtree(addon_folder)
    try:
        downloader2.download(url, lib, dp)
        addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
        time.sleep(3)
    except:
        xbmcgui.Dialog().ok('[COLOR red]StreamHub[/COLOR]','Oops..Something Went Wrong Downloading The Update...Try Again')
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR red]StreamHub[/COLOR]","Installing Dependency Update Version [COLOR red]%s[/COLOR]"%vers,'', 'Please Wait')
    dp.update(0,"", "Installing... Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    try:
        unzip(lib,addonfolder,dp)
    except:
        xbmcgui.Dialog().ok('[COLOR red]StreamHub[/COLOR]','Oops..Something Went Wrong Installing The Update...Try Again')
	
	
def unzip(_in, _out, dp):
	import zipfile,sys
	__in = zipfile.ZipFile(_in,  'r')
	
	nofiles = float(len(__in.infolist()))
	count   = 0
	
	try:
		for item in __in.infolist():
			count += 1
			update = (count / nofiles) * 100
			
			if dp.iscanceled():
				dialog = xbmcgui.Dialog()
				dialog.ok('[COLOR red]StreamHub[/COLOR]', 'Process was cancelled.')
				
				sys.exit()
				dp.close()
			
			try:
				dp.update(int(update))
				__in.extract(item, _out)
			
			except Exception, e:
				print str(e)

	except Exception, e:
		print str(e)
		return False
		
	return True