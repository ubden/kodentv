import os,xbmc,xbmcgui,downloader,user

def install(name,url):

	if xbmc.getCondVisibility('system.platform.android'):
		path = xbmc.translatePath(os.path.join('/storage/emulated/0/Download',''))
		dp = xbmcgui.DialogProgress()
		dp.create(user.name,"","",'Downloading:' + name)
		lib=os.path.join(path, 'app.apk')
		downloader.download(url, lib, dp)
		xbmcgui.Dialog().ok(user.name, "[COLOR white]Launching the installer[/COLOR]" , "[COLOR white]You will now be asked to install[/COLOR] [B][COLOR lime]%s[/COLOR][/B]"%name)
		xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:' + lib + '")' )
	else:
		xbmcgui.Dialog().ok("[COLOR white]Non Android Device[/COLOR]" , " ","[COLOR white]This App Installer is only compatible with Android Devices[/COLOR]"," ")