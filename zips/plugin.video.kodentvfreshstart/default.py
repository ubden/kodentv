#------------------------------------------------------------
# No Limits Fresh Start
#------------------------------------------------------------

import os,sys,xbmcaddon
import plugintools

AddonID='plugin.video.kodentvfreshstart'
AddonTitle="Fresh Start"
VERSION = "1.0"
EXCLUDES1 = ['script.module.requests','script.module.addon.common']            
EXCLUDES2 = []

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
                        
            if not failed: plugintools.log("freshstart.main_list All user files removed, you now have a clean Kodi install"); plugintools.message(AddonTitle,"The process is complete, you're now back to a fresh Kodi configuration!","Please reboot your system or restart Kodi in order for the changes to be applied.")
            else: plugintools.log("freshstart.main_list User files partially removed"); plugintools.message(AddonTitle,"The process is finished, you're now back to a fresh Kodi configuration!","Please reboot your system or restart Kodi in order for the changes to be applied.")
        except: plugintools.message(AddonTitle,"Problem found","Your settings have not been changed"); import traceback; plugintools.log(traceback.format_exc()); plugintools.log("freshstart.main_list NOT removed")
        plugintools.add_item(action="",title="Done",folder=False)
    else: plugintools.message(AddonTitle,"Your settings","have not been changed"); plugintools.add_item(action="",title="Done",folder=False)
        
run()