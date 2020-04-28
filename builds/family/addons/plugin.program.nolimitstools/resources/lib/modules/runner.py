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
import xbmc,xbmcgui,os,sys

REPO     =  xbmc.translatePath(os.path.join('special://home/addons','repository.echo'))
dialog = xbmcgui.Dialog()
ADDONTITLE="[COLOR yellowgreen]ECHO[/COLOR] [COLOR white]Wizard[/COLOR]"

def check():

	#if not os.path.exists(REPO):
	#	dialog.ok(ADDONTITLE, 'The ECHO Repository is not installed','It is a requirement of the ECHO Wizard to have the repo installed.','[COLOR dodgerblue][B]Please install the ECHO Repo from [/COLOR][COLOR red]http://echocoder.com/repo[/B][/COLOR]')
	#	sys.exit(0)