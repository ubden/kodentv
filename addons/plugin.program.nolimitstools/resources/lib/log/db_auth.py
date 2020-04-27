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
import urllib2
import json
import log_utils
import uuid

AUTH_URL = 'https://logs.tvaddons.ag/db_auth.php'

class ErrorResponse(Exception):
    def __init__(self, e):
        self.status = e.code
        self.reason = e.reason

class DbAuth(object):
    def __init__(self, auth_url):
        self.session_id = str(uuid.uuid4())
        self.auth_url = auth_url
        
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.remove_session()

    def start_session(self):
        data = {'action': 'start_session', 'session_id': self.session_id, 'auth_url': self.auth_url}
        result = self.__http_request(data=data)
        if result.get('success'):
            return result['pin'], result['redirect_uri']
        
    def remove_session(self):
        data = {'action': 'remove_session', 'session_id': self.session_id}
        return self.__http_request(data=data)
        
    def get_code(self, pin):
        data = {'action': 'get_code', 'session_id': self.session_id, 'pin': pin}
        return self.__http_request(data=data)

    def __http_request(self, params=None, data=None, headers=None, method=None):
        if params is None: params = {}
        if headers is None: headers = {}
        url = AUTH_URL

        if data:
            if isinstance(data, basestring):
                data = data
            else:
                data = urllib.urlencode(data, True)

            if method == 'PUT':
                headers['Content-Length'] = len(data)

        try:
            log_utils.log('url: |%s| method: |%s| data: |%s| headers: |%s|' % (url, method, data, headers))
            request = urllib2.Request(url, data=data, headers=headers)
            if method is not None: request.get_method = lambda: method.upper()
            response = urllib2.urlopen(request)
            result = ''
            while True:
                data = response.read()
                if not data: break
                result += data
        except urllib2.HTTPError as e:
            raise ErrorResponse(e)
        
        return json.loads(result)
