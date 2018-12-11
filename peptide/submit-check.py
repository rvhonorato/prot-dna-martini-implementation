import time
import urllib

def launch(name, file):
    # Ask user for username and password
    username = ""
    password = ""
    # HADDOCK file-upload interface URL
    url = 'http://milou.science.uu.nl/cgi/enmr/services/HADDOCK2.2/haddockserver-file.cgi'
    # Params used in the file-upload interface :
    params = urllib.urlencode({'runname': name, 'params': open(file).read(), 'username':username, 'password':password})
    # POST request with pepetide sequence as parameter
    f = urllib.urlopen(url , params)
    time.sleep(10)
    # Get results page informations
    result = f.read()
    print result
    return 0