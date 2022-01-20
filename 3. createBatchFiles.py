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

def loadSettings(settingfile):
  with open(settingfile, "r",encoding='utf-8') as fh:
    text = fh.read()
    settings = json.loads(text)
  return settings

def splitSKU(meta):
  try:
    keywords = meta.split()
    searchableKeywords = []
    for keyword in keywords:
        #print(keyword)
        letters = list(keyword)
        searchableKeyword = []
        previousChar = ""
        for letter in letters:
            previousChar += letter
            # starting at 3 characters
            if (len(previousChar) > 1):
                searchableKeyword.append(previousChar)
        searchableKeywords += searchableKeyword
    return ';'.join(searchableKeywords)
  except:
    return ''

def splitSpace(prod):
  try:
    parts=prod.split(' ')
    newparts = ''
    for nr in range(1,len(parts)):
      newparts+=prod.replace(' ','',nr)+';'
    return newparts
  except:
    return ''

def addCustomMappings(post, mydoc):
  for key in post:
    val = getKey(post,key)
    if (key.endswith('mm')):
      val = val.replace('mm','').strip()
    mydoc.AddMetadata(key, val)
  return mydoc
  
def add_document(post,filename):
    global storesSKU
    global stores
    # Create new push document
    mydoc = CoveoDocument.Document(post['p_producturl'])
    content = "<meta charset='UTF-16'><meta http-equiv='Content-Type' content='text/html; charset=UTF-16'>"+post['p_all_text']
    #print(content)
    mydoc.SetContentAndZLibCompress(content)
    mydoc.AddMetadata('documenttype','Product')
    mydoc.AddMetadata('objecttype','Product')
    mydoc.AddMetadata("ec_brand", post['p_brand'])
    mydoc.AddMetadata("ec_modelnumber", post['p_mpn'])
    mydoc.AddMetadata("ec_category", post['p_cat'])
    mydoc.AddMetadata("ec_description", post['p_desc'])
    mydoc.AddMetadata("cat_slug", post['p_cat_slug'])
    mydoc.AddMetadata("ec_name", fixHtml(post['p_name']))
    mydoc.AddMetadata("ec_product_id", post['p_productid'])
    mydoc.AddMetadata("ec_images", [post['p_image']])
    mydoc.AddMetadata("ec_image", post['p_image'])
    mydoc.AddMetadata("ec_price", post['p_price'])
    mydoc.AddMetadata("ec_in_stock",  post['p_in_stock'])
    mydoc.AddMetadata("ec_slug", post['p_mpn'])

    mydoc = addCustomMappings(post, mydoc)
    mydoc.AddMetadata("ec_sku", post['p_sku'])
    mydoc.AddMetadata("sku", post['p_productid'])
    #mydoc.AddMetadata("ec_tags", post['p_vals'])
    #mydoc.AddMetadata("ec_docs", post['p_docs'])
    mydoc.AddMetadata("permanentid", post['p_productid'])
    mydoc.Title = fixHtml(post['p_name'])

    
    # Build up the quickview/preview (HTML)

    # Set the fileextension
    mydoc.FileExtension = ".html"
    # Set the date
    try:
      thedate = parse(post['p_date'],dayfirst=True )
      mydoc.SetDate(thedate)
      mydoc.SetModifiedDate(thedate)
    except:
      pass

    return mydoc



allattributes=[]

def getKey(jsont, key):
  if key in jsont:
    if jsont[key]=='(null)':
      return ''
    else:
      return jsont[key]
  else:
    return ''

def fixHtml(htmls):
  htmls = htmls.replace("&amp;","&")
  return html.unescape(htmls)


def createCategories(field, delim):
  categories=[]
  for content in field.split(delim):
    categories.append(content)

  return categories


def createCategoriesPaths(categories):
  catpath=''
  catpaths=[]
  for cat in categories:
     if catpath=='':
       catpath=cat #man
       catpaths.append(catpath)
     else:
       catpath=catpath+'|'+cat
       catpaths.append(catpath)
  #catpaths = list(set(catpaths))
  return catpaths

def createCategoriesSlug(categories):
  slug=[]
  catpath=''
  for cat in categories:
    cat=cat.lower().replace(' ','-')
    if catpath=='':
      catpath=cat #man
      slug.append(catpath)
    else:
      catpath=catpath+'/'+cat
      slug.append(catpath)
  
  #slug = list(set(catpaths))

  return slug

