"""
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmc,xbmcgui,base64,sys,re
import urllib2,urllib

def Beast_Install(redo=False):
	
	#This list of builds requires autherisa
	if redo == False:
		choice = xbmcgui.Dialog().yesno("The Beast", "You are required to login to install builds from The Beast!", "Would you like to enter in your information?", "Visit http://thebeast1.com to sign up!", yeslabel="Enter Details", nolabel="No Cancel")
	else: choice = 1

	if choice == 1:
		xbmcgui.Dialog().ok('[B][COLOR red]IMPORTANT[/B][/COLOR]','[COLOR white]After registration, you MUST [B][COLOR green]LOG IN[/B][/COLOR] and scroll down to [B][COLOR red]VERIFY EMAIL[/B][/COLOR][/COLOR].', '[COLOR white]If you do not verify your email via the website, the build will not download.[/COLOR]')
		username    = _get_keyboard( heading="Enter Your Login Email" )
		password    = _get_keyboard( heading="Enter Your Password" )
	else:
		sys.exit()

	url = 'http://thebeast1.com/signup2/check.php?email=' + username + '&pass=' + password

	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', base64.b64decode(b'UmVwbGljYW50V2l6YXJkLzEuMC4w'))
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
	except: 
		xbmcgui.Dialog().ok("The Beast","[B][COLOR red]IMPORTANT INFORMATION:[/B][/COLOR]", "[COLOR orange]There was an error connecting to the authentication server. Please try again later![/COLOR]")
		sys.exit(0)

	try:
		total = re.compile('install="(.+?)"').findall(link)[0]
	except: total = "0"

	if str(total) != '1':
 		if xbmcgui.Dialog().yesno('Authentication Failure', 'Please signup here: http://thebeast1.com', 'Then Re-Enter the details', yeslabel="Re-Enter Details", nolabel="No Cancel"):
			Beast_Install(True)
		else:
			sys.exit()
	else:
		xbmcgui.Dialog().ok("The Beast","[B][COLOR red]IMPORTANT INFORMATION:[/B][/COLOR]", "[COLOR orange]The login credentials will expire 12 hours after activation![/COLOR]")

def Endless_Install(redo=False):
	
	#This list of builds requires autherisa
	if redo == False:
		choice = xbmcgui.Dialog().yesno("EndlessFlix", "You are required to login to install builds from EndlessFlix!", "Would you like to enter in your information?", "Visit http://ww.endlessflix.co.uk/members to sign up!", yeslabel="Enter Details", nolabel="No Cancel")
	else: choice = 1

	if choice == 1:
		xbmcgui.Dialog().ok('[B][COLOR red]IMPORTANT[/B][/COLOR]','[COLOR white]After registration, you MUST [B][COLOR green]LOG IN[/B][/COLOR] and scroll down to [B][COLOR red]VERIFY EMAIL[/B][/COLOR][/COLOR].', '[COLOR white]If you do not verify your email via the website, the build will not download.[/COLOR]')
		username    = _get_keyboard( heading="Enter Your Login Email" )
		password    = _get_keyboard( heading="Enter Your Password" )
	else:
		sys.exit()

	url = 'http://endlessflix.co.uk/members/check.php?email=' + username + '&pass=' + password

	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', base64.b64decode(b'UmVwbGljYW50V2l6YXJkLzEuMC4w'))
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
	except: 
		xbmcgui.Dialog().ok("Endlessflix","[B][COLOR red]IMPORTANT INFORMATION:[/B][/COLOR]", "[COLOR orange]There was an error connecting to the authentication server. Please try again later![/COLOR]")
		sys.exit(0)

	try:
		total = re.compile('install="(.+?)"').findall(link)[0]
	except: total = "0"

	if str(total) != '1':
 		if xbmcgui.Dialog().yesno('Authentication Failure', 'Please signup here: http://www.endlessflix.co.uk/members', 'Then Re-Enter the details', yeslabel="Re-Enter Details", nolabel="No Cancel"):
			Endless_Install(True)
		else:
			sys.exit()
	else:
		xbmcgui.Dialog().ok("Endlessflix","[B][COLOR red]IMPORTANT INFORMATION:[/B][/COLOR]", "[COLOR orange]The login credentials will expire 24 hours after activation![/COLOR]")

def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default