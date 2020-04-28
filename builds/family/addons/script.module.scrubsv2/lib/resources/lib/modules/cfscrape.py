# -*- coding: utf-8 -*-

import re
import os
import ast
import ssl
import copy
import time
import random
import operator as op
from collections import OrderedDict
from requests.sessions import Session
from requests.adapters import HTTPAdapter
from requests.compat import urlparse, urlunparse
from requests.exceptions import RequestException
try:
    from urllib3.util.ssl_ import create_urllib3_context, DEFAULT_CIPHERS
except:
    from requests.packages.urllib3.util.ssl_ import create_urllib3_context, DEFAULT_CIPHERS


operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor, ast.USub: op.neg}


__version__ = "2.0.8"


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"
]


DEFAULT_USER_AGENT = random.choice(USER_AGENTS)


DEFAULT_HEADERS = OrderedDict(
    (
        ("Host", None),
        ("Connection", "keep-alive"),
        ("Upgrade-Insecure-Requests", "1"),
        ("User-Agent", DEFAULT_USER_AGENT),
        (
            "Accept",
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        ),
        ("Accept-Language", "en-US,en;q=0.9"),
        ("Accept-Encoding", "gzip, deflate"),
    )
)


BUG_REPORT = """\
Cloudflare may have changed their technique, or there may be a bug in the script.
"""


ANSWER_ACCEPT_ERROR = """\
The challenge answer was not properly accepted by Cloudflare.
"""


DEFAULT_CIPHERS += ":!ECDHE+SHA:!AES128-SHA:!AESCCM:!DHE:!ARIA"


class CloudflareAdapter(HTTPAdapter):
    def get_connection(self, *args, **kwargs):
        conn = super(CloudflareAdapter, self).get_connection(*args, **kwargs)
        if conn.conn_kw.get("ssl_context"):
            conn.conn_kw["ssl_context"].set_ciphers(DEFAULT_CIPHERS)
        else:
            context = create_urllib3_context(ciphers=DEFAULT_CIPHERS)
            conn.conn_kw["ssl_context"] = context
        return conn


class CloudflareError(RequestException):
    pass


class CloudflareScraper(Session):
    def __init__(self, *args, **kwargs):
        self.tries = 0
        self.prev_resp = None
        self.delay = kwargs.pop("delay", None)
        headers = OrderedDict(kwargs.pop("headers", DEFAULT_HEADERS))
        headers.setdefault("User-Agent", DEFAULT_USER_AGENT)
        super(CloudflareScraper, self).__init__(*args, **kwargs)
        self.headers = headers
        self.mount("https://", CloudflareAdapter())


    @staticmethod
    def is_cloudflare_iuam_challenge(resp, allow_empty_body=False):
        return (resp.status_code in (503, 429) and resp.headers.get("Server", "").startswith("cloudflare") and (allow_empty_body or (b"jschl_vc" in resp.content and b"jschl_answer" in resp.content)))


    @staticmethod
    def is_cloudflare_captcha_challenge(resp):
        return (resp.status_code == 403 and resp.headers.get("Server", "").startswith("cloudflare") and b"/cdn-cgi/l/chk_captcha" in resp.content)


    def request(self, method, url, *args, **kwargs):
        resp = super(CloudflareScraper, self).request(method, url, *args, **kwargs)
        if self.is_cloudflare_captcha_challenge(resp):
            self.raise_captcha_error()
        self.prev_resp = resp
        if self.is_cloudflare_iuam_challenge(resp):
            if self.tries >= 3:
                exception_message = 'Failed to solve Cloudflare challenge!'
                if os.getenv('CI') == 'true':
                    exception_message += '\n' + resp.text
                raise Exception(exception_message)
            resp = self.solve_cf_challenge(resp, **kwargs)
        return resp


    def cloudflare_is_bypassed(self, url, resp=None):
        cookie_domain = ".{}".format(urlparse(url).netloc)
        return (self.cookies.get("cf_clearance", None, domain=cookie_domain) or (resp and resp.cookies.get("cf_clearance", None, domain=cookie_domain)))


    def raise_captcha_error(self):
        exception_message = 'Cloudflare returned captcha!'
        if self.prev_resp is not None and os.getenv('CI') == 'true':
            exception_message += '\n' + self.prev_resp.text
        raise Exception(exception_message)


    def solve_cf_challenge(self, resp, **original_kwargs):
        self.tries += 1
        start_time = time.time()
        body = resp.text
        parsed_url = urlparse(resp.url)
        domain = parsed_url.netloc
        submit_url = "%s://%s/cdn-cgi/l/chk_jschl" % (parsed_url.scheme, domain)
        cloudflare_kwargs = copy.deepcopy(original_kwargs)
        headers = cloudflare_kwargs.setdefault("headers", {})
        headers["Referer"] = resp.url
        try:
            params = cloudflare_kwargs["params"] = OrderedDict(re.findall(r'name="(s|jschl_vc|pass)"(?: [^<>]*)? value="(.+?)"', body))
            for k in ("jschl_vc", "pass"):
                if k not in params:
                    raise ValueError("%s is missing from challenge form" % k)
        except Exception as e:
            raise ValueError("Unable to parse Cloudflare anti-bot IUAM page: %s %s" % (e.message, BUG_REPORT))
        try:
            answer, delay = solve_challenge(body, domain)
        except:
            self.raise_captcha_error()
        params["jschl_answer"] = answer
        method = resp.request.method
        cloudflare_kwargs["allow_redirects"] = False
        if not self.delay:
            time.sleep(max(delay - (time.time() - start_time), 0))
        else:
            time.sleep(self.delay)
        redirect = self.request(method, submit_url, **cloudflare_kwargs)
        redirect_location = urlparse(redirect.headers["Location"])
        if not redirect_location.netloc:
            redirect_url = urlunparse(
                (
                    parsed_url.scheme,
                    domain,
                    redirect_location.path,
                    redirect_location.params,
                    redirect_location.query,
                    redirect_location.fragment,
                )
            )
            return self.request(method, redirect_url, **original_kwargs)
        return self.request(method, redirect.headers["Location"], **original_kwargs)