def parse(dir, offset, settingfile):

  settings = loadSettings(settingfile)
  #*********************** SETTINGS ******************************
  pageurl='https://demo.com/web/p/'
  updateSourceStatus = True
  deleteOlder = True

  total=0
  #*********************** SETTINGS ******************************
  # Setup the push client
  push = CoveoPush.Push(settings['sourceId'], settings['orgId'], settings['apiKey'], p_Endpoint=settings['endpoint'],p_Mode=CoveoConstants.Constants.Mode.Stream, p_Save=True, p_Offset=offset)
  # Set the maximum
  push.SetSizeMaxRequest(15*1024*1024)
  allattributes={}
  # Start the batch
  push.Start(updateSourceStatus, deleteOlder)
  totalf=0
  #url = '0100034.json'
  urls = glob.glob(dir+'\\*.json')
  for url in urls:
      #if (url.startswith('https___uk')):
    print (str(total)+'/'+str(totalf)+' - '+url)

    try:
       with open(url, "r",encoding='utf-8') as fh:
        text = fh.read()
        fh.close()
        totalf=totalf+1
        jsont = json.loads(text)
        #only parse when longDescription is in
        if "DocumentId" in jsont:
          data={}
          #print (jsont)
          data['p_images'] = getKey(jsont,'image_url')
          data['p_image'] = getKey(jsont,'image_url')
          data['p_name'] = getKey(jsont,'title')
          data['p_sku'] = getKey(jsont,'productid')
          #data['p_date'] =  getKey(jsont,'introductionDate')
          split_sku=''
          mpn=getKey(jsont,'supplierproductcode')
          data['p_mpn'] = mpn
          try:
            splitSpaces = splitSpace(getKey(jsont,'productid'))+';'+splitSpace(mpn)
            split_sku = splitSKU(getKey(jsont,'productid'))+';'+splitSKU(mpn)+';'+splitSpaces
            split_sku = split_sku.replace(';',' ')+' '+getKey(jsont,'productid').replace('-','').replace('.','')+' '+mpn.replace('-','').replace('.','')
          except:
            pass
          #print (split_sku)
          data['p_brand'] = getKey(jsont,'brand')
          data['p_price'] = getKey(jsont,'price')
          data['p_desc'] = getKey(jsont,'description')
          groupid = getKey(jsont,'groupid')
          if groupid=='':
            groupid = getKey(jsont,'productid')
          data['ec_item_group_id'] = groupid

          
          #with open('test.json', "w") as file:
          #      file.write(json.dumps(jsont,indent=3))
          #print (json.dumps(jsont,indent=3))
          #data['p_domain'] = jsont['props']['pageProps']['atlas']['region']
          all_text = ''#jsont['props']['pageProps']['articleResult']['data']['article']['descriptiveContent']['unique']['content']
          p_all_text = '<html><body>'
          for content in jsont:
            p_all_text += ' '+getKey(jsont, content)
            key ='p_'+content.replace(' ','_').lower() 
            data[key]=jsont[content]
            if (key not in allattributes):
              allattributes[key]=jsont[content]
            else:
              if (len(allattributes[key])<500):
                allattributes[key] = allattributes[key]+';'+jsont[content]
            #print (p_all_text)
          data['p_in_stock']= False#jsont['props']['pageProps']['articleResult']['data']['article']['productAvailability']['productPageStockLevel']
          data['p_productid']= getKey(jsont,'productid')
          #data['p_producturl']= pageurl+getKey(jsont,'groupNbr')
          data['p_producturl']= pageurl+getKey(jsont,'productid')
          
          #print (p_all_text)
          #print (p_in_stock)
          #next

          categories = createCategories( getKey(jsont,'category'),'\\')
          data['p_cat'] = createCategoriesPaths(categories)
          data['p_cat_slug'] = createCategoriesSlug(categories)
          
          p_all_text+=' '+split_sku+'</body></html'
          #print (p_all_text)
          data['p_all_text']=p_all_text
          
          
          push.Add(add_document(data,''))
          #print (attr)
          total = total +1
          #if (total>5000):
          #  break
        else:
          print ("MAYDAY: No DocumentId in: "+url)
        #if total>15000:
        #  break
    except Exception as e:
        print (e)
        pass
  # End the Push

  with open('output.json',"w",encoding='utf-8') as file:              
    json.dump(allattributes, file, sort_keys=True, ensure_ascii=True, indent=4)

  push.End(updateSourceStatus, deleteOlder)

if __name__ == "__main__":
    dir = sys.argv[1]
    offset = sys.argv[2]
    settingfile = sys.argv[3]
    print(dir)
    print(offset)
    parse(dir,int(offset), settingfile)


