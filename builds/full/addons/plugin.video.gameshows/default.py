# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Game Shows
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: something else promotions
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.gameshows'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "PLViprzlAIySwNGM5_LQA9jvvMlbVHmgBe"
YOUTUBE_CHANNEL_ID_2 = "PL2B05267D592362C2"
YOUTUBE_CHANNEL_ID_3 = "PLuKKJ5FR6_i9J6FoH5aNlh-nf9Xxjw3vh"
YOUTUBE_CHANNEL_ID_4 = "PLuKKJ5FR6_i9Bnikl9xgykuFM-bs_9YCr"
YOUTUBE_CHANNEL_ID_5 = "PLQh8Ze6l7j-ivkprrUJl-bu6qsrB2crkL"
YOUTUBE_CHANNEL_ID_6 = "PLuKKJ5FR6_i-LbxNHjv_uB4N7OUsqXc9-"
YOUTUBE_CHANNEL_ID_7 = "PLgkOniLhKf9NAb_6o9JzYwtnDmfVWqHUr"
YOUTUBE_CHANNEL_ID_8 = "PLOfEy4Ga6wU0AhxKyrXQQj2pfpPyWlxMv"
YOUTUBE_CHANNEL_ID_9 = "PLuKKJ5FR6_i-G3X2qR9kJ6TRri07AKsJe"
YOUTUBE_CHANNEL_ID_10 = "PLeUU3kj3xcQrkjpUB6m-E8knuqALWLHlS"
YOUTUBE_CHANNEL_ID_11 = "PLZ2Bc2lovJ1Y5sWgy-6FvefehZ4GpUH81"
YOUTUBE_CHANNEL_ID_12 = "PLD08F66DFAEB1464E"
YOUTUBE_CHANNEL_ID_13 = "PLMbL_ZwxO92nmwac7zlaVLz80WH53L0y9"
YOUTUBE_CHANNEL_ID_14 = "PLGYYJaZ8b8kkC-3ZNJudb9b2PErOz9Ac4"
YOUTUBE_CHANNEL_ID_15 = "PLhWfK-KPoeysBYbbk32jFoRsAIZ-iGc5s"
YOUTUBE_CHANNEL_ID_16 = "PLQJP5TbQDoj0g1kCKtJ9ofimbM8z9_Tz5"
YOUTUBE_CHANNEL_ID_17 = "PLE1E0F9AC0DD9D8AC"
YOUTUBE_CHANNEL_ID_18 = "PL-c6AuUf1qcrO2_nHdKKgEjoONQ4erXWP"
YOUTUBE_CHANNEL_ID_19 = "PLBICMoNVHdfPVZOMCxO4OPfDgVG2AeyLD"
YOUTUBE_CHANNEL_ID_20 = "PL83560A3A7366350A"
YOUTUBE_CHANNEL_ID_21 = "PLuEa_oSflwHDda6XCwFpOBLjb2FL07Fjj"
YOUTUBE_CHANNEL_ID_22 = "PLg4VlNrloERNTJtefXxIRlo_4VE9VL_fk"
YOUTUBE_CHANNEL_ID_23 = "PL465AoFfS_960oI5Ugda26xW4-uKKagjJ"
YOUTUBE_CHANNEL_ID_24 = "PLOi-t4rTa1-wLdQYXYkteCABYLRlyhueX"
YOUTUBE_CHANNEL_ID_25 = "PLs3fd2-WUPUQd2IYQuW3JI7uk4GAcu8DO"
YOUTUBE_CHANNEL_ID_26 = "PLoShi5376u7KJfLrJcmeVm8CHy_thNLaG"
YOUTUBE_CHANNEL_ID_27 = "PLhXzjouqZvnDNJxDaGKUwYdaOzbLsYZPL"
YOUTUBE_CHANNEL_ID_28 = "PLHBBtqTT5UuOxgOxruWbKhfJBC0BqmiNI"
YOUTUBE_CHANNEL_ID_29 = "PLkJDZvJKJ_FR9NuNBhNyR9lGQCCKKXPpT"
YOUTUBE_CHANNEL_ID_30 = "PL19I9b_nuOoST_54oFY6cOBMEQt9ilVJw"
YOUTUBE_CHANNEL_ID_31 = "PLArmP8leXZx9AylO0tUFw-EKZf-S8EBDw"
YOUTUBE_CHANNEL_ID_32 = "PL5Jei4FryblUps-rHKhdA-ibrkeyJfjOB"
YOUTUBE_CHANNEL_ID_33 = "PLLJ7b60X2qTYcfRd40v3FMCH4tgC_GgTo"
YOUTUBE_CHANNEL_ID_34 = "PLGPIiT-x2q0PqfAanlsQFPxvvy8U3tZZR"
YOUTUBE_CHANNEL_ID_35 = "PLdfGT-_lpV-LGSkGXULDHU4_eQaER6e2i"
YOUTUBE_CHANNEL_ID_36 = "PLks3XupJarT9mLKvDer1nTvN50xpv5JzO"
YOUTUBE_CHANNEL_ID_37 = "PLfdFF0MOrKLH5UELOgs4ZkVgNbDJ8apWC"
YOUTUBE_CHANNEL_ID_38 = "PL8sTrZq3yadjzNMksys4-Duf_n0pUfVB_"
YOUTUBE_CHANNEL_ID_39 = "PLwxIC9DW0gX6ULCL-GlnJcZxjzU4DQfxi"
YOUTUBE_CHANNEL_ID_40 = "PL9F73C659BE7AAF42"
YOUTUBE_CHANNEL_ID_41 = "PLFda-J7qex_Nk392n7q-hpnSwHpTpczxl"
YOUTUBE_CHANNEL_ID_42 = "PLundnhqfpGl8PokLe-3dKO_WzR5Gd-Cfo"
YOUTUBE_CHANNEL_ID_43 = "PLPQqKws5phcIlGsuMlcFIYV70Yo16F5Cx"
YOUTUBE_CHANNEL_ID_44 = "PL_3_7HXYmrr5XxT6HBz6guYebPDuRYf30"
YOUTUBE_CHANNEL_ID_45 = "PL7VcXHxuqxrsd0jgnrcCN9Qxi10D2Rorn"
YOUTUBE_CHANNEL_ID_46 = "UCdTDOuDq_GTldgv4VoKXSsQ"
YOUTUBE_CHANNEL_ID_47 = "PLKFjLe98LJ1DTLWEY9nuYa_wYPl2J8JaI"
YOUTUBE_CHANNEL_ID_48 = "PLqBNuYkaLwnrwJo3Yg4UtdAc3bHWf48hg"
YOUTUBE_CHANNEL_ID_49 = "PLJox73Z61GYgyPExXVuFXEU3bqxu72BYI"
YOUTUBE_CHANNEL_ID_50 = "PLpDORv6XfWwbsEW4h9ylmiTuv_0Q9zPMg"
YOUTUBE_CHANNEL_ID_51 = "PLU5VunIS9DxXYLfoZvHJa7wqp99nn9XoX"
YOUTUBE_CHANNEL_ID_52 = "PLDkwLK38gGuDLJ4iCStCRlnCXMZ8XQaA7"
YOUTUBE_CHANNEL_ID_53 = "PLaEDwyCz4u8WXEPkgeMxxzktb96-1B47R"
YOUTUBE_CHANNEL_ID_54 = "PLmpUmLkpzRAiC5l38-UPwAreNa9Iyq3XO"
YOUTUBE_CHANNEL_ID_55 = "PLawCeCnmJKVeINCOBrCgL_8lnsXhVBD_B"
YOUTUBE_CHANNEL_ID_56 = "PLt6dddU5-rRT2cEkyVgSdetQyJ5OUt"
YOUTUBE_CHANNEL_ID_57 = "PLFcqmYiqU_tzT1IYO23HTUwA1YZr6rJqW"
YOUTUBE_CHANNEL_ID_58 = "PL8kpOtRr6c-xuWAW5LVOOU0b5gpy2MLYR"
YOUTUBE_CHANNEL_ID_59 = "LtRS3UiOVoAl8YCMys6jRZRxwNcBe6vtE"
YOUTUBE_CHANNEL_ID_60 = "PLrT7Oi-dj3IL6rpXaC45sSGgSKTKp37CJ"
YOUTUBE_CHANNEL_ID_61 = "PLhfTC0aqK0acYJsjcbRjVF0PVs4LOUAnT"
YOUTUBE_CHANNEL_ID_62 = "PLIj5C5a8Uh8HNGXXYbrIe_lWbp6ZN998y"
YOUTUBE_CHANNEL_ID_63 = "PLclGq4B3wC23Jz3OjOm2DVO7SqYwkkJSB"
YOUTUBE_CHANNEL_ID_64 = "PLrkhg5M7PyKImmwlPnoojJJKEZLIbpyTb"
YOUTUBE_CHANNEL_ID_65 = "PLMcb8xW9Uni2c38X_U9VMy7GqRxCWZZYk"
YOUTUBE_CHANNEL_ID_66 = "PL4TRvYtQ5aW9df1vrjW124-HGck_LqjmN"
YOUTUBE_CHANNEL_ID_67 = "PLZfNH2ObJMlzdTN4Oo5fGQavQxEHgnEsv"
YOUTUBE_CHANNEL_ID_68 = "PLvseuwFlK2wfufUIkdSiwGi_cstrw-99Q"
YOUTUBE_CHANNEL_ID_69 = "PLFqDRbNu_PahbZwmuc7EQriFhIHpTkNSk"
YOUTUBE_CHANNEL_ID_70 = "PLb7woqtLP_I0PzsJ8Gm4fGHhswy6IP2F2"
YOUTUBE_CHANNEL_ID_71 = "PLcjY_QX0-cvw0lW0OKF2j8YBoX-x3tbpm"
YOUTUBE_CHANNEL_ID_72 = "PLJi8eRGHlDx-k1T1XH1hTGKW1keiXONFi"
YOUTUBE_CHANNEL_ID_73 = "gottalentglobal"
YOUTUBE_CHANNEL_ID_74 = "PLDjjXsK_ohIuuh59Ypou0ZAmdQOx3iB3_"
YOUTUBE_CHANNEL_ID_75 = "PLBTpuIrurUG65RwzWO1DzuU3w81VS72NR"
YOUTUBE_CHANNEL_ID_76 = "PLwNk3tDc9N123yDUYYO0M13Iniij35e3f"
YOUTUBE_CHANNEL_ID_77 = "PLiOY8ArrvTR5XG9-QwE9FC4n2ZbDZWrzZ"
YOUTUBE_CHANNEL_ID_78 = "PL1JAyPrwR2eeNxVPUfddtONIEH8oRu2jL"
YOUTUBE_CHANNEL_ID_79 = "PLPdFJd8tDtfxpZEW8urqGDJk11xRg3wwo"
YOUTUBE_CHANNEL_ID_80 = "PL71sZc11FwRI3TeXO1-0oR4Tut5O1pnCf"
YOUTUBE_CHANNEL_ID_81 = "PLHqoPmrMrYa_9s3-OnZWH1ULBoCtv1jlC"
YOUTUBE_CHANNEL_ID_82 = "PL-C_fu0ZbbDJo6aCYk5jsrvFPmV7GHHTc"
YOUTUBE_CHANNEL_ID_83 = "PLJ4M-mZoGC3zmF_i44BL63tLdDJyggKOV"
YOUTUBE_CHANNEL_ID_84 = "PLF2Tn77Nr4z-eofQwd9_pGyvRAy2ZOk_a"
YOUTUBE_CHANNEL_ID_85 = "PLoz0IK63CMU0xySjwGMOLcs5tnrhOH9mR"
YOUTUBE_CHANNEL_ID_86 = "PLa4_J3cytwKZxZsyw2AyNYVCXI7bvpv8p"
YOUTUBE_CHANNEL_ID_87 = "PLYEgFwcLB1GvN6asBhCJaaUdiobgL6gjf"
YOUTUBE_CHANNEL_ID_88 = "PLhWfK-KPoeys-eDl1ZuduUcwe9ZhYfW6l"
YOUTUBE_CHANNEL_ID_89 = "PLwywog9TzJiaPqKPwpRJ7hkDrWRkIIS9t"
YOUTUBE_CHANNEL_ID_90 = "PLtKRkXRBRPqonoFBbqE_GJMuS79H0mGZD"
YOUTUBE_CHANNEL_ID_91 = "PL4vYX2eX2RikLRe8nZWSv50GEX_Z02NHS"
YOUTUBE_CHANNEL_ID_92 = "PLlC13rJIzDTWPq2qhcN_q9F5kV7SyT_fa"
YOUTUBE_CHANNEL_ID_93 = "PLmf5eZ-m874SXRvfzc6xlwscWVai8Ru_g"
YOUTUBE_CHANNEL_ID_94 = "PL-LRcs3PmKq53hfEr0eB-L_vg7EO80zIr"
YOUTUBE_CHANNEL_ID_95 = "PLd-PL2uxF2EazYRYk_dIuEJSxW55ewaUR"
YOUTUBE_CHANNEL_ID_96 = "PLEzqBt4Ql6AxurgctZnKDs0cD3ALPOZUl"
YOUTUBE_CHANNEL_ID_97 = "PL9CE9j1GUxNKLR03uTfiteuPCD1GXK03R"
YOUTUBE_CHANNEL_ID_98 = "PLAd3Q9am4uzL9hwIOfxPJO9d1nNgawvLt"
YOUTUBE_CHANNEL_ID_99 = "PL-LbyE8S6hrkiHi2KLqmR42XKtg9QeMOl"
YOUTUBE_CHANNEL_ID_100 = "PLFYGpNEy75dh_-d8VIySsucQfe_Q02Q8t"
YOUTUBE_CHANNEL_ID_101 = "PL91W4YQ2G59tInM8IE1Ef5fSy1Xf6N1Ys"
YOUTUBE_CHANNEL_ID_102 = "PLv-l11zT8jERpTu7zo0dWTtMc43c3yMul"
YOUTUBE_CHANNEL_ID_103 = "PL7vZAO9dxqpfmSv3jniNCdOE3jY4AV0A_"
YOUTUBE_CHANNEL_ID_104 = "PLyTHJhDpT2oBllm--y7uDeqqbFOIL0GCq"
YOUTUBE_CHANNEL_ID_105 = "PL3JTzVEWSDQCOalw2cCcJQpT5BvJbETD1"
YOUTUBE_CHANNEL_ID_106 = "PLUw0KFD5ibhyhUV4AD709gIPBQcvwC5Hs"
YOUTUBE_CHANNEL_ID_107 = "PL6MMPMTT1eIOjZUhILldpv6qVq2oCDk-D"
YOUTUBE_CHANNEL_ID_108 = "PL5S7bFME3GI5M3oJtbIaEUb_DA9a52UWd"
YOUTUBE_CHANNEL_ID_109 = "PLwPAyFpEmsF4DJx6wmgSaAZsPdEPOWdY7"
YOUTUBE_CHANNEL_ID_110 = "PL_gp7Hzok-wo9BFYmQclr1kcT6g-xGxSl"
YOUTUBE_CHANNEL_ID_111 = "PLayabSlVMF624r2_Fn1aS9ktpWfyBHq5B"
YOUTUBE_CHANNEL_ID_112 = "PLkP9zDfMfflu_TVYSuAEnKvzDmARks8YD"
YOUTUBE_CHANNEL_ID_113 = "PL9jcGx2_ahll11KqR9-CZYs1vzmfvXI2a"
YOUTUBE_CHANNEL_ID_114 = "PLb13VL0_sv1fhlIFITcDQCXWCcYzt1DKI"
YOUTUBE_CHANNEL_ID_115 = "PLKGCGGFII7wwp0YmI-UX1vHsa6sDdOlF5"
YOUTUBE_CHANNEL_ID_116 = "PLUVRD8yY4HqmVMJAwy9eoXiBu6nzI_CcD"
YOUTUBE_CHANNEL_ID_117 = "PL4pwczPGQTo9tdb0rrLm9FlUSDV_XJzLM"
YOUTUBE_CHANNEL_ID_118 = "PLAPwQ3SRrJOOPgMZjsAq0tkGR_tK_SIKu"
YOUTUBE_CHANNEL_ID_119 = "PL7Kn65uniKnNJzUeRbRManmhM-pL5judO"
YOUTUBE_CHANNEL_ID_120 = "PL35_QcjL3vlDj3BsQTpk-4JbnQWdeAbog"
YOUTUBE_CHANNEL_ID_121 = "PLETDuLSAxfVLCQTHVxQNik0vcBMfGVqMj"
YOUTUBE_CHANNEL_ID_122 = "PLI1nPBr0Zl_w5BZ1AF1N1Aom8zwcvRRh6"
YOUTUBE_CHANNEL_ID_123 = "PL2MpdH56omP66BmVe38-QRNGLhXljruYC"
YOUTUBE_CHANNEL_ID_124 = "PLoD2pmQfeSDoTL65mrwtryQ2FGcya2Ipa"
YOUTUBE_CHANNEL_ID_125 = "PLnpuTP0e-2hZ5ohYo8vuS7Eybp5eVgrma"
YOUTUBE_CHANNEL_ID_126 = "PL3AjfLMqFdODmrK8rs27tzw4aLCrQpfaG"
YOUTUBE_CHANNEL_ID_127 = "PLhyGpvoVedupP49JQk6uQikDWA5TMMKOa"
YOUTUBE_CHANNEL_ID_128 = "PLuvXfq8orEKcBN8jtnzVcc5GElQC7GaCv"
YOUTUBE_CHANNEL_ID_129 = "PLO7NN-0UlY0l2a44_M0dgsFGQy7o2K6WK"
YOUTUBE_CHANNEL_ID_130 = "PLKKbVdRlaxZG89jhMxuyAvAi-zy0rBkeR"
YOUTUBE_CHANNEL_ID_131 = "PLecYxHnp2I2KkmtyrXdPQ8HBanhXnPjv9"
YOUTUBE_CHANNEL_ID_132 = "PLnyUW4bk2hcjf9iuVpzRCQTjyh8684jX-"
YOUTUBE_CHANNEL_ID_133 = "PLAk14QzBmnOWe5jeDMEvfF2RucHnG26wa"
YOUTUBE_CHANNEL_ID_134 = "PLaYe3G4U2cSfa4Npycy_EAClCmzJ6nZ0R"
YOUTUBE_CHANNEL_ID_135 = "PLPixK-LMBPxW4RKgCu5_jz5nIewymTryn"
YOUTUBE_CHANNEL_ID_136 = "PLF8PeJV3VPawNFFn42HbZzoaplc9n9b4-"
YOUTUBE_CHANNEL_ID_137 = "PLdsKrK3VjwwwppqGVFd13-L28NGhG07I0"
YOUTUBE_CHANNEL_ID_138 = "UCoUZ2E-LWUflzwuJTQcXxng"
YOUTUBE_CHANNEL_ID_139 = "PLDwhSv1E88xnUjBRrywO9j-UOOzvZEU7_"
YOUTUBE_CHANNEL_ID_140 = "PLp75rWugbhBam6NVyFJd51fHLKCpVN2gS"
YOUTUBE_CHANNEL_ID_141 = "PLbTcrjtgHvyKugU5CGdlZG3Zo82pXntaO"
YOUTUBE_CHANNEL_ID_142 = "PLNzvSXHvZhxp6SzWF87UZjwZ0iAI4ZGMi"
YOUTUBE_CHANNEL_ID_143 = "PLTNxthcgPCLR9S0Fi5eyKqC2jURisxtLm"
YOUTUBE_CHANNEL_ID_144 = "PL_L-f4UlHGv9jgo4XONfhSJ0jQ26Amdcj"
YOUTUBE_CHANNEL_ID_145 = "PL6s26Yyh67fNq93afprPw1qclwE9E5sL-"
YOUTUBE_CHANNEL_ID_146 = "PL4gt2Trt0k7IWdpEsfCQ-WO8mIMTQ39kC"
YOUTUBE_CHANNEL_ID_147 = "PL7Cy3x8Os9AgsfSmPnsAJCPfLIZ_ueKIA"
YOUTUBE_CHANNEL_ID_148 = "PLKJdGYZHbzrrFiJiTCyyTBirBtHYxKxjU"
YOUTUBE_CHANNEL_ID_149 = "PLHXZB7UW6xEK6F5K4L1ej1jyPdTl_BTbV"
YOUTUBE_CHANNEL_ID_150 = "PLa777k7jxLtWNidJutUB9w3ZSpFze282Z"
YOUTUBE_CHANNEL_ID_151 = "PLQTOwyVgP-hwCOYw1U2cjjmFRee4_t5wc"
YOUTUBE_CHANNEL_ID_152 = "PLUDuFBgbdoFolkFj-mIIyShuILVUcCFo6"
YOUTUBE_CHANNEL_ID_153 = "PL6AiOyqcVvjXv_JIkU1GqiMbbKcKsk8b6"
YOUTUBE_CHANNEL_ID_154 = "PL7PdeMoD4z5dJyGYiEsmex6eWgw32xCGe"
YOUTUBE_CHANNEL_ID_155 = "PL4AGvH9loFXIXFcAZFrX1itDVr7kNrwdq"
YOUTUBE_CHANNEL_ID_156 = "PLOFCC8426NOtVBHRYR6AqWSW8mF3nFxK4"
YOUTUBE_CHANNEL_ID_157 = "PLiysj-EKbPPrhY-dZLyGVsg5ef_WKir4F"
YOUTUBE_CHANNEL_ID_158 = "youdontknowjacktvsho"
YOUTUBE_CHANNEL_ID_159 = "PLF8E562B65576BA59"

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
        title="GAMES SHOWS (topic)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="50's Game Shows",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="50's Game Shows (more)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="60's Game Shows",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="70's Game Shows",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="70's Game Shows (more)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )          

    plugintools.add_item( 
        #action="", 
        title="70's Game Shows (even more)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="80's Game Shows",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="80's Game Shows (more)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="90's Game Shows",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Classic Game Shows",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Classic TV Game Shows ('50s - '80s)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Game Show Pilots",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Game Shows misc.",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Old game shows",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Old game shows (more)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Rare Game Shows",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="TV Game Shows",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UK Game Shows",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="$64,000/$128,000 Question",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="1 vs. 100",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="101 Ways to Leave a Game Show",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="500 Questions",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="America's Got Talent",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="American Gladiators",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="American Idol",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="American Ninja Warrior",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Are You Smarter than a 5th Grader?",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Baggage",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BattleBots",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Battle of the Network Stars",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Beat The Clock",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Big Brother",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Blankety Blank",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Blind Date",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Blockbusters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bowling for Dollars",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Britain's Got Talent",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bullseye",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bumper Stumpers",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Card Sharks",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Cash Cab",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Catch 21",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Catchphrase",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Celebrity Bowling",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Celebrity Family Feud",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Celebrity Jeopardy!",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Celebrity Name Game",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Celebrity Squares",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Chain Reaction",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Concentration",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_51+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Countdown",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_52+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dale's Supermarket Sweep",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_53+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dancing with the Stars",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_54+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Deal or No Deal",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_55+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dirty Rotten Cheater",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_56+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dog Eat Dog",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_57+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Don't Forget the Lyrics!",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_58+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Don't Forget Your Toothbrush",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_59+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Double Dare",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_60+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dragons' Den",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_61+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Eggheads",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_62+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Family Feud",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_63+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Family Fortunes",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_64+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Family Game Night",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_65+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Fear Factor",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_66+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Fifteen to One",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_67+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Figure It Out",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_68+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Finders Keepers",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_69+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Friend or Foe?",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_70+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Going for Gold",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_71+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Golden Balls",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_72+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Got Talent Global",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_73+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="High Rollers",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_74+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Hole in the Wall",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_75+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Hollywood Game Night",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_76+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Hollywood Squares",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_77+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="I've Got a Secret",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_78+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Idiotest",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_79+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ink Master",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_80+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="I Survived a Japanese Game Show",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_81+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Jeopardy!",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_82+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Jeopardy! College Championship",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_83+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Jeopardy! Teachers Tournament",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_84+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Jeopardy! Tournament of Champions",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_85+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )           

    plugintools.add_item( 
        #action="", 
        title="Legends of the Hidden Temple",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_86+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Let's Make a Deal",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_87+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Liars Club",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_88+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Lingo",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_89+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Little Big Shots",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_90+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Love Connection",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_91+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Make Me Laugh",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_92+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Man vs. Beast",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_93+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Match Game",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_94+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Million Dollar Password",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_95+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Minute To Win It",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_96+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Name That Tune",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_97+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Nick Arcade",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_98+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Nickelodeon Guts",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_99+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Now You See It",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_100+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Password",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_101+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Password Plus/Super Password",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_102+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Penn & Teller: Fool Us",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_103+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="People Are Funny",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_104+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )
    
    plugintools.add_item( 
        #action="", 
        title="Play Your Cards Right",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_105+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )
    
    plugintools.add_item( 
        #action="", 
        title="Pointless",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_106+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )
    
    plugintools.add_item( 
        #action="", 
        title="Press Your Luck",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_107+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Pyramid",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_108+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Queen for a Day",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_109+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Remote Control",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_110+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="RuPaul's Drag Race: Untucked",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_111+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Russian Roulette",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_112+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Sale of the Century",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_113+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Sasuke",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_114+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Scrabble",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_115+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Shark Tank",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_116+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Shop 'til You Drop",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_117+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Silent Library",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_118+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Sports Jeopardy!",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_119+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Strike It Lucky",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_120+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Supermarket Sweep",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_121+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Survivor",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_122+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tattletales",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_123+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Amazing Race",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_124+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The American Bible Challenge",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_125+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Apprentice",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_126+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Chase",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_127+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Crystal Maze",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_128+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Dating Game",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_129+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Generation Game",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_130+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )           

    plugintools.add_item( 
        #action="", 
        title="The Gong Show",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_131+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Million Pound Drop",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_132+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Moment of Truth",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_133+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Newlywed Game",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_134+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Price Is Right",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_135+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Singing Bee",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_136+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Voice",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_137+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Wall",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_138+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Think Fast",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_139+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tic-Tac-Dough",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_140+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="To Tell the Truth",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_141+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Trivia Trap",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_142+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Truth or Consequences",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_143+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Weakest Link",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_144+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Whammy!",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_145+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="What's My Line?",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_146+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="What Would You Do?",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_147+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Wheel of Fortune",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_148+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Who Do You Trust?",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_149+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )
    
    plugintools.add_item( 
        #action="", 
        title="Whose Line Is It Anyway?",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_150+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )
    
    plugintools.add_item( 
        #action="", 
        title="Who Wants to Be a Millionaire?",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_151+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )
    
    plugintools.add_item( 
        #action="", 
        title="Win, Lose or Draw",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_152+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Win Ben Stein's Money",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_153+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Wipeout",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_154+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Wizard Wars",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_155+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="You Bet Your Ass",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_156+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="You Bet Your Life",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_157+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="You Don't Know Jack",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_158+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )   

    plugintools.add_item( 
        #action="", 
        title="You Don't Say!",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_159+"/",
        thumbnail="http://clipartix.com/wp-content/uploads/2017/04/Television-retro-tv-clipart.png",
        folder=True )  		
run()
