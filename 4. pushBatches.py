#pip install lxml
#pip install beautifulsoup
#npm install requests
#npm install gzip
#pip install python-dateutil
#pip install git+https://github.com/coveo-labs/SDK-Push-Python
import requests
import gzip
import io
import glob
import os
import sys
import json
import time
from datetime import datetime
import xml.etree.ElementTree as ET

from random import randint
from bs4 import BeautifulSoup
from coveopush import CoveoPush
from coveopush import CoveoDocument
from coveopush import CoveoPermissions
from coveopush import CoveoConstants
from dateutil.parser import parse
import html
stores=["1","2","3","4","5","6","7"]
storesSKU={}

def get(post, value):
  if value in post:
    return post[value]
  else:
    return ''


def loadSettings(settingsfile):
  with open(settingsfile, "r",encoding='utf-8') as fh:
    text = fh.read()
    settings = json.loads(text)
  return settings

def parse(dir, offset, settingsfile):

  settings = loadSettings(settingsfile)
  #*********************** SETTINGS ******************************
  direct = 'batch'
  updateSourceStatus = True
  deleteOlder = True

  total=0
  #*********************** SETTINGS ******************************
  # Setup the push client
  push = CoveoPush.Push(settings['sourceId'], settings['orgId'], settings['apiKey'], p_Endpoint=settings['endpoint'],p_Mode=CoveoConstants.Constants.Mode.Stream, p_Save=False, p_Offset=0)
  # Set the maximum
  push.SetSizeMaxRequest(150*1024*1024)

  # Start the batch
  push.Start(updateSourceStatus, deleteOlder)
  totalf=0
  supertotal=0
  urls = glob.glob('batch\\*.*')
  for url in urls:
      #if (url.startswith('https___uk')):
    print (str(supertotal)+'/'+str(totalf)+' - '+url)

    try:
       with open(url, "r",encoding='utf-8') as fh:
        text = fh.read()
        fh.close()
        jsont = json.loads(text)
        for rec in jsont:
          #print (rec['ec_sku'])
          push.AddJson(rec)
          total=total+1
          supertotal=supertotal+1
        totalf=totalf+1

    except Exception as e:
        print (e)
        pass

    print (str(supertotal)+'/'+str(totalf)+' - '+url)
  # End the Push
  push.End(updateSourceStatus, deleteOlder)

if __name__ == "__main__":
    dir = sys.argv[1]
    offset = sys.argv[2]
    settingfile = sys.argv[3]
    print(dir)
    print(offset)
    parse(dir,int(offset), settingfile)


