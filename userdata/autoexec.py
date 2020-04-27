import os

HomeDir = xbmc.translatePath('special://home')
WindowsCache = os.path.join(xbmc.translatePath('special://home'), 'cache')
OtherCache = xbmc.translatePath('special://temp')

if os.path.exists(WindowsCache)==True:   
	path=WindowsCache
	import glob
	for infile in glob.glob(os.path.join(path, '*.fi')):
		File=infile
		print infile
		os.remove(infile)

if os.path.exists(OtherCache)==True:   
	path=OtherCache
	import glob
	for infile in glob.glob(os.path.join(path, '*.fi')):
		File=infile
		print infile
		os.remove(infile)