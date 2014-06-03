import urllib
from urllib2 import *
import re
import os

class Web():
    profile_id = "1320147380"
    client_id = "b4a37965871b48f79e5365fa097f8e24"
    client_secret = "3f0f335f1cf648a7b0de9ecbbb55941b"
    redirect_uri = "http://neopixel.org"
    get_token_url = "https://api.instagram.com/oauth/authorize/?client_id="+client_id+"&redirect_uri="+redirect_uri+"&response_type=token"
    # token = ""
    token = "1320147380.b4a3796.86fc6de63606444e9e34e795a6793606"   

    """******** Funcion: setToken **************
    Descripcion: Guarda un nuevo token para el acceso
    Parametros:
    newToken string
    Retorno: void
    ***********************************************************************************************************************"""
    def setToken(self, newToken):
        Web.token = newToken

    """******** Funcion: profile **************
    Descripcion: consulta por un perfil y sus fotos recientes
    Parametros:
    profile_id entero
    Retorno: profile arreglo de datos los datos
    ***********************************************************************************************************************"""
    def profile(self, profile_id):
        query = "https://api.instagram.com/v1/users/"+profile_id+"?access_token="+Web.token
        try:
            response = urlopen(query)
            the_page = response.read()
        except HTTPError:
            print "HTTP Error 400: BAD REQUEST (posible private)"
            print 'error_message: you cannot view this resource'
            return 0

        profile = {}
        profile["profile_id"] = profile_id
        tmatch = re.search(r'"username":"(.*?)",', the_page)
        
        profile['username'] = tmatch.group(1)
        tmatch = re.search(r'"bio":"(.*?)",', the_page)
        
        profile['bio'] = tmatch.group(1)
        tmatch = re.search(r'"website":"(.*?)",', the_page)
        
        profile['website'] = tmatch.group(1).replace('\\','')
        tmatch = re.search(r'"profile_picture":"(.*?)",', the_page)
        
        image = tmatch.group(1).replace('\\','')
        imagecode = "temp/"+image[40:]
        profile['profile_picture'] = image
        profile['picture_file'] = imagecode

        if not os.path.exists("temp/"):
            os.makedirs("temp/")

        if not os.path.exists(imagecode):
            f = open(imagecode,'wb')
            f.write(urllib.urlopen(image).read())
            f.close()

        query = "https://api.instagram.com/v1/users/"+profile_id+"/media/recent?count=20&access_token="+Web.token
        response = urlopen(query)
        the_page = response.read()
        profile['images'] = []
        tmatch1 = re.findall(r'"thumbnail":{"url":"(.*?)"', the_page)
        tmatch2 = re.findall(r'"caption":(.*?),(.*?),', the_page)
        if len(tmatch1) > 0:
            for x in xrange(0,len(tmatch1)):
                image = tmatch1[x].replace('\\','')
                imagecode = "temp/"+re.search(r"http://(.*?)/(.*?)@", image+'@').group(2).replace("/", "-")
                
                if not os.path.exists(imagecode):
                    f = open(imagecode,'wb')
                    f.write(urllib.urlopen(image).read())
                    f.close()
                
                if tmatch2[x][0] == 'null':
                    profile['images'].append((image, imagecode, 'No caption'))
                else:
                    try:
                        caption = re.search(r'"text":"(.*?)"', tmatch2[x][1])
                        caption = caption.group(1).replace('\\','')
                        profile['images'].append([image, imagecode, caption])
                    except Exception, e:
                        continue

        
        if profile_id == self.profile_id:
            profile['following'] = 2
        else:
            query = "https://api.instagram.com//v1/users/"+profile_id+"/relationship?access_token="+Web.token
            response = urlopen(query)
            the_page = response.read()
            
            regex = r'"data":{"outgoing_status":"(.*?)","target_user_is_private":(.*?),"incoming_status":"(.*?)"}'
            match = re.search(regex, the_page)
            if match.group(1) == 'follows':
                profile['following'] = 1
            else:
                profile['following'] = 0
                
        return profile

    """******** Funcion: search **************
    Descripcion: busca un string en instagram
    Parametros:
    string string
    Retorno: profiles arreglo de todos los perfiles encontrados
    ***********************************************************************************************************************"""
    def search(self, string):
        string = string.replace(" ", "%20")
        query = "https://api.instagram.com/v1/users/search?q="+string+"&count=20&access_token="+Web.token
        response = urlopen(query)
        the_page = response.read()
        regex = r'"username":"(.*?)","bio":"(.*?)","website":"(.*?)","profile_picture":"(.*?)","full_name":"(.*?)","id":"(.*?)"'
        tmatch = re.findall(regex, the_page)
        profiles = []
        for x in xrange(0,len(tmatch)):
                profile = tmatch[x]
                image = profile[3].replace('\\','')
                imagecode = "temp/"+image[40:].replace("/", "-")

                if not os.path.exists("temp/"):
                    os.makedirs("temp/")

                if not os.path.exists(imagecode):
                    f = open(imagecode,'wb')
                    f.write(urllib.urlopen(image).read())
                    f.close()
                                    
                profiles.append((profile[0],profile[1],profile[2],imagecode,profile[4],profile[5]))
                
        return profiles

    """******** Funcion: follow **************
    Descripcion: hace follow o unfollow segun el parametro dado
    follow entero
    profile_id entero
    Retorno: void
    ***********************************************************************************************************************"""
    def follow(self, follow, profile_id):
        url = 'https://api.instagram.com/v1/users/'+profile_id+'/relationship?access_token='+Web.token

        if follow == 1:
            value = {'action':'follow'}
        else:
            value = {'action':'unfollow'}

        data = urllib.urlencode(value)
        response = urllib.urlopen(url, data)
        the_page = response.read()

    """******** Funcion: feed **************
    Descripcion: consulta por el feed del perfil
    Retorno: feed arreglo de las fotos recientes
    ***********************************************************************************************************************"""
    def feed(self):
        query = "https://api.instagram.com/v1/users/self/feed?count=50&access_token="+Web.token
        response = urlopen(query)
        the_page = response.read()
        feed = []
        tmatch = re.findall(r'"thumbnail":{"url":"(.*?)",[^@]+,"caption":(.*?),"from":{"username":"(.*?)"', the_page)
        if len(tmatch) > 0:
            for x in xrange(0,len(tmatch)):
                image = tmatch[x][0].replace('\\','')
                imagecode = "temp/"+re.search(r"http://(.*?)/(.*?)@", image+'@').group(2).replace("/", "-")

                username = tmatch[x][2]
                
                if not os.path.exists(imagecode):
                    f = open(imagecode,'wb')
                    f.write(urllib.urlopen(image).read())
                    f.close()
                
                if tmatch[x][1] == 'null':
                    feed.append([username, image, imagecode, 'No caption'])
                else:
                    try:
                        caption = re.search(r'"text":"(.*?)"', tmatch[x][1])
                        caption = caption.group(1).replace('\\','')
                        feed.append([username, image, imagecode, caption])
                    except Exception, e:
                        continue
        return feed


