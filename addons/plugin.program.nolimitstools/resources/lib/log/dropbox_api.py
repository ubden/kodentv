import re
import urllib
import urllib2
import json
import log_utils

USER_AGENT = 'TVA Dropbox API'
API_HOST = 'api.dropboxapi.com'
WEB_HOST = "www.dropbox.com"
API_CONTENT_HOST = 'content.dropboxapi.com'
API_NOTIFICATION_HOST = 'notify.dropboxapi.com'
API_VERSION = 1
_OAUTH2_ACCESS_TOKEN_PATTERN = re.compile(r'\A[-_~/A-Za-z0-9\.\+]+=*\Z')  # From the "Bearer" token spec, RFC 6750.

class ErrorResponse(Exception):
    def __init__(self, e):
        self.status = e.code
        self.reason = e.reason

class Client(object):
    def _build_url(self, host, target, params=None):
        if isinstance(target, unicode):
            target = target.encode('utf-8')

        url = 'https://%s%s' % (host, target)
        if params:
            url += '?' + params_to_urlencoded(params)
        return url
    
    def _call_dropbox(self, target, params=None, data=None, headers=None, method=None,
                      auth=True, content_server=False, notification_server=False):
        if params is None: params = {}
        if headers is None: headers = {}

        if content_server:
            host = API_CONTENT_HOST
        elif notification_server:
            host = API_NOTIFICATION_HOST
        else:
            host = API_HOST
            
        url = self._build_url(host, target, params)
        headers['User-Agent'] = USER_AGENT
        if auth:
            headers['Authorization'] = 'Bearer %s' % (self.token)

        if data:
            if 'Content-Type' not in headers:
                headers['Content-Type'] = 'application/octet-stream'
                
            if isinstance(data, basestring):
                data = data
            else:
                data = urllib.urlencode(data, True)

            if method == 'PUT':
                headers['Content-Length'] = len(data)

        try:
            log_data = len(data) if len(data) > 255 else data
            log_utils.log('url: |%s| method: |%s| data: |%s| headers: |%s|' % (url, method, log_data, headers))
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
    
class DropboxClient(Client):
    def __init__(self, oauth2_access_token):
        self.token = oauth2_access_token
    
    def upload_file(self, full_path, file_obj, overwrite=True, autorename=False, mute=False):
        url = '/2/files/upload'
        mode = 'overwrite' if overwrite else 'add'
        db_args = {'path': format_path(full_path), 'mode': mode, 'autorename': autorename, 'mute': mute}
        headers = {'Dropbox-API-Arg': json.dumps(db_args)}

        if hasattr(file_obj, 'read'):
            data = file_obj.read()
        else:
            data = file_obj
        
        return self._call_dropbox(url, data=data, headers=headers, content_server=True)

    def share(self, path, short_url=True):
        url = '/2/sharing/create_shared_link'
        data = {'path': path, 'short_url': short_url}
        headers = {'Content-Type': 'application/json'}
        return self._call_dropbox(url, data=json.dumps(data), headers=headers)

class DropboxOAuth2FlowBase(Client):

    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def _get_authorize_url(self, redirect_uri, state):
        params = {'response_type': 'code', 'client_id': self.consumer_key}
        if redirect_uri is not None:
            params['redirect_uri'] = redirect_uri
        if state is not None:
            params['state'] = state

        return self._build_url(WEB_HOST, '/oauth2/authorize', params)

    def _finish(self, code, redirect_uri):
        url = '/oauth2/token'
        data = {'grant_type': 'authorization_code', 'code': code,
                'client_id': self.consumer_key, 'client_secret': self.consumer_secret}
        if redirect_uri is not None:
            data['redirect_uri'] = redirect_uri
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = self._call_dropbox(url, data=data, headers=headers, auth=False)
        return response["access_token"], response["uid"]

class DropboxOAuth2Flow(DropboxOAuth2FlowBase):
    """
    OAuth 2 authorization helper for apps that can't provide a redirect URI
    (such as the command-line example apps).

    Example::
        auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

        authorize_url = auth_flow.start()
        print "1. Go to: " + authorize_url
        print "2. Click \\"Allow\\" (you might have to log in first)."
        print "3. Copy the authorization code."
        auth_code = raw_input("Enter the authorization code here: ").strip()

        try:
            access_token, user_id = auth_flow.finish(auth_code)
        except ErrorResponse, e:
            print('Error: %s' % (e,))
            return

        c = DropboxClient(access_token)
    """

    def __init__(self, consumer_key, consumer_secret):
        """
        Construct an instance.

        Parameters
          consumer_key
            Your API app's "app key"
          consumer_secret
            Your API app's "app secret"
        """
        super(self.__class__, self).__init__(consumer_key, consumer_secret)

    def start(self):
        """
        Starts the OAuth 2 authorization process.

        Returns
            The URL for a page on Dropbox's website.  This page will let the user "approve"
            your app, which gives your app permission to access the user's Dropbox account.
            Tell the user to visit this URL and approve your app.
        """
        return self._get_authorize_url(None, None)

    def finish(self, code, redirect_uri=None):
        """
        If the user approves your app, they will be presented with an "authorization code".  Have
        the user copy/paste that authorization code into your app and then call this method to
        get an access token.

        Parameters
          code
            The authorization code shown to the user when they approved your app.

        Returns
            A pair of ``(access_token, user_id)``.  ``access_token`` is a string that
            can be passed to DropboxClient.  ``user_id`` is the Dropbox user ID (string) of the
            user that just approved your app.

        Raises
            The same exceptions as :meth:`DropboxOAuth2Flow.finish()`.
        """
        return self._finish(code, redirect_uri)


def params_to_urlencoded(params):
    """
    Returns a application/x-www-form-urlencoded 'str' representing the key/value pairs in 'params'.
    
    Keys are values are str()'d before calling urllib.urlencode, with the exception of unicode
    objects which are utf8-encoded.
    """
    def encode(o):
        if isinstance(o, unicode):
            return o.encode('utf8')
        else:
            return str(o)
    utf8_params = {}
    for k, v in params.iteritems():
        utf8_params[encode(k)] = encode(v)
    return urllib.urlencode(utf8_params)

def format_path(path):
    """Normalize path for use with the Dropbox API.

    This function turns multiple adjacent slashes into single
    slashes, then ensures that there's a leading slash but
    not a trailing slash.
    """
    if not path:
        return path

    path = re.sub(r'/+', '/', path)

    if path == '/':
        return (u"" if isinstance(path, unicode) else "")
    else:
        return '/' + path.strip('/')