def eval_expr(expr):
    return eval_(ast.parse(expr, mode='eval').body)


def eval_(node):
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp):
        return operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)


def parseJSString(s):
    offset = 1 if s[0] == '+' else 0
    val = s.replace('!+[]', '1').replace('!![]', '1').replace('[]', '0')[offset:]
    val = val.replace('(+0', '(0').replace('(+1', '(1')
    if s[0] != '(':
        val = '({})'.format(val)
    val = re.findall(r'\((?:\d|\+|\-)*\)', val)
    val = ''.join([str(eval_expr(i)) for i in val])
    return int(val)


def solve_challenge(body, domain):
    delay = int(re.compile("\}, ([\d]+)\);", re.MULTILINE).findall(body)[0]) / 1000
    init = re.findall('setTimeout\(function\(\){\s*var.*?.*:(.*?)}', body)[-1]
    builder = re.findall(r"challenge-form\'\);\s*(.*)a.v", body)[0]
    try:
        challenge_element = re.findall(r'id="cf.*?>(.*?)</', body)[0]
    except:
        challenge_element = None
    if '/' in init:
        init = init.split('/')
        decryptVal = parseJSString(init[0]) / float(parseJSString(init[1]))
    else:
        decryptVal = parseJSString(init)
    lines = builder.split(';')
    char_code_at_sep = '"("+p+")")}'
    for line in lines:
        if len(line) > 0 and '=' in line:
            sections = line.split('=')
            if len(sections) < 3:
                if '/' in sections[1]:
                    subsecs = sections[1].split('/')
                    val_1 = parseJSString(subsecs[0])
                    if char_code_at_sep in subsecs[1]:
                        subsubsecs = re.findall(r"^(.*?)(.)\(function", subsecs[1])[0]
                        operand_1 = parseJSString(subsubsecs[0] + ')')
                        operand_2 = ord(domain[parseJSString(
                            subsecs[1][subsecs[1].find(char_code_at_sep) + len(char_code_at_sep):-2])])
                        val_2 = '%.16f%s%.16f' % (float(operand_1), subsubsecs[1], float(operand_2))
                        val_2 = eval_expr(val_2)
                    else:
                        val_2 = parseJSString(subsecs[1])
                    line_val = val_1 / float(val_2)
                elif len(sections) > 2 and 'atob' in sections[2]:
                    expr = re.findall((r"id=\"%s.*?>(.*?)</" % re.findall(r"k = '(.*?)'", body)[0]), body)[0]
                    if '/' in expr:
                        expr_parts = expr.split('/')
                        val_1 = parseJSString(expr_parts[0])
                        val_2 = parseJSString(expr_parts[1])
                        line_val = val_1 / float(val_2)
                    else:
                        line_val = parseJSString(expr)
                else:
                    if 'function' in sections[1]:
                        continue
                    line_val = parseJSString(sections[1])
            elif 'Element' in sections[2]:
                subsecs = challenge_element.split('/')
                val_1 = parseJSString(subsecs[0])
                if char_code_at_sep in subsecs[1]:
                    subsubsecs = re.findall(r"^(.*?)(.)\(function", subsecs[1])[0]
                    operand_1 = parseJSString(subsubsecs[0] + ')')
                    operand_2 = ord(domain[parseJSString(
                        subsecs[1][subsecs[1].find(char_code_at_sep) + len(char_code_at_sep):-2])])
                    val_2 = '%.16f%s%.16f' % (float(operand_1), subsubsecs[1], float(operand_2))
                    val_2 = eval_expr(val_2)
                else:
                    val_2 = parseJSString(subsecs[1])
                line_val = val_1 / float(val_2)
            decryptVal = '%.16f%s%.16f' % (float(decryptVal), sections[0][-1], float(line_val))
            decryptVal = eval_expr(decryptVal)
    if '+ t.length' in body:
        decryptVal += len(domain)
    if decryptVal % 1 == 0:
        return int(decryptVal), delay
    else:
        return float('%.10f' % decryptVal), delay


create_scraper = CloudflareScraper


