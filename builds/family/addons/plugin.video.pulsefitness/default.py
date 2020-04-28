# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pinoy abroad v2 by pulsemediahubuk (pulsemediahub)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: pulsemediahubuk
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.pulsefitness'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "FitnessBlender"
YOUTUBE_CHANNEL_ID_2 = "robinforlife"
YOUTUBE_CHANNEL_ID_3 = "myfitgirls"
YOUTUBE_CHANNEL_ID_4 = "lovezumba"
YOUTUBE_CHANNEL_ID_5 = "BeFit"
YOUTUBE_CHANNEL_ID_6 = "runtasticFitness"
YOUTUBE_CHANNEL_ID_7 = "Perfectfitnesstv"
YOUTUBE_CHANNEL_ID_8 = "popsugartvfit"
YOUTUBE_CHANNEL_ID_9 = "bodybuildandfitness"
YOUTUBE_CHANNEL_ID_10 = "superherofitnesstv"
YOUTUBE_CHANNEL_ID_11 = "STORYOFSHIRTLESS"
YOUTUBE_CHANNEL_ID_12 = "TheQuestForFitness"
YOUTUBE_CHANNEL_ID_13 = "fit"
YOUTUBE_CHANNEL_ID_14 = "shauntfitness"

# Entry point
def run():
    plugintools.log("docu.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("docu.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="Fitness Blender",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="http://icons.iconarchive.com/icons/icons8/ios7/128/Sports-Exercise-icon.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="robinforlife",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="http://icons.iconarchive.com/icons/sportsbettingspot/summer-olympics/128/weightlifting-icon.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="My Fitness Girls",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="http://icons.iconarchive.com/icons/sonya/swarm/128/gym-icon.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Zumba Fitness",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="http://s3.postimg.org/lhzsp1h1f/zumba.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Be Fit",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="http://icons.iconarchive.com/icons/icons-land/metro-raster-sport/128/Fitness-Hand-Grippers-icon.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Runtastic Fitness",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="http://icons.iconarchive.com/icons/sonya/swarm/128/Running-icon.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Perfect fitness tv",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="http://icons.iconarchive.com/icons/sportsbettingspot/summer-olympics/128/weightlifting-icon.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="pop sugar tvfit",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="http://icons.iconarchive.com/icons/hopstarter/3d-cartoon-vol3/128/Yahoo-Messenger-icon.png",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="bodybuild and fitness",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="http://icons.iconarchive.com/icons/sonya/swarm/128/Running-icon.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="super hero fitness tv",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="http://icons.iconarchive.com/icons/icons8/ios7/128/Sports-Exercise-icon.png",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="Fit Media Channel",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="http://icons.iconarchive.com/icons/iconsmind/outline/128/Bodybuilding-icon.png",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Jon Venus",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="http://icons.iconarchive.com/icons/tribalmarkings/colorflow/128/bodybuilding-icon.png",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="FiT – Global Fitness Network",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="http://icons.iconarchive.com/icons/iconsmind/outline/128/weight-Lift-icon.png",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Shaun T",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="http://icons.iconarchive.com/icons/icons8/ios7/128/Sports-Exercise-icon.png",
        folder=True ) 
		
           
   	
run()
