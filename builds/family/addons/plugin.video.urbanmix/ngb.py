# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Sourced From Online Templates And Guides
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Thanks To: Google Search For This Template
# Modified: NGB
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.urbanmix'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

xbmc.executebuiltin('Container.SetViewMode(500)')

YOUTUBE_CHANNEL_ID_1 = "PL4088E6DBCDA80604"
YOUTUBE_CHANNEL_ID_2 = "PL320A7B9E39D0B0FF"
YOUTUBE_CHANNEL_ID_3 = "PL6C274CB9CD98F182"
YOUTUBE_CHANNEL_ID_4 = "PLWFxvae3Nu5f26ncQ0NsGyWKZ_5LefjTj"
YOUTUBE_CHANNEL_ID_5 = "PLdVCmamIGu4BOvHNOxPfp7ZGiKFoYrmTf"
YOUTUBE_CHANNEL_ID_6 = "PL1T0hHFDjgDERnAbqJMnLyDrmxuU35bbR"
YOUTUBE_CHANNEL_ID_7 = "PL0SG-YYoSyzwxZNLeGPy7epfoRlkKYDEK"
YOUTUBE_CHANNEL_ID_8 = "PL8AC872D0F225EE17"
YOUTUBE_CHANNEL_ID_9 = "PLBF36AFA3DCED059D"
YOUTUBE_CHANNEL_ID_10 = "PL1T0hHFDjgDGcBdjrU1dZCHMq6dsJNMZd"
YOUTUBE_CHANNEL_ID_11 = "PL1T0hHFDjgDHYVUhVOcFWPo8KceLDS0YR"
YOUTUBE_CHANNEL_ID_12 = "PL1T0hHFDjgDFq5eiSSmeNSCg3Ynms3NVH"
YOUTUBE_CHANNEL_ID_13 = "PL1T0hHFDjgDFP8LlRP0E0FQuj4Q-wxVxI" 
YOUTUBE_CHANNEL_ID_14 = "PLDCEE77DF961BFCB4" 
YOUTUBE_CHANNEL_ID_15 = "PL23B8EBA78EE2AD47"
YOUTUBE_CHANNEL_ID_16 = "PLCC7100C247461AD6"
YOUTUBE_CHANNEL_ID_17 = "PLFD8EB1AD970B0D1A" 
YOUTUBE_CHANNEL_ID_18 = "PLA0FCD8C71A9FACD3"
YOUTUBE_CHANNEL_ID_19 = "PL_ejXIzP7qOCGCodJyyRF_7GctAn0DUAW"
YOUTUBE_CHANNEL_ID_20 = "PL-xYCUbZoLJZPxqUxNVfDdxQcjDfbx6RG" 
YOUTUBE_CHANNEL_ID_21 = "PLjIuADMrDKIauFRrHP_4jgFuIX-B8wAdh"
YOUTUBE_CHANNEL_ID_22 = "PLnH1CB9xsqNG8Bfv3bwQI0UW4nZBXGj6T"
YOUTUBE_CHANNEL_ID_23 = "PLjIuADMrDKIZh24r0bnqFlNTV8N5WD958" 
YOUTUBE_CHANNEL_ID_24 = "PLjIuADMrDKIbWEdXYa-fq_ZT7oZbnek3Y"
YOUTUBE_CHANNEL_ID_25 = "PLn8lpQwVMAVuh2ds-Q8Hu4ygs_5aziJMi"
YOUTUBE_CHANNEL_ID_26 = "PL8B2F42F23FAC31AF&index=6"
YOUTUBE_CHANNEL_ID_27 = "PL1h2g3l5piTOyF5gyGR0qNsEk62ZREz9z" 
YOUTUBE_CHANNEL_ID_28 = "PL98D68F072C101E27"
YOUTUBE_CHANNEL_ID_29 = "PL0977DB481D8DF38F"
YOUTUBE_CHANNEL_ID_30 = "PL8vxlfyMLIXqRd4XSnOpaeXt1FkxKfez_"
YOUTUBE_CHANNEL_ID_31 = "RDEMsUXUFdJOU_cQErdt6BiDYw"
YOUTUBE_CHANNEL_ID_32 = "PL37A7E8177FE8AAAD"
YOUTUBE_CHANNEL_ID_33 = "PLufMIQ_JDNbvaw3d2jNTufEUrTlQa9IqM" 
YOUTUBE_CHANNEL_ID_34 = "PL2AF7DE102A312BED"
YOUTUBE_CHANNEL_ID_35 = "PLD11FC3C53B5DF533"
YOUTUBE_CHANNEL_ID_36 = "PL94FEFB7898FC9823"
YOUTUBE_CHANNEL_ID_37 = "PL4TrGu5rwzH_DUg02i3UpY24zWGyVb7Zr"
YOUTUBE_CHANNEL_ID_38 = "PL4TrGu5rwzH9X4PdkQ_84FTTn8i__U2Ou" 
YOUTUBE_CHANNEL_ID_39 = "PLfzXEgZknUtn0Crxt07tuz0XxrR0u6wlz"
YOUTUBE_CHANNEL_ID_40 = "PLCQNxPV-Jejo9IoY-c_hCT7g31DLFe1Ms"
YOUTUBE_CHANNEL_ID_41 = "PLkPanC9DXxrVim1Xigb2aEwpC-mmqrrGO"
YOUTUBE_CHANNEL_ID_42 = "PL66F91FD399055E25"
YOUTUBE_CHANNEL_ID_43 = "PL574E9A1F4A6FA648" 
YOUTUBE_CHANNEL_ID_44 = "PLSEBSkT5M0SMeHb0mLoVkKDDt0oea0eAj"
YOUTUBE_CHANNEL_ID_45 = "PL556EE154301DCE33"
YOUTUBE_CHANNEL_ID_46 = "PL0D69250AC1161232"
YOUTUBE_CHANNEL_ID_47 = "PL-UWPlRIl68oFA13Vnzx4BlRqNWvF_B14"
YOUTUBE_CHANNEL_ID_48 = "PL23AD6A41F3640A0C" 
YOUTUBE_CHANNEL_ID_49 = "PL19A80C76FE183024"
YOUTUBE_CHANNEL_ID_50 = "PL456C0CE5D9634665"
YOUTUBE_CHANNEL_ID_51 = "PLBCE8F0A27363A34D"
YOUTUBE_CHANNEL_ID_52 = "PLFO-VhWlv-YvYApk3G7RwF3RT1pcEyiDb"
YOUTUBE_CHANNEL_ID_53 = "PLypxKwK9RwxyXJxuu0uR7bO6ANN99y_2c" 
YOUTUBE_CHANNEL_ID_54 = "PLCiM8YZKsSco0bTPniWH7oPJEFVmBDpR3"
YOUTUBE_CHANNEL_ID_55 = "PLoN5CB3TkBIyj2_icUvFWmCYTUzJ0xN9S"
YOUTUBE_CHANNEL_ID_56 = "PLNLy-Dp-F3dMfa5g6IT73TeWRzSJI9_-U"
YOUTUBE_CHANNEL_ID_57 = "PLB22BA588F9D9348E"
YOUTUBE_CHANNEL_ID_58 = "PLetCt47kP_9IvXAexj5mKVdZsgXJrY49S" 
YOUTUBE_CHANNEL_ID_59 = "PLoN5CB3TkBIylMK6hmURvmp6U34iL7P1P"
YOUTUBE_CHANNEL_ID_60 = "PL78B56E1B239B23FC"
YOUTUBE_CHANNEL_ID_61 = "PLwL9a9Ossy_8uxO3qXbwC8dxVDVmV2Wsw"
YOUTUBE_CHANNEL_ID_62 = "PL41384C6316B101FB"
YOUTUBE_CHANNEL_ID_63 = "PLwL9a9Ossy_-MOiVqNKoW4xA0dYbLyEx5" 
YOUTUBE_CHANNEL_ID_64 = "PLKVr4TXT17bOuydVH7bytCssUttprhIdx"
YOUTUBE_CHANNEL_ID_65 = "PL705172A71F31831B"
YOUTUBE_CHANNEL_ID_66 = "PLB2DE7A90921FF03C"
YOUTUBE_CHANNEL_ID_67 = "PLddSkUxmPEC8ZhwHsiAvs_XmMQphvjdYa"
YOUTUBE_CHANNEL_ID_68 = "UU_Bf08Y-3m6CMAvTms3EkKg" 
YOUTUBE_CHANNEL_ID_69 = "PL14BD193A45B39615"
YOUTUBE_CHANNEL_ID_70 = "PL3B4CB468ADC0EFE7"
YOUTUBE_CHANNEL_ID_71 = "PLX68ZEYlh74svZk0wSFjgImcZv6IK_PVc"
YOUTUBE_CHANNEL_ID_72 = "RDEMPtGB9EpccKVuEX6JeqVTsQ"
YOUTUBE_CHANNEL_ID_73 = "PLXu_cA-xfxWv6T94QwnDVf-IHfBKZtMqy" 
YOUTUBE_CHANNEL_ID_74 = "PLXu_cA-xfxWuFmI4YPj_ypbXBSmmBZotP"
YOUTUBE_CHANNEL_ID_75 = "PLXu_cA-xfxWspbqI9oG0CfSajxDLIjYvK"
YOUTUBE_CHANNEL_ID_76 = "PLXu_cA-xfxWuBkwLxd-puBSAOQwo6yig0"
YOUTUBE_CHANNEL_ID_77 = "PLXu_cA-xfxWvDeDXtZKfyHlWpmpL9t0wG"
YOUTUBE_CHANNEL_ID_78 = "PLT-2Kb_LVJZ5GsIX_f1fR5myMhr7evu2e" 
YOUTUBE_CHANNEL_ID_79 = "PLVCo0h-sEai2i6VjtdwgZj3WB4m0kmASa"
YOUTUBE_CHANNEL_ID_80 = "PLzKWdth3ZGJMvcbhg8MgvWQvCGB5WY0kY"
YOUTUBE_CHANNEL_ID_81 = "PLddSkUxmPEC-6w8qCWxJ5_geRPOB-5cv_"
YOUTUBE_CHANNEL_ID_82 = "PLAC109F1D1E81DE87"
YOUTUBE_CHANNEL_ID_83 = "PLasA1IRBDbhyGIsJcBm98xa8VNYRNRAkD" 
YOUTUBE_CHANNEL_ID_84 = "PLasA1IRBDbhwICCgPY-jrz-9TJdWWTt4W"
YOUTUBE_CHANNEL_ID_85 = "PLX68ZEYlh74t4iJ85QChLi9xfdfVGgE1e"
YOUTUBE_CHANNEL_ID_86 = "PLddSkUxmPEC_1p0OUGn9lARzrb0CPr4FR"
YOUTUBE_CHANNEL_ID_87 = "PLasA1IRBDbhwxe64nP8zho8BywnG_OzJF" 
YOUTUBE_CHANNEL_ID_88 = "PLddSkUxmPEC_Gz2rZQg56OGCxObp0Y6qN"
YOUTUBE_CHANNEL_ID_89 = "PLasA1IRBDbhxwr5_RpGb_3aQ_Lg0IvEW5"
YOUTUBE_CHANNEL_ID_90 = "PLfxsh4foa5GxgqSqtRFFkNcfdO4tvUqCn"
YOUTUBE_CHANNEL_ID_91 = "PL-UWPlRIl68qybTmllksOPllIq_GT71i6"
YOUTUBE_CHANNEL_ID_92 = "PL61D5333BC7E1374C" 
YOUTUBE_CHANNEL_ID_93 = "PLE5fC5WPVNILY6QYle8er2i8bVQ_iyhlC"
YOUTUBE_CHANNEL_ID_94 = "PLddSkUxmPEC8FE3X4KuZcAa9e7Oz5u3ks"
YOUTUBE_CHANNEL_ID_95 = "PLRHehd721eXWxOCeQ433rGNncpMo550Wj"
YOUTUBE_CHANNEL_ID_96 = "PL1T0hHFDjgDH48pZRDQlX1Ej9W8ypcMhO"
YOUTUBE_CHANNEL_ID_97 = "PL63B3E26FA995C0E3"
YOUTUBE_CHANNEL_ID_98 = "PL98F4847656FCACDC"
YOUTUBE_CHANNEL_ID_99 = "PLddSkUxmPEC9stRc8u6U-RiONpXr1ewjs"
YOUTUBE_CHANNEL_ID_100 = "PL50B1BF2632A6E093"
YOUTUBE_CHANNEL_ID_101 = "PL1T0hHFDjgDEr4bE5Tbfuc7Obv9h88E1T"
YOUTUBE_CHANNEL_ID_102 = "PL5DC5CD4BC5E4B3B8"
YOUTUBE_CHANNEL_ID_103 = "PL-UWPlRIl68oMu55-vVK3ZxJuup1yK8da"
YOUTUBE_CHANNEL_ID_104 = "PL-UWPlRIl68rJjUO_qEj8hNqk_eORGFX2"
YOUTUBE_CHANNEL_ID_105 = "PL72036965959A6A13"
YOUTUBE_CHANNEL_ID_106 = "PL92161268B99576B9"
YOUTUBE_CHANNEL_ID_107 = "PLIwp7kqcjTlK1tV27jjwYwCGpDe9D-qMR"
YOUTUBE_CHANNEL_ID_108 = "PLLmgOoYGnRZwOV7F4EF7cBRZ23gJs_1Cj"
YOUTUBE_CHANNEL_ID_109 = "PLEXj723meovEAaXKftldJovNpkD2AYWly"
YOUTUBE_CHANNEL_ID_110 = "PL7E874B8047D94DEE"
YOUTUBE_CHANNEL_ID_111 = "PLddSkUxmPEC8X3HhrH7HMC0kiipFWt2Re"
YOUTUBE_CHANNEL_ID_112 = "PLF0BAC11AFF835DCB"
YOUTUBE_CHANNEL_ID_113 = "PL9A46226A32FFD647"
YOUTUBE_CHANNEL_ID_114 = "PL89ADA4ED34AF910A"
YOUTUBE_CHANNEL_ID_115 = "PL-UWPlRIl68prUFiMailYM94pLlOVyDFu"
YOUTUBE_CHANNEL_ID_116 = "PL9uezSX-FbQxerRwsngfsm8Mksrf9jCjO"
YOUTUBE_CHANNEL_ID_117 = "PLEF1310CFF845DAC7"
YOUTUBE_CHANNEL_ID_118 = "PL41A788487EA1081B"
YOUTUBE_CHANNEL_ID_119 = "PL1E2D8A3A5212FC66"
YOUTUBE_CHANNEL_ID_120 = "PL4990093DCEB8B91B"
YOUTUBE_CHANNEL_ID_121 = "PLaIt4aj4APXroQc070wLDVSjjxTLxuKtT"
YOUTUBE_CHANNEL_ID_122 = "RDEMAAhQy0NA0a8tl8RLn-CcCg"
YOUTUBE_CHANNEL_ID_123 = "RDEM2sx0TGMjodqfMp8O6yqSnQ"
YOUTUBE_CHANNEL_ID_124 = "PL8C93E666E962003B"
YOUTUBE_CHANNEL_ID_125 = "PL0-I4Ng6a7dpYenvNUHxvg1lRcNpdZafE"
YOUTUBE_CHANNEL_ID_126 = "PLRRAa4e_avB8aI1RuT_cD-6za4crtvAlz"
YOUTUBE_CHANNEL_ID_127 = "PLGndpYI340NAS72kCyrU3-IrWzVg5Xuyk"
YOUTUBE_CHANNEL_ID_128 = "PLZACO0O8-0lumIEiCeh-4AxM5yeirWE4u"
YOUTUBE_CHANNEL_ID_129 = "PLZACO0O8-0luV46HvEK5ljRe33V7J_lys"
YOUTUBE_CHANNEL_ID_130 = "PLQy1BbegvJQ27Ss1d66uWPqy7XSjgPDtN"
YOUTUBE_CHANNEL_ID_131 = "RDEMVuC3k-bQzt1ixwgrAGHC_w"
YOUTUBE_CHANNEL_ID_132 = "PL7130C1A5BCA90113"
YOUTUBE_CHANNEL_ID_133 = "PLB685C5A10B67D3C6"
YOUTUBE_CHANNEL_ID_134 = "PLh-vD982F5Q95-qQc9Pjm0-FimqYX12gL"
YOUTUBE_CHANNEL_ID_135 = "PLiPFnhsiN6AVnureEfXIKFuuYZ1DBnFq3"
YOUTUBE_CHANNEL_ID_136 = "PL2984C4E377FA8BA6"
YOUTUBE_CHANNEL_ID_137 = "PLTrszPQGF0dkajfTuI5jzKm7oCYNYHdq1"
YOUTUBE_CHANNEL_ID_138 = "PL73F5191E57388FE1"
YOUTUBE_CHANNEL_ID_139 = "PLWdhPS36JVaw4VK-Sf8ETiXRVCcf-oG4l"
YOUTUBE_CHANNEL_ID_140 = "PLz3b2_ZQp24lx7WT4mMsSS6ndfQpKX8nB"
YOUTUBE_CHANNEL_ID_141 = "PLui_y1sf7zsdEwWiKcntM7QpWotwXyj6y"
YOUTUBE_CHANNEL_ID_142 = "PL7353DD7FF880458F"
YOUTUBE_CHANNEL_ID_143 = "PLV6tyn0NsHD64VEhpj1cpGeP1CsxrSPXE"
YOUTUBE_CHANNEL_ID_144 = "PLA3988F0B56289C98"
YOUTUBE_CHANNEL_ID_145 = "PL1F873F37DE56651C"
YOUTUBE_CHANNEL_ID_146 = "PL668CE625BDAA3A75"
YOUTUBE_CHANNEL_ID_147 = "RDEMEVaC7fv_pJtvMYku5D0Clg"
YOUTUBE_CHANNEL_ID_148 = "UU-QezoqJgvxadJqhJbP199A"
YOUTUBE_CHANNEL_ID_149 = "RDEMH0jX8oc8siFLNm4OVgTvtQ"
YOUTUBE_CHANNEL_ID_150 = "PLNF1TtPlNbF93rsc3E6FIPCaUfEGtaOwJ"
YOUTUBE_CHANNEL_ID_151 = "PLRenhQjuCDJbBODrk9QhEAVNcwRo5X7FB"
YOUTUBE_CHANNEL_ID_152 = "PL-7N_vqZjHt2_OLbgmxPGwhqazPSwsPbO"
YOUTUBE_CHANNEL_ID_153 = "PLcz6fUTBbvldDxM64nQyI9IT_BdvyVA99"
YOUTUBE_CHANNEL_ID_154 = "PLbhz5zS0JwJbXt5C2aLms2bIcdN5F2AiG"
YOUTUBE_CHANNEL_ID_155 = "PLbhz5zS0JwJZ5EIyLlkBLIVEnzTqzs4hN"
YOUTUBE_CHANNEL_ID_156 = "PL_0z4fbxWqsbvf-Lz5JjS6zFJqQ2iJmS3"
YOUTUBE_CHANNEL_ID_157 = "PLCEBABB68604B7D16"
YOUTUBE_CHANNEL_ID_158 = "PL4F149D40E1386F60"
YOUTUBE_CHANNEL_ID_159 = "PL2C45AE0237B99585"
YOUTUBE_CHANNEL_ID_160 = "PLA9SDSc3wXiohSOkfY9mYjYyYbgDJ6Wuj"
YOUTUBE_CHANNEL_ID_161 = "PLVP1nukhQ7IkYT9Juzxp5rHlLLPiXzMw8"
YOUTUBE_CHANNEL_ID_162 = "PL9uczDoXQxSauu9zLpcWuGbaSKNiRrtIc"
YOUTUBE_CHANNEL_ID_163 = "PLNF1TtPlNbF93rsc3E6FIPCaUfEGtaOwJ"
YOUTUBE_CHANNEL_ID_164 = "PLPC9GdcFrNTrJUFZmE9hpof0_KrbMPKkp"
YOUTUBE_CHANNEL_ID_165 = "PLyryiSZDpmKRZv8fYgBNL2uGM__MzLkmL"
YOUTUBE_CHANNEL_ID_166 = "RDEM8awvDbN69uJRslisq1A6mQ"
YOUTUBE_CHANNEL_ID_167 = "PL-UWPlRIl68oVeKxja9Aq0pmhMGeJFipY"
YOUTUBE_CHANNEL_ID_168 = "PLCE2D49F12DC77615"
YOUTUBE_CHANNEL_ID_169 = "PL2JnfTDSU8B8UcuWEuloweEJrdaAQ9I_Y"
YOUTUBE_CHANNEL_ID_170 = "PLLocRl8pwE6qaa4IHkZkYdRkTSZGsJwp4"
YOUTUBE_CHANNEL_ID_171 = "PLjXJu3FTSMflerjy0Hqow2Ivlsp2gcF4k"
YOUTUBE_CHANNEL_ID_172 = "PLCQNxPV-JejrxkeNtkVhPp578JWEEB9d1"
YOUTUBE_CHANNEL_ID_173 = "PLQeroY7XkiFFRTIwHU4mUs7VWGmNeq3Mk"
YOUTUBE_CHANNEL_ID_174 = "PLkB-JydfW9-TGPa40Q3wlZvtW2hhbLtF0"
YOUTUBE_CHANNEL_ID_175 = "PL3BA400C24D962D26"
YOUTUBE_CHANNEL_ID_176 = "PLNkOGKy8zEAlrE36qVB1cxm-yXvipz-kt"
YOUTUBE_CHANNEL_ID_177 = "PL4FB4615B6BF94F35"
YOUTUBE_CHANNEL_ID_178 = "PLg6pRIRseIs4eYrEoRKGhslQVl0R04tz1"
YOUTUBE_CHANNEL_ID_179 = "PLQTbOfPPkCYPsnSwoxfQvoEPxqujlPG4_"
YOUTUBE_CHANNEL_ID_180 = "PLIen3IPVo_U2zazKybthfgi7luT9J-oza"
YOUTUBE_CHANNEL_ID_181 = "PLTldUy0Fnxo18bgwRyQVGNhqcmkycWdqW"




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
        title="Akon Konvicted",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="http://vignette1.wikia.nocookie.net/lyricwiki/images/3/3a/Akon_-_Konvicted.jpg/revision/latest?cb=20061204001141",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Akon Trouble",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/7/75/AkonTrouble.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Akon Freedom",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="http://www.yorapper.com/Photos/akon-freedom-album-cover.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Busta The Big Bang",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/4/49/Bustarhymes-thebigbang.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bad meets evil Hell the sequel ",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_177+"/",
        thumbnail="http://www.southpawer.com/wp-content/uploads/2015/06/Bad_Meets_Evil_Hell_The_Sequel_album_cover_big-500x500.jpeg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Bad Boys",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_145+"/",
        thumbnail="https://massrel-library-assets.a.ssl.fastly.net/production/46206/grapcs_7.png?1459642310",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Busta Genesis",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/c/c7/Bustarhymes_genesis.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Busta Anarchy",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/8/85/Bustabuss-anarchy.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Beyonce Dangerously in love",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/8/84/Dangerously_In_Love_Album(2003).png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Beyonce Sasha Fierce",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/9/96/I_Am..._Sasha_Fierce.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Beyonce Bday",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="http://www.at40.com/cimages/var/plain_site/storage/images/repository/news/music-news/beck-s-composer-father-worked-on-beyonce-s-2006-album-b-day/394539-1-eng-US/Beck-s-Composer-Father-Worked-On-Beyonce-s-2006-Album-B-Day.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Beenie Man Maestro",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/1/14/Beenie_man_maestro.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Beenie Man Many moods of moses",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="http://vignette4.wikia.nocookie.net/lyricwiki/images/9/96/Beenie_Man_-_Many_Moods_Of_Moses.jpg/revision/latest?cb=20110220163647",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Beenie Man Back to basics",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/3/36/Back_to_Basics_(Beenie_Man_album).jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Beenie Man Undisputed",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="http://vignette1.wikia.nocookie.net/lyricwiki/images/8/83/Beenie_Man_-_Undisputed.jpg/revision/latest?cb=20110220181950",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Beenie Man Tropical Storm",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/9/9b/Beenie_Man_Al_Tropical_Storm.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bob Marley Uprising",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="http://retro.recordsale.de/cdpix/b/bob_marley_the_wailers-uprising(1).jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Bob Marley Rastaman Vibration",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="http://cps-static.rovicorp.com/3/JPG_400/MI0001/600/MI0001600487.jpg?partner=allrovi.com",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bob Marley Survival",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://images-na.ssl-images-amazon.com/images/I/51HT0Y20JJL.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bob Marley Exodus",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="http://www.musicmookreview.com/wp-content/uploads/2010/08/back-cover.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Bob Marley Legend",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="http://www.covermesongs.com/wp-content/uploads/2015/05/bobmarley-500x500.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bob Marley Babylon",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="http://vignette3.wikia.nocookie.net/lyricwiki/images/0/09/Bob_Marley_-_Babylon_By_Bus.jpg/revision/latest?cb=20140625194326",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Beastie Boys To The 5 Boroughs",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="http://cdn.albumoftheyear.org/album/to-the-5-boroughs.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Beastie Boys Check you head",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="http://www.xxlmag.com/files/2015/04/beastieboys-checkyourhead.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Beastie Boys Licenced to Ill",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="http://diffuser.fm/files/2015/07/license-to-ill.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Beastie Boys Pauls Boutique",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://images-na.ssl-images-amazon.com/images/I/41Z75KN4PKL.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Biggie Life after Death",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://i.imgur.com/rztSAqO.png",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Biggie Ready to Die",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="http://cdn.straightfromthea.com/wp-content/uploads/2011/03/ready-520x520.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Biggie Duets",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://images-na.ssl-images-amazon.com/images/I/6136FHGJVML.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="CypressHill Hill Skull and Bones",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/61sGt6S2KyL.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="CypressHill Hill Black Sunday",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="http://www.1000recordings.com/images/artist-c/cypress-hill-226-l.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="CypressHill Temple of Boom",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="http://acrossthemargin.com/wp-content/uploads/2015/10/CypressHill.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="CypressHill Hits from the bong",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="http://funkyimg.com/u2/429/518/Greatest_Hits_From_The_Bong__2005_.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Chris Brown Hits",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/5/5c/Chris_Brown_cover.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Craig David born to do it",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="http://eil.com/images/main/Craig+David+Born+To+Do+It+189687.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Craig David The story goes",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="http://covers1.img-themusic-world.info/000/10/10963.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Craig david Slicker than your Average",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="https://c1.staticflickr.com/3/2404/2489199345_4f6836b087.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Digable Planets",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_132+"/",
        thumbnail="http://toponehitwonders.com/wp-content/uploads/2010/03/digable-planets.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Dizzee Rascale",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_166+"/",
        thumbnail="https://i1.sndcdn.com/artworks-000041347123-o9et2o-t500x500.jpg",
        folder=True )		
		
    plugintools.add_item( 
        #action="", 
        title="Drake Thank me Later",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="http://www.2dopeboyz.com/wp-content/uploads/2010/05/20100503-TML.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Drake Take Care",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="https://images.genius.com/90efbd9ee9091147cdd46cb6b5f55e64.600x600x1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Drake if your reading this its....",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="http://cdn2.pitchfork.com/news/58558/46ceb4fa.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Dr Dre 2001",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="http://www.tuffgnarl.com/wp-content/uploads/2014/11/chronic2001.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Dr Dre The Aftermath",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="http://is1.mzstatic.com/image/thumb/Music/v4/d1/77/f2/d177f28d-4a2b-1180-1b3c-0793b7bab8cb/source/600x600bb.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dr Dre Detox",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="http://www.hiphopsite.com/http://www.hiphopsite.com//2014/05/detox_cover2010-big.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="DMX Grand Champ",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="http://pop-verse.com/wp-content/uploads/2013/05/00-dmx-grand_champ.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="DMX And then there was",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="http://cps-static.rovicorp.com/3/JPG_500/MI0001/816/MI0001816133.jpg?partner=allrovi.com",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="DMX The great Depression",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="https://images.rapgenius.com/5b59ca91241393b6eac14b81f2831664.510x503x1.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="DMX Its Dark and Hell is Hot",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/51LjI4HP%2BkL.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="DMX Flesh of my Flesh",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="http://cdn.certifiedmixtapez.com/UploadedFiles/Albums/dmx-flesh-of-my-flesh-blood-of-my-blood/DMX%20-%20Flesh%20Of%20My%20Flesh%20Blood%20Of%20My%20Blood.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Destinys Child Survivor",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail="http://2.bp.blogspot.com/_zjVydElJEho/TUDoDGazMsI/AAAAAAAAD9o/vNuBsvRwC5k/s1600/Destiny%2527s%2BChild%2B-%2BSurvivor%2B%2528FanMade%2BAlbum%2BCover%2529%2BMade%2Bby%2B%2BJonathanLGardner.png",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Destinys child Writings on the wall",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail="http://cdn.ratedrnb.com/2014/07/thewritingsonthewall.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Destinys Child Destiny Fulfilled",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail="http://thatgrapejuice.net/wp-content/uploads/2014/11/thatgrapejuice-destiny-fulfilled.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Destinys Child Self entitled",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_51+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/3/30/Destiny's_Child_%E2%80%93_Destiny's_Child_(album).jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Easy E",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_147+"/",
        thumbnail="http://66.media.tumblr.com/1c7d95ee7f425b9c8b2ea35630dba0a4/tumblr_nluegm5flE1qmlsnho1_500.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Eminem The Marshal Mathers LP",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_52+"/",
        thumbnail="http://orig12.deviantart.net/15aa/f/2013/365/d/e/the_marshall_mathers_lp_2_fan_version_cover_by_thatguywiththeshades-d707ooe.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Eminem Marshal Mathers LP 2",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_53+"/",
        thumbnail="https://gatsiesheikar.files.wordpress.com/2013/11/1452401_10151714501005079_1355930697_n.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Eminem Encore",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_54+"/",
        thumbnail="http://hw-img.datpiff.com/mc64fd12/Eminem_Eminem_-_Encore_the_Special_Edition-front-large.jpg",
        folder=True )	
		
    plugintools.add_item( 
        #action="", 
        title="The Eminem Show",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_55+"/",
        thumbnail="https://s-media-cache-ak0.pinimg.com/736x/ed/6f/55/ed6f55f684f57e7ae1ddf607166c68ec.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Eminem Relapse",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_56+"/",
        thumbnail="http://static.idolator.com/uploads/2009/04/relapse_cover.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Eminem Recovery",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_57+"/",
        thumbnail="http://data.whicdn.com/images/48148319/large.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Eminem Curtain Call",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_58+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/51Vh-qUCKBL.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="The Slim Shady LP",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_59+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/3/35/Eminem_-_The_Slim_Shady_LP_CD_cover.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Eminem presents the Re-up",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_60+"/",
        thumbnail="http://shadyrecords.com/wp-content/uploads/2013/01/0000427361_500.jpg",
        folder=True )
    		
    plugintools.add_item( 
        #action="", 
        title="50 Cent Get rich or die trying",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_174+"/",
        thumbnail="http://www.vmusic.com.au/content/50-cent-get-rich-or-die-tryin--artwork.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="50 Cent The Massacre",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_175+"/",
        thumbnail="https://images-na.ssl-images-amazon.com/images/I/6177K9GjoZL.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Elephant Man Good to Go",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_61+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/5193Y6H6DGL.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Elephant man Lets get Physical",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_62+"/",
        thumbnail="http://eil.com/images/main/Elephant+Man+Lets+Get+Physical+480812.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Elephant Man Higher Level",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_63+"/",
        thumbnail="http://welcometojamrockreggaecruise.com/2015cruise/wp-content/uploads/2014/12/elephantman1.jpg",
        folder=True )
    
    plugintools.add_item( 
        #action="", 
        title="Flava Unit MCs",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://40.media.tumblr.com/tumblr_lzjtafQFrn1r6jzd3o1_500.jpg",
        folder=True )
	
    plugintools.add_item( 
        #action="", 
        title="Flo Rida Mail on Sunday",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_64+"/",
        thumbnail="http://vignette1.wikia.nocookie.net/lyricwiki/images/8/88/Flo_Rida_-_Mail_On_Sunday.jpg/revision/latest?cb=20090327185149",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Flo Rida R.O.O.T.S",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_65+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/61Pu3R6TeaL.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Flo Rida Only one Flo",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_66+"/",
        thumbnail="http://3.bp.blogspot.com/_sKQxo0H2khc/TQgbaYzxqpI/AAAAAAAAAG4/vsH_xf5J760/s1600/1290517566_flo-rida-only-one-flo-part-1-500x500.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Geto Boys",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_178+"/",
        thumbnail="http://direct-ns.rhap.com/imageserver/v2/albums/Alb.122926117/images/500x500.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Heavy D",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_179+"/",
        thumbnail="https://images.genius.com/e47e90aa8aedb08596054d3fcb4fdc02.500x500x1.jpg",
        folder=True )
   		
    plugintools.add_item( 
        #action="", 
        title="Iggy Azelea The New Classic",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_134+"/",
        thumbnail="http://cbsradionews.files.wordpress.com/2014/03/iggy_azalea_new_classic-500x500.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Jay Z Vevo",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_68+"/",
        thumbnail="http://cdn.albumoftheyear.org/album/kingdom-come.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Jay Z Playlist",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_69+"/",
        thumbnail="http://www.onlycoolstuff.net/wp-content/uploads/2013/12/jay-z.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Joe Budden",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_70+"/",
        thumbnail="http://www.underground-dtsa.com/images/events/2016/JoeBudden-may27-2016.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Jay Z Reasonable Doubt",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_71+"/",
        thumbnail="https://41.media.tumblr.com/5bf9d1df872ec5f76ccc3d979aca2486/tumblr_mjtygySfHn1raw34bo1_500.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Jamie Foxx",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_72+"/",
        thumbnail="http://boi-1da.net/wp-content/uploads/2015/03/Jamie-Foxx.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="JT Futuresex Lovesound",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_128+"/",
        thumbnail="https://charlieprime.files.wordpress.com/2015/12/img_1694.jpg?w=604",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="JT The 20/20 Experience",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_129+"/",
        thumbnail="http://trinitrent.com/wp-content/uploads/2013/07/justin-timberlake-20-experience-2-thelavalizard.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="JT Justified",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_130+"/",
        thumbnail="https://s-media-cache-ak0.pinimg.com/736x/47/19/4c/47194c346dd2787841856a2b178d64f5.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Kendrick Lemar",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_180+"/",
        thumbnail="http://cache.umusic.com/_sites/kendricklamar.com/images/og.jpg",
        folder=True )
    		
    plugintools.add_item( 
        #action="", 
        title="Kanye College Dropout",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_73+"/",
        thumbnail="http://images.complex.com/complex/image/upload/t_article_image/kap7sz3mbnrnrhdugnjl.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Kanye Late Registration",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_74+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/51kfhkHeMTL.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Kanye Graduation",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_75+"/",
        thumbnail="http://cdn3.pitchfork.com/albums/10462/afa9da9d.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Kanye Beutifull dark twisted Fantasy",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_76+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/f/f0/My_Beautiful_Dark_Twisted_Fantasy.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Kanye Yeezus",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_77+"/",
        thumbnail="https://griffinmiller47.files.wordpress.com/2014/08/tumblr_moelxko29e1qjo50co1_1371248265_cover.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Lenny Kravits Hits",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_131+"/",
        thumbnail="https://31.media.tumblr.com/aa260999d502bead0e6e7e02794c92e0/tumblr_inline_n8xdd1YCBV1qazwkm.jpg",
        folder=True )		
		
    plugintools.add_item( 
        #action="", 
        title="LiL Jon We still Crunk",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_78+"/",
        thumbnail="http://vignette3.wikia.nocookie.net/lyricwiki/images/3/33/Lil_Jon_%26_The_East_Side_Boyz_-_We_Still_Crunk!!.jpg/revision/latest?cb=20120209202607",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="LiL Jon Crunk Juice",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_80+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/619JlPfFd7L.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="LiL Jon The Bottom",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_81+"/",
        thumbnail="https://lh5.googleusercontent.com/k7IuOJ8bwQaerSZBmnG4awi30nOSCiL2eKXJUTJNqA5q21zd-iGcD26j0o_PDWi7cbI5KDbL=w300",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LiL Jon Crunk Rock",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_82+"/",
        thumbnail="http://media1.fdncms.com/atlanta/imager/lil-jon-crunk-rock/u/original/1513801/1276280470-crunkrock.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LiL Wayne The Carter",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_83+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/d/d8/Lil_Wayne_-_Tha_Carter.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="LiL Wayne The Carter 2",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_84+"/",
        thumbnail="http://www.lilwaynehq.com/images/discography/tha-carter-2-artwork.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LiL Wayne The Carter 3",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_85+"/",
        thumbnail="http://www.lilwaynehq.com/images/discography/tha-carter-3-artwork.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="The Carter 4",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_86+"/",
        thumbnail="http://www.lilwaynehq.com/images/blog/lil-wayne-tha-carter-4-deluxe-cover.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LiL Wayne I am not a human being",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_87+"/",
        thumbnail="http://www.belfasttelegraph.co.uk/migration_catalog/article25722960.ece/ALTERNATES/h342/lil%20wayne",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LiL Wayne I am not a human being 2",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_88+"/",
        thumbnail="http://www.killerhiphop.com/wp-content/uploads/2013/01/lilwayneIANAHB2cover.jpeg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="LiL Wayne Rebirth",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_89+"/",
        thumbnail="http://www.lilwaynehq.com/images/blog/lil-wayne-rebirth-front-cover.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LiL Wayne Free Weezy",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_90+"/",
        thumbnail="http://stshd.translationllc.netdna-cdn.com/wp-content/uploads/2015/02/lil-wayne-the-free-weezy-album-cover1.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Ludacris Back for the First Time",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_91+"/",
        thumbnail="http://covers.discorder.com/fullsize/front/0731454813822.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ludacris Word of Mouf",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_92+"/",
        thumbnail="http://theupmag.com/wp-content/uploads/2015/11/tumblr_nxzpliMqYi1t1yehoo1_500.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Ludacris Disturbing thu Peace",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_94+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/8/81/Ludacris_Presents_Disturbing_tha_Peace.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Ludacris Chicken and Beer",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_93+"/",
        thumbnail="http://66.media.tumblr.com/5161d7341695711cbe8adb424454598c/tumblr_mhfv7fybM01rre7pmo1_500.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Ludacris Red Light District",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_95+"/",
        thumbnail="https://cdn.shopify.com/s/files/1/0993/9646/products/DEFJ348302CD_large.jpeg?v=1457734655",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Ludacris Release Therapy",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_96+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/51kg6lXnu2L.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Ludacris Theater of the mind",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_97+"/",
        thumbnail="http://i.imgur.com/XcFwspw.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Ludacris Battle of the sexes",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_98+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/51TjqIgs1dL.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Ludacris Ludaversal",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_99+"/",
        thumbnail="http://hiphop101online.com/wp-content/uploads/2015/04/ludacrisludaversal300x300.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Macklemore The VS. Redux",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_125+"/",
        thumbnail="http://i75.fastpic.ru/big/2016/0221/21/2bbdcf3fd1edaa2e9dd4bd766709e921.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Macklemore The Heist",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_126+"/",
        thumbnail="http://static.djbooth.net/pics-albums/macklemore-theheist.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Macklemore This unholly Mess",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_126+"/",
        thumbnail="http://images.starpulse.com/news/bloggers/1297578/blog_images/-macklemore.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="",
		title="Method Man",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_181+"/",
        thumbnail="http://www.hotnewhiphop.com/image/500x500/cover/1433461790_25f28e1b2faf07779896aeb936b193f0.jpg/c4ed666b67860e6ce41590dd1029675c/1433461790_a5e0b3704704397fab9540fa8782d9f5.jpg",
        folder=True )		
		
    plugintools.add_item( 
        #action="",
		title="Missy Elliot Supa Dupa Fly",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_100+"/",
        thumbnail="http://s3.amazonaws.com/rapgenius/1362802256_Supa%20Dupa%20Fly%20178708_1_f.png",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Missy Elliot So Addictive",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_101+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/61cr01UA5QL.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Missy Elliot Under Construction",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_102+"/",
        thumbnail="https://images-na.ssl-images-amazon.com/images/I/517WkAnT6JL.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Missy Elliot This is not a test",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_103+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/0/0d/Missy_Elliott_-_This_is_not_a_test_-_Album.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Missy Elliot The Cookbook",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_104+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/515YMP6MD5L.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Marvin Gaye",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_105+"/",
        thumbnail="http://okf-cdn.okayplayer.com/wp-content/uploads/2013/04/artworks-000042659444-mjzrrp-t500x500.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="N.E.R.D In search of",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_138+"/",
        thumbnail="https://s-media-cache-ak0.pinimg.com/736x/d7/2b/98/d72b98345b7505f238b9ea391adee383.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="N.E.R.D Fly or Die",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_139+"/",
        thumbnail="http://i.imgur.com/VIbp9nK.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="N.E.R.D Nothing",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_140+"/",
        thumbnail="http://hypetrak.com/images/2010/10/N.E.R.D.-Nothing-Tracklist.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="N.E.R.D Seeing Sounds",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_141+"/",
        thumbnail="http://gangstaraptalk.com/wp-content/uploads/nd9oqLw.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Nicki Minaj",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_151+"/",
        thumbnail="http://stupiddope.com/wp-content/uploads/2013/08/nicki-minaj-w1-e1338411687203.jpeg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="NAS Illmatic",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_106+"/",
        thumbnail="http://orig04.deviantart.net/e6b0/f/2011/122/0/b/nas_illmatic_cover__by_skred_by_skred210-d3ffbcm.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="NAS It was Written",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_107+"/",
        thumbnail="https://i.imgur.com/ZRKPQYU.png",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="NAS I am-Double Album",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_108+"/",
        thumbnail="http://images.rapgenius.com/2v9tzreq0pvflfzzs6ie3dlmj.500x500x1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="NAS Nastradamus",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_109+"/",
        thumbnail="http://i133.photobucket.com/albums/q59/blackboi2009/8c34h3q.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="NAS Stillmatic",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_110+"/",
        thumbnail="http://img2-ak.lst.fm/i/u/ar0/b96e1ee04faa4f3f84b119a693aab756",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="NAS God's Son",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_111+"/",
        thumbnail="http://assets.rollingstone.com/assets/images/album_review/b43efee08ff0a45863ba1a0a0a0d034636c8d596.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="NAS Hiphop is Dead",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_112+"/",
        thumbnail="https://images-na.ssl-images-amazon.com/images/I/51usHqm3%2BdL.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="NAS Uutitled",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_113+"/",
        thumbnail="http://img11.nnm.me/b/c/5/9/8/bc59850691113266865330b85d2f60bd_full.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="NAS Life is Good",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_114+"/",
        thumbnail="http://www.xclusiveszone.net/wp-content/uploads/2012/06/nas-life-is-good-500x500.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Nelly Country Grammar",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_115+"/",
        thumbnail="http://upc.fm/wp-content/uploads/2015/09/500x500.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Nelly Nellyville",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_116+"/",
        thumbnail="http://cdn.albumoftheyear.org/album/10479-nellyville.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Nelly Sweat",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_117+"/",
        thumbnail="http://cs621630.vk.me/v621630565/378e/ZspP4Hu5wAM.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Nelly Furtado Loose",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_118+"/",
        thumbnail="https://c1.staticflickr.com/1/192/486937142_a9d61bce53.jpg",
        folder=True )
    plugintools.add_item( 
        #action="",
		title="Nelly Furtado Whoa Nelly",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_119+"/",
        thumbnail="https://s-media-cache-ak0.pinimg.com/736x/cc/f0/0d/ccf00d484c3aa8d6ae1d43cf347f6168.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Nelly Furtado Folklore",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_120+"/",
        thumbnail="https://c1.staticflickr.com/5/4117/4829659873_197b2a5bde.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Nelly Furtado Spirit Indestructible",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_121+"/",
        thumbnail="http://trinitrent.com/wp-content/uploads/2012/05/nelly-furtado-tsi-2_thelavalizard.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="NWA Hits",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_122+"/",
        thumbnail="http://ec1.images-amazon.com/images/I/61TQ0QCES7L.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Naughty by nature hits",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_123+"/",
        thumbnail="http://www.okayplayer.com/wp-content/uploads/2013/05/naughty-by-nature-lp-cover.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Pitbull",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_165+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/61QzTGbaQwL.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Public Enemy",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_133+"/",
        thumbnail="http://www.mixtapewall.com/uploads/2012/06/Public_Enemy-Most_of_My_Heroes.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Pharrell In My Mind",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_135+"/",
        thumbnail="http://images.amazon.com/images/P/B000BLI4TM.01._SS500_SCLZZZZZZZ_V64908687_.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Pharrel Out of my Mind",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_136+"/",
        thumbnail="http://2.bp.blogspot.com/_UBfVa1fHf5w/TAHfJLQGBvI/AAAAAAAABGY/jxISsVuN1kY/s1600/out-of-my-mind.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Pharrell GIRL",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_137+"/",
        thumbnail="http://www.clutchmagonline.com/wp-content/uploads/2014/02/pharrell_girl-500x500.jpeg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Pink",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_142+"/",
        thumbnail="http://i71.fastpic.ru/big/2015/0901/24/07d1fc2763a7e8443e005750e3153824.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Puff Daddy no way out",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_143+"/",
        thumbnail="http://i.imgur.com/JtHldBj.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="P Diddy Press Play",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_144+"/",
        thumbnail="https://images-na.ssl-images-amazon.com/images/I/51Q4PTX89AL.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Diddy Dirty Money",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_147+"/",
        thumbnail="http://factmag-images.s3.amazonaws.com/wp-content/uploads/2012/09/Diddy_Dirty_Money_Love_Love_Vs_Hate_Love-front-large1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Redman",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_79+"/",
        thumbnail="http://cps-static.rovicorp.com/3/JPG_500/MI0003/746/MI0003746308.jpg?partner=allrovi.com",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Run DMC Vevo",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_148+"/",
        thumbnail="http://richardbeaversgallery.com/images/art/artists/run-dmc-1341012607.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Run DMC",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_149+"/",
        thumbnail="http://direct-ns.rhap.com/imageserver/v2/albums/Alb.172805514/images/500x500.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="R Kelly The hits",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_150+"/",
        thumbnail="http://rnbmain.thisisrnb.netdna-cdn.com/wp-content/uploads/2009/08/r-kelly-untitled-album-cover.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Shabba Ranks",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_152+"/",
        thumbnail="https://images-na.ssl-images-amazon.com/images/I/513DUWPvBOL.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Timberland Shock Value",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_167+"/",
        thumbnail="http://blogsferamusic.files.wordpress.com/2009/09/timbaland_shockvalue_v1.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Timberland Shock Value 2",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_168+"/",
        thumbnail="https://images-na.ssl-images-amazon.com/images/I/510artTWJPL.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Twista",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_169+"/",
        thumbnail="http://i2.wp.com/inyaearhiphop.com/wp-content/uploads/2016/03/twista-arrested-indiana-e1458927614281.png?resize=500%2C500",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Tupac All eyes on me",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_171+"/",
        thumbnail="http://www.dafont.com/forum/attach/orig/6/8/68010.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Tupac The Greatest hits",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_172+"/",
        thumbnail="http://a1yola.com/wp-content/uploads/2010/08/2Pac-Greatest-Hits.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Tupac Resurection",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_173+"/",
        thumbnail="http://images.complex.com/complex/image/upload/c_limit,fl_progressive,q_80,w_680/kudrbbz9bwmsy9yobhal.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Tribe called Quest",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_153+"/",
        thumbnail="http://eil.com/images/main/A+Tribe+Called+Quest+The+Best+Of+431067.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Rhianna Music of the sun",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_154+"/",
        thumbnail="http://direct-ns.rhap.com/imageserver/v2/albums/Alb.7579447/images/500x500.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Rhianna Girl like me ",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_155+"/",
        thumbnail="http://i74.fastpic.ru/big/2016/0216/e2/52efbba013da0315cf964b4a1ddbd4e2.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Rhianna Good girl gone bad",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_156+"/",
        thumbnail="http://madparadox.com/MusicFiles/Rihanna/Good%20Girl%20Gone%20Bad%20Reloaded/cover.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Rhianna Rated R",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_157+"/",
        thumbnail="http://2.bp.blogspot.com/_BJbaPRBdOYU/SwDfgz8EhcI/AAAAAAAAE6s/wULPERT9uJk/s1600/RATED-R-VIPCOVERLAND.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Rhianna Loud",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_158+"/",
        thumbnail="https://c1.staticflickr.com/7/6046/5899394654_b8856e80ae_z.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Rhianna Talk that Talk",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_159+"/",
        thumbnail="http://2.bp.blogspot.com/_BJbaPRBdOYU/SwDfgz8EhcI/AAAAAAAAE6s/wULPERT9uJk/s1600/RATED-R-VIPCOVERLAND.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Rhianna Unapologetic",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_160+"/",
        thumbnail="http://11vh803uiffj14claev3ivq1.wpengine.netdna-cdn.com/wp-content/uploads/2012/11/rihanna-unapologetic-500x500.jpg",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Rhianna Anti",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_161+"/",
        thumbnail="http://cdn-images.deezer.com/images/cover/4fc5f387624c25de0ec96b4719e3a36d/500x500.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="R Kelly",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_163+"/",
        thumbnail="http://rnbmain.thisisrnb.netdna-cdn.com/wp-content/uploads/2009/08/r-kelly-untitled-album-cover.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="",
		title="Tevin Campbell",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_164+"/",
        thumbnail="http://vignette3.wikia.nocookie.net/lyricwiki/images/e/ee/Tevin_Campbell_-_Tevin_Campbell.jpg/revision/latest?cb=20120324104849",
        folder=True )

    plugintools.add_item( 
        #action="",
		title="Wu Tang Clan",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_162+"/",
        thumbnail="http://assets.craniumfitteds.com/images/main/Rocksmith-And-Wu-Tang-Clan-The-Wu-Tang-Logo-Tank-White-2.jpg",
        folder=True )
		


run()