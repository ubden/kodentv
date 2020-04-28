import xbmc,os,shutil

def check():

	try:
		xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
		version=float(xbmc_version[:4])

		if version >= 17.0 and version <= 17.9:
			
			caches = ["special://cache",
			"special://temp/",
			"/private/var/mobile/Library/Caches/AppleTV/Video/Other",
			"/private/var/mobile/Library/Caches/AppleTV/Video/LocalAndRental"]
			
			for folders in caches:
				if "special" in folders:
					folders = xbmc.translatePath(folders)
				if os.path.exists(folders):
					cache_dir = os.path.join(folders, "archive_cache")
					if not os.path.exists(cache_dir):
						os.makedirs(cache_dir)
	except: pass