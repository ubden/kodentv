#------------------------------------------------------------
# No Limits Fresh Start
# by Kodi No Limits
#------------------------------------------------------------

import os,sys,xbmcaddon
import plugintools

AddonID='plugin.video.nolimitsfreshstart'
AddonTitle="Fresh Start"
KODIVERSION = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
VERSION = "1.2"

def run(): # Entry point
    plugintools.log("freshstart.run"); params=plugintools.get_params() # Get params
    if params.get("action") is None: main_list(params)
    else: action=params.get("action"); exec action+"(params)"
    plugintools.close_item_list()

##################
#  FRESH START   #
##################
def main_list(params): # Main menu
    plugintools.log("freshstart.main_list "+repr(params)); yes_pressed=plugintools.message_yes_no(AddonTitle,"Do you wish to restore ","Kodi to default settings?")
    if yes_pressed:
        addonPath=xbmcaddon.Addon(id=AddonID).getAddonInfo('path'); addonPath=xbmc.translatePath(addonPath); 
        xbmcPath=os.path.join(addonPath,"..",".."); xbmcPath=os.path.abspath(xbmcPath); plugintools.log("freshstart.main_list xbmcPath="+xbmcPath); failed=False

        EXCLUDES1 = ['plugin.video.nolimitswizard','script.module.requests','script.module.addon.common','packages']            
    
        if KODIVERSION >= 17.0: ##Check if Kodi 17.x Krypton
            EXCLUDES2 = ['favourites.xml','advancedsettings.xml','profiles.xml','Addons27.db','ADSP0.db']
        else: ##Check if Kodi 16.x Jarvis or Earlier
            EXCLUDES2 = ['favourites.xml','advancedsettings.xml','profiles.xml'] 
                
        try:
            for root, dirs, files in os.walk(xbmcPath,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES1] ##Skip Exclude Directories
                for name in files:
                    if name not in EXCLUDES2:  ##Skip Exclude2 Files
                        try: os.remove(os.path.join(root,name))
                        except:
                            if name not in ["Addons15.db","MyVideos75.db","Textures13.db","xbmc.log"]: failed=True
                            plugintools.log("Error removing "+root+" "+name)
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name))
                    except:
                        if name not in ["Database","userdata"]: failed=True
                        plugintools.log("Error removing "+root+" "+name)
                        
            if not failed: 
                REMOVE_EMPTY_FOLDERS_BUILDS()
                plugintools.log("freshstart.main_list All user files removed, you now have a clean Kodi install"); plugintools.message(AddonTitle,"The process is complete, you're now back to a fresh Kodi configuration!","Please reboot your system or restart Kodi in order for the changes to be applied.")
            else: 
                plugintools.log("freshstart.main_list User files partially removed"); plugintools.message(AddonTitle,"The process is finished, you're now back to a fresh Kodi configuration!","Please reboot your system or restart Kodi in order for the changes to be applied.")
        except: plugintools.message(AddonTitle,"Problem found","Your settings have not been changed"); import traceback; plugintools.log(traceback.format_exc()); plugintools.log("freshstart.main_list NOT removed")
        plugintools.add_item(action="",title="Done",folder=False)
    else: plugintools.message(AddonTitle,"Your settings","have not been changed"); plugintools.add_item(action="",title="Done",folder=False)


############################
###REMOVE EMPTY FOLDERS#####
############################

def REMOVE_EMPTY_FOLDERS_BUILDS():
#initialize the counters
	print"########### Start Removing Empty Folders #########"
	empty_count = 0
	used_count = 0
	
	EXCLUDES3 = ['Thumbnails']

	try:
		for dirs, subdirs, files in os.walk(HOME,topdown=True):
			subdirs[:] = [d for d in subdirs if d not in EXCLUDES3]
			if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
				empty_count += 1 #increment empty_count
				os.rmdir(dirs) #delete the directory
				print "successfully removed: "+dirs
			elif len(subdirs) > 0 and len(files) > 0: #check for used directories
				used_count += 1 #increment 
	except: pass

run()