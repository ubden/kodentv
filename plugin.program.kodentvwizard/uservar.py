import os, xbmc, xbmcaddon

#########################################################
### Global Variables ####################################
#########################################################
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')
#########################################################

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = 'Supreme Builds Wizard'
BUILDERNAME    = 'KodiSkills'
EXCLUDES       = [ADDON_ID, 'repository.supremebuilds']
# Enable/Disable the text file caching with 'Yes' or 'No' and age being how often it rechecks in minutes
CACHETEXT      = 'Yes'
CACHEAGE       = 30
# Text File with build info in it.
#BUILDFILE      = 'https://wizard.supremebuilds.com/texts/builds.txt'
BUILDFILE      = 'https://ubden.github.io/kodentv/kur.txt'
# How often you would like it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 2
# Text File with apk info in it.  Leave as 'http://' to ignore
APKFILE        = 'https://wizard.supremebuilds.com/texts/apks.txt'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE   = 'YouTube Videos'
YOUTUBEFILE    = 'https://wizard.supremebuilds.com/texts/youtube.txt'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'https://wizard.supremebuilds.com/texts/addons.txt'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'https://wizard.supremebuilds.com/texts/advanced.txt'
#########################################################

#########################################################
### Theming Menu Items ##################################
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'http://aftermathwizard.net/repo/wizard/settings.png'
# Leave as http:// for default icon
ICONBUILDS     = 'https://wizard.supremebuilds.com/images/supremebuilds.png'
ICONMAINT      = 'https://wizard.supremebuilds.com/images/maintenance.png'
ICONSPEED      = 'https://wizard.supremebuilds.com/images/speed.png'
ICONAPK        = 'https://wizard.supremebuilds.com/images/apkinstaller.png'
ICONADDONS     = 'https://wizard.supremebuilds.com/images/addoninstaller.png'
ICONYOUTUBE    = 'https://wizard.supremebuilds.com/images/youtube.png'
ICONSAVE       = 'https://wizard.supremebuilds.com/images/savedata.png'
ICONTRAKT      = 'https://wizard.supremebuilds.com/images/trakt.png'
ICONREAL       = 'https://wizard.supremebuilds.com/images/realdebrid.png'
ICONLOGIN      = 'https://wizard.supremebuilds.com/images/login.png'
ICONCONTACT    = 'https://wizard.supremebuilds.com/images/contactus.png'
ICONSETTINGS   = 'https://wizard.supremebuilds.com/images/settings.png'
# Hide the section seperators 'Yes' or 'No'
HIDESPACERS    = 'No'
# Character used in seperator
SPACER         = '='

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'firebrick'
COLOR2         = 'ghostwhite'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR1+'][B][I]([COLOR '+COLOR2+']Supreme Builds[/COLOR])[/I][/B][/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Current Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'No'
# You can add \n to do line breaks
CONTACT        = 'Thank you for choosing Supreme Builds.\n\nContact us on facebook at https://facebook.com/groups/supremebuilds'
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = 'https://wizard.supremebuilds.com/images/contactus.png'
CONTACTFANART  = 'https://wizard.supremebuilds.com/images/sbforumfanart.jpg'
#########################################################

#########################################################
### Auto Update                   #######################
###        For Those With No Repo #######################
#########################################################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'No'
# Url to wizard version
WIZARDFILE     = BUILDFILE
#########################################################

#########################################################
### Auto Install                 ########################
###        Repo If Not Installed ########################
#########################################################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'No'
# Addon ID for the repository
REPOID         = 'repository.supremebuilds'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://raw.githubusercontent.com/kodiskills/supremebuildsrepo/master/repository.supremebuilds/addons.xml'
# Url to folder zip is located in
REPOZIPURL     = 'https://github.com/kodiskills/supremebuildsrepo/raw/master/zips'
#########################################################

#########################################################
### Notification Window #################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'Yes'
# Url to notification file
NOTIFICATION   = 'https://wizard.supremebuilds.com/texts/notify.txt'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Image'
# Font size of header
FONTHEADER     = 'Font14'
HEADERMESSAGE  = '[B][COLOR firebrick]Supreme Builds[/COLOR][/B] Wizard'
# url to image if using Image 424x180
HEADERIMAGE    = 'https://wizard.supremebuilds.com/images/sbnews.png'
# Font for Notification Window
FONTSETTINGS   = 'Font13'
# Background for Notification Window
BACKGROUND     = 'https://wizard.supremebuilds.com/images/sbsplash.jpg'
#########################################################
