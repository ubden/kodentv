# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Sourced From Online Templates And Guides
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Thanks To: Google Search For This Template
# Modified: Pulse
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.pulsebeats'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

xbmc.executebuiltin('Container.SetViewMode(500)')

YOUTUBE_CHANNEL_ID_1 = "PLywWGW4ILrvpqqkgKRV8jpZMaUPohQipP"
YOUTUBE_CHANNEL_ID_2 = "PL64E6BD94546734D8"
YOUTUBE_CHANNEL_ID_3 = "PLFbWuc6jwPGeqFkoDBq87CcmlurwrlEGv"
YOUTUBE_CHANNEL_ID_4 = "PLqYXv_L7NiEyYnfZhVHR7ixOTANxjes89"
YOUTUBE_CHANNEL_ID_5 = "PL8F6B0753B2CCA128"
YOUTUBE_CHANNEL_ID_6 = "PLsWYhntNoL3hW_J9Ulrb-3s1iFaVQb1Y8"
YOUTUBE_CHANNEL_ID_7 = "PLgwqhB4wv9zUKFtOJp_V2VhcQctNHT9NP"
YOUTUBE_CHANNEL_ID_8 = "PLH6pfBXQXHECUaIU3bu9rjG2L6Uhl5A2q"
YOUTUBE_CHANNEL_ID_9 = "PLuK6flVU_Aj45QZ_A5ld0-pP3CIkoNQDk"
YOUTUBE_CHANNEL_ID_10 = "PLGBuKfnErZlCkRRgt06em8nbXvcV5Sae7"
YOUTUBE_CHANNEL_ID_11 = "PLGBuKfnErZlAkaUUy57-mR97f8SBgMNHh"
YOUTUBE_CHANNEL_ID_12 = "PLCD0445C57F2B7F41"
YOUTUBE_CHANNEL_ID_13 = "PL7DA3D097D6FDBC02" 
YOUTUBE_CHANNEL_ID_14 = "PLpuDUpB0osJmZQ0a3n6imXirSu0QAZIqF" 
YOUTUBE_CHANNEL_ID_15 = "PLF-DoV_vajTzKav0aTTlOT6o56QGo5IKn" 
YOUTUBE_CHANNEL_ID_16 = "PLhInz4M-OzRX96VZlkhDs9s1WuyQvKKTL" 
YOUTUBE_CHANNEL_ID_17 = "PLQog_FHUHAFVRsO4otlwzn0bZspSAefOl"
YOUTUBE_CHANNEL_ID_18 = "PLBA204FBDC0F345BB" 

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
        title="UK TOP 100",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="http://www.hometohomecalls.com/wp-content/uploads/2015/12/Music-Charts.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BEST OF DANCE",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="http://static.fnac-static.com/multimedia/images_produits/ZoomPE/8/2/7/3596971209728.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BEST OF R&B",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="http://www.mixcrate.com/img/ugc/covers/2/8/28827_l.jpg?v=119201344",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="BEST OF HOUSE",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="http://www.elfm.co.uk/wp-content/uploads/2012/02/House-Music-Festival-Logo-441x400.gif",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="BEST OF TRANCE",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://thumbnailer.mixcloud.com/unsafe/300x300/profile/0/2/1/d/e2fe-eb16-4031-8f0a-307bf026e005.jpg",
        folder=True )	

    plugintools.add_item( 
        #action="", 
        title="BEST OF SOUL",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://lh3.googleusercontent.com/Ey34WOE2jwn2-Fxpv__byOi4jcsaC69mIGlTeyFGYYWRO4obi5i8nhl_1-suIzp76bA=w300",
        folder=True )	

    plugintools.add_item( 
        #action="", 
        title="BEST OF CLASSIC ROCK",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="http://www.mixcrate.com/img/ugc/covers/9/1/9174620_l.jpg?v=326201557",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BEST OF JAZZ",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="http://debrusbrewery.com/wp-content/uploads/jazz-band-300x300.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BEST OF COUNTRY",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="http://theicemanshow.com/wp-content/uploads/2015/08/CountryMusic.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="BEST ALTERNATIVE SONGS",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="http://www.mixcrate.com/img/ugc/covers/2/5/257135_l.jpg?v=118201333",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BEST OF HIP HOP",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="http://lpdc.net/wp-content/uploads/2015/08/hip-hop-300x300.jpeg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BEST OF THE 50's",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="http://i228.photobucket.com/albums/ee193/CSponhaltz/8082_neon_back_to_the_fifties.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BEST OF THE 60's",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRM6qDUmO4spNstYXSIBO4GkCI3QEGBZbej_2f8Yyoi-g0-CPkAyA",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BEST OF THE 70's",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="http://www.themovieguys.net/wp-content/uploads/2012/01/iheart70s.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BEST OF THE 80's",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://images-eu.ssl-images-amazon.com/images/I/51FDqQfYfgL._SY300_QL70_.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BEST OF THE 90's",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcT7yx_XBv3v3nmEtBqIcKoa8Hrm3lQtQWx9Mx7l1TWlUZzlRit7",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BEST OF THE 00's",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://rymimg.com/lk/f/s/19bccc20b0092e0f768f5cfe3f79959b/4852576.jpeg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BEST OF 10/16",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="http://techmento.com/wp-content/uploads/2011/07/sony_music_01-300x300.jpg",
        folder=True )

run()