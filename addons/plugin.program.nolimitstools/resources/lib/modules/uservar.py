import os, xbmc, xbmcaddon

#########################################################
### User Edit Variables #################################
#########################################################
ADDONTITLE     = "[COLOR aqua]No Limits[/COLOR] [COLOR white]Tools[/COLOR]"
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')  #'plugin.program.nolimitstools'
EXCLUDES       = [ADDON_ID]
# Text File with build info in it.
BUILDFILE      = 'http://'#'http://nolimitsbuilds.com/xmls/builds.txt'
# How often you would like it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 0
# Text File with APK info in it.
APKFILE        = 'http://'#'http://nolimitsbuilds.com/xmls/apks.txt'
# Text File with Youtube Videos URLs.  Leave as 'http://' to ignore
YOUTUBETITLE   = 'Reviews & Tutorials'
YOUTUBEFILE    = 'http://'#'http://nolimitsbuilds.com/xmls/youtubes.txt'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'http://'#'http://nolimitsbuilds.com/xmls/addons.txt'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'http://'

# Dont need to edit just here for icons stored locally
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################
# If you want to use locally stored icons then place them in the Resources/Art/
# folder of the Wizard then use os.path.join(ART, 'imagename.png')
# Do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'http://aftermathwizard.net/repo/wizard/settings.png'
# Leave as http:// for default icon
ICONBUILDS     = 'http://'#'http://nolimitsbuilds.com/images/Builds.jpg'
ICONMAINT      = 'http://'#'http://nolimitsbuilds.com/images/Maintenace.jpg'
ICONAPK        = 'http://'#'http://nolimitsbuilds.com/images/forks.jpg'
ICONADDONS     = 'http://'#'http://nolimitsbuilds.com/images/AddonInstall.jpg'
ICONYOUTUBE    = 'http://'#'http://nolimitsbuilds.com/images/REVTuts.jpg'
ICONSAVE       = 'http://'#'http://nolimitsbuilds.com/images/SaveAccount.jpg'
ICONTRAKT      = 'http://'#'http://nolimitsbuilds.com/images/trakt.jpg'
ICONREAL       = 'http://'#'http://nolimitsbuilds.com/images/rd.jpg'
ICONLOGIN      = 'http://'#'http://nolimitsbuilds.com/images/login.jpg'
ICONCONTACT    = 'http://'#'http://nolimitsbuilds.com/images/Support.jpg'
ICONSETTINGS   = 'http://'#'http://nolimitsbuilds.com/images/settings.jpg'
# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'No'
# Character used in seperator
SPACER         = '--'

# You can edit these however you want, just make sure that you have a %s in each of the
# THEMEs so it grabs the text from the menu item
COLOR1         = 'magenta'
COLOR2         = 'cyan'
# Primary Menu Items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR1+'][I][B]([COLOR '+COLOR2+']No Limits[/COLOR])[/B][/I][/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate Items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Current Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Chosen Build Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Chosen Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME6         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' don't hide
HIDECONTACT    = 'No'
# You can add \n to do line breaks
#CONTACT        = '[B][COLOR '+COLOR2+']The LG Wizard was built by the great KleptoKodi and modified by Teverz. You can find him at [COLOR '+COLOR1+']@K1ept0[/COLOR]. Thank you for choosing the [COLOR '+COLOR1+']Looking Glass[/COLOR] Team\'s Wizard!\r\n\r\nFor any questions, concerns, suggestions and/or requests contact me on Twitter at:  [COLOR '+COLOR1+']@TeverzMe[/COLOR][/B]'
CONTACT        = 'Follow Us At... \n \n \nYouTube.com/kodinolimits \n \nSnapchat.com/add/kodinolimits \n \nPaypal.me/kodinolimits '
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = 'http://'
CONTACTFANART  = xbmc.translatePath('special://home/addons/plugin.program.nolimitstools/resources/art/black.jpg')
#Images used for the Auto Advanced Settings window.
ADVANCEDFANART = xbmc.translatePath('special://home/addons/plugin.program.nolimitstools/resources/art/black.jpg')
#########################################################

#########################################################
### AUTO UPDATE #########################################
########## FOR THOSE WITH NO REPO #######################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'No'
# URL to wizard version
WIZARDFILE     = 'http://'#'http://nolimitsbuilds.com/xmls/builds.txt'
#########################################################

#########################################################
### AUTO INSTALL REPO ###################################
############### IF NOT INSTALLED ########################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'No'
# Addon ID for the repository
REPOID         = ''
# URL to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = ''
# URL to folder zip is located in
REPOZIPURL     = ''
#########################################################

#########################################################
### NOTIFICATION WINDOW #################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'No'
# URL to notification file
NOTIFICATION   = ''
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
HEADERMESSAGE  = '[B]No Limits Tools[/B]'
# URL to image if using Image 424x180
HEADERIMAGE    = ''
# Background for Notification Window
BACKGROUND     = ''
#########################################################