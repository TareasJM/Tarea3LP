from urllib import *
from urllib2 import *
import cookielib
import re

url = 'https://instagram.com/accounts/login/'

response = urlopen(url)
the_page = response.read()


tmatch = re.search(r'<input type="hidden" name="csrfmiddlewaretoken" value="(.*?)"/>', the_page)
if tmatch:
	login_id = tmatch.group(1)
	print login_id


headers = { 'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)' }
values = {'csrfmiddlewaretoken' : login_id, 'username' : 'ayudantia.lp.usm','password' : 'borquez2014' }
data = urlencode(values)
data = data.encode('utf-8')

cookies = cookielib.CookieJar()

opener = build_opener(
    HTTPRedirectHandler(),
    HTTPHandler(debuglevel=0),
    HTTPSHandler(debuglevel=0),
    HTTPCookieProcessor(cookies))

req = Request(url, data, headers)

response = urlopen(req)
the_page = response.read()

f = open('page.html', 'w')
f.write(the_page)



# client_id = "b4a37965871b48f79e5365fa097f8e24"
# client_secret = "3f0f335f1cf648a7b0de9ecbbb55941b"
# redirect_uri = "http://neopixel.org"
# get_token_url = "https://api.instagram.com/oauth/authorize/?client_id="+client_id+"&redirect_uri="+redirect_uri+"&response_type=code"

# response = urlopen(get_token_url)

# print response.geturl()