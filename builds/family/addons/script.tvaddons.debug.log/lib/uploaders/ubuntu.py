"""
    TVAddons Log Uploader Script
    Copyright (C) 2016 tknorris

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
import urllib
import re
import uploader
from uploader import UploaderError
from .. import log_utils

try:
    from urllib.request import urlopen, Request, build_opener, install_opener, HTTPErrorProcessor # python 3.x
except ImportError:
    from urllib2 import urlopen, Request, build_opener, install_opener, HTTPErrorProcessor  # python 2.x

BASE_URL = 'https://paste.ubuntu.com'
USER_AGENT = "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"


class NoRedirection(HTTPErrorProcessor):
    def http_response(self, request, response):
        log_utils.log('Stopping Redirect', log_utils.LOGDEBUG)
        return response
 
    https_response = http_response
     

class UbuntuUploader(uploader.Uploader):
    name = 'ubuntu'

    def upload_log(self, log, name=None):
        data = {'content': log, 'expiration': 'week','syntax': 'text', 'poster': 'tvaddons.co'}
        headers = {'User-Agent': USER_AGENT}
        # req = urllib2.Request(BASE_URL, data=urllib.urlencode(data), headers=headers)
        req = Request(BASE_URL, data=urllib.urlencode(data), headers=headers)
        try:
            # opener = urllib2.build_opener(NoRedirection)
            opener = build_opener(NoRedirection)
            install_opener(opener)
            res = urlopen(req)
            if res.getcode() == 302:
                paste_url = res.info().getheader('location')
                if re.match('%s/[A-Za-z0-9]+' % (BASE_URL), paste_url):
                    return paste_url
                else:
                    raise UploaderError('Unexcepted url from ubuntu: %s' % (paste_url))
            else:
                raise UploaderError('Unexcepted response from ubuntu: %s' % (res.getcode()), log_utils.LOGWARNING)
        except Exception as e:
            raise UploaderError(e)
            
    def send_email(self, email, results):
        return None
