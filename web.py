from urllib import *
from urllib2 import *
import cookielib
import re

class Web():
	profile_id = "1320147380"
	client_id = "9119878932724a62af94b0725cd415f7"
	client_secret = "a8e0ad3201bc496187049e194c18614e"
	redirect_uri = "http://neopixel.org"
	get_token_url = "https://api.instagram.com/oauth/authorize/?client_id="+client_id+"&redirect_uri="+redirect_uri+"&response_type=token"
	token = ""

	def setToken(self, newToken):
		Web.token = newToken

	def myProfile(self):
		query = "https://api.instagram.com/v1/users/1320147380?access_token="+Web.token
		response = urlopen(query)
		the_page = response.read()

		profile = {}
		tmatch = re.search(r'"username":"(.*?)",', the_page)
		if tmatch:
			profile['username'] = tmatch.group(1)
		tmatch = re.search(r'"bio":"(.*?)",', the_page)
		if tmatch:
			profile['bio'] = tmatch.group(1)
		tmatch = re.search(r'"website":"(.*?)",', the_page)
		if tmatch:
			profile['website'] = tmatch.group(1)
		tmatch = re.search(r'"profile_picture":"(.*?)",', the_page)
		if tmatch:
			profile['profile_picture'] = tmatch.group(1)

		return profile


