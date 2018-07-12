#!/usr/bin/python

#### Author: Mikael Trellet (January 2011)

###
### This script allwos you to launch HADDOCK jobs on the grid by a simple command.
### You just have to provide a name for your run, a HADDOCK parameter file, a username and a password.
### It requires an installation of the enmr.eu grid certificate associated to your username and your password.
###

import urllib
import getpass

def usage():
  print "This script is used to launch HADDOCK jobs on the grid providing only a name and a HADDOCK parameter file (ex: haddockparam.web)"
  print "It requires a valid certificate issued by enmr.eu VO and associated to your username and password combination"
  print ""
  print "EXAMPLE: "
  print "##> python run_haddock_file.py job_name param_file_path"
  print "##> Login: toto"
  print "##> Password: "
  print "##Your data have been received and are being processed .............."

  
def launch(name, file):
  # Ask user for username and password
  #username = raw_input('Login: ')
  #password = getpass.getpass('Password: ')
  username = "rvhonorato"
  password = "Rvh2349&"
  # HADDOCK file-upload interface URL 
  #url = 'http://alcazar.science.uu.nl/cgi/services/HADDOCK2.2/haddockserver-file.cgi'
  url = 'http://milou.science.uu.nl/cgi/services/HADDOCK2.2/haddockserver-file.cgi'
  # Params used in the file-upload interface :
  #
  # 'runname': name of your run, 'params': HADDOCK parameters file, 'username': User name, 'password': Password linked to the username
  params = urllib.urlencode({'runname': name, 'params': open(file).read(), 'username':username, 'password':password})
  # POST request with pepetide sequence as parameter
  f = urllib.urlopen(url , params)
  # Get results page informations
  result=f.read()
  print result
  return 0


if __name__ == "__main__":
  import sys
  if (len(sys.argv) < 2) or (sys.argv[1]=="-h"):
    usage()
    sys.exit()
  file = sys.argv[2]
  name = sys.argv[1]
  launch(name,file)
