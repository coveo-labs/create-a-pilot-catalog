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

def add_document(post,filename):
    global storesSKU
    global stores
    # Create new push document
    mydoc = CoveoDocument.Document(post['p_producturl'])
    content = "<meta charset='UTF-16'><meta http-equiv='Content-Type' content='text/html; charset=UTF-16'>"+post['p_all_text']
    mydoc.SetContentAndZLibCompress(content)
    mydoc.AddMetadata('documenttype','Product')
    mydoc.AddMetadata('objecttype','Product')
    mydoc.AddMetadata("ec_brand", post['p_brand'])
    mydoc.AddMetadata("mysite", get(post,'site'))
    mydoc.AddMetadata("ec_modelnumber", post['p_mpn'])
    mydoc.AddMetadata("ec_category", post['p_cat'])
    mydoc.AddMetadata("ec_description", post['p_desc'])
    mydoc.AddMetadata("category_slug", post['p_cat'].replace('|','/').replace(' ','-').lower())
    mydoc.AddMetadata("ec_name", fixHtml(post['p_name']))
    mydoc.AddMetadata("ec_product_id", post['p_productid'])
    mydoc.AddMetadata("ec_images", post['p_image'])
    mydoc.AddMetadata("ec_image", post['p_image'])
    mydoc.AddMetadata("ec_price", post['p_price'])
    mydoc.AddMetadata("ec_promo_price", post['p_price_low'])
    mydoc.AddMetadata("ec_in_stock",  post['p_in_stock'])
    mydoc.AddMetadata("ec_slug", post['p_mpn'])
    #mydoc.AddMetadata("ec_region", post['p_domain'])
    mydoc.AddMetadata("ec_disk_type", get(post,'p_Disk_Type'))
    mydoc.AddMetadata("ec_series", get(post,'p_Series'))
    mydoc.AddMetadata("ec_amplifier_type", get(post,'p_Amplifier_Type')+get(post,'p_Verstärker-Typ'))
    mydoc.AddMetadata("ec_current_type", get(post,'p_Current_Type'))
    mydoc.AddMetadata("ec_material", get(post,'p_Material'))
    mydoc.AddMetadata("ec_output_voltage",get(post,'p_Output_Voltage')+get(post,'p_Ausgangsspannung'))
    volt=get(post,'p_Output_Voltage')+get(post,'p_Ausgangsspannung')
    volt = volt.replace("V","")
    mydoc.AddMetadata("ec_output_voltage_num",get(post,'p_Output_Voltage')+get(post,'p_Ausgangsspannung'))
    mydoc.AddMetadata("ec_input_range",get(post,'p_Input_Voltage_Range')+get(post,'p_Eingangsspannung'))
    mydoc.AddMetadata("ec_input_voltage",get(post,'p_Input_Voltage_Nominal')+get(post,'p_Eingangsnennspannung'))
    mydoc.AddMetadata("ec_power_rating",get(post,'p_Power_Rating')+get(post,'p_Nennleistung'))
    mydoc.AddMetadata("ec_maximum_temperature", get(post,'p_Maximum_Temperature')+''+get(post,'p_Maximum_Operating_Temperature')+''+get(post,'p_Betriebstemperatur max.'))
    mydoc.AddMetadata("ec_gender", get(post,'p_Gender'))
    mydoc.AddMetadata("ec_contact_material", get(post,'p_Contact_Material')+get(post,'p_Kontaktmaterial'))
    mydoc.AddMetadata("ec_end_type", get(post,'p_End_Type')+get(post,'p_End_Typ'))
    mydoc.AddMetadata("ec_insert_type", get(post,'p_Insert_Type')+get(post,'p_Insert_Typ'))
    mydoc.AddMetadata("ec_maximum_supply_voltage", get(post,'p_Maximum_Supply_Voltage')+get(post,'p_Versorgungsspannung_max.'))
    mydoc.AddMetadata("ec_flanged", get(post,'p_Flanged')+get(post,'p_Mit_Flansch'))
    mydoc.AddMetadata("ec_hazardous_area_certification", get(post,'p_Hazardous_Area_Certification'))
    mydoc.AddMetadata("ec_ral_code", get(post,'p_RAL_Code'))
    mydoc.AddMetadata("ec_gasket_material", get(post,'p_Gasket_Material')+get(post,'p_Dichtungswerkstoff'))
    mydoc.AddMetadata("ec_disc_size", get(post,'p_Disc_Size')+get(post,'p_Scheibengröße'))
    mydoc.AddMetadata("ec_grinder_type", get(post,'p_Grinder_Type')+get(post,'p_Schleiferart'))
    mydoc.AddMetadata("ec_speed", get(post,'p_Speed')+get(post,'p_Hub-/Drehzahl'))
    mydoc.AddMetadata("ec_plug_type", get(post,'p_Plug_Type')+get(post,'p_Steckertyp'))
    mydoc.AddMetadata("ec_thermal_resistance", get(post,'p_Thermal_Resistance')+get(post,'p_Wärmewiderstand'))
    mydoc.AddMetadata("ec_mounting", get(post,'p_Mounting')+get(post,'p_Montage'))
    mydoc.AddMetadata("ec_number_of_levers", get(post,'p_Number_of_Levers')+get(post,'p_Anzahl_Hebel'))
    mydoc.AddMetadata("ec_maximum_coil_frequency", get(post,'p_Maximum_Coil_Frequency'))
    mydoc.AddMetadata("ec_coil_resistance", get(post,'p_Coil_Resistance'))
    mydoc.AddMetadata("ec_contact_resistance", get(post,'p_Contact_Resistance'))
    mydoc.AddMetadata("ec_contact_voltage", get(post,'p_Contact_Voltage'))
    mydoc.AddMetadata("ec_coil_power", get(post,'p_Coil_Power'))
    mydoc.AddMetadata("ec_life", get(post,'p_Life'))
    mydoc.AddMetadata("ec_hinge_type", get(post,'p_Hinge_Type'))
    mydoc.AddMetadata("ec_closing_type", get(post,'p_Closing_Type'))
    mydoc.AddMetadata("ec_fixing_method", get(post,'p_Fixing_Method'))
    mydoc.AddMetadata("ec_user_interface", get(post,'p_User_Interface'))
    mydoc.AddMetadata("ec_cross_sectional_area", get(post,'p_Cross_Sectional_Area'))
    mydoc.AddMetadata("ec_american_wire_gauge", get(post,'p_American_Wire_Gauge'))
    mydoc.AddMetadata("ec_core_strands", get(post,'p_Core_Strands'))
    mydoc.AddMetadata("ec_conductor_material", get(post,'p_Conductor_Material'))
    mydoc.AddMetadata("ec_wire_style", get(post,'p_Wire_Style'))
    mydoc.AddMetadata("ec_insulation_wall_thickness", get(post,'p_Insulation_Wall_Thickness'))
    mydoc.AddMetadata("ec_connector_system", get(post,'p_Connector_System'))
    mydoc.AddMetadata("ec_tool_type", get(post,'p_Tool_Type'))
    mydoc.AddMetadata("ec_plugsocket", get(post,'p_Plug/Socket'))
    mydoc.AddMetadata("ec_contact_gender", get(post,'p_Contact_Gender'))
    mydoc.AddMetadata("ec_mating_type", get(post,'p_Mating_Type'))
    mydoc.AddMetadata("ec_mounting_type", get(post,'p_Mounting_Type')+''+get(post,'p_Montage-Typ'))
    mydoc.AddMetadata("ec_response_time", get(post,'p_Response_Time'))
    mydoc.AddMetadata("ec_accuracy", get(post,'p_Accuracy'))
    mydoc.AddMetadata("ec_cable_length", get(post,'p_Cable_Length'))
    mydoc.AddMetadata("ec_inner_dia", get(post,'p_Innendurchmesser')+get(post,'p_Inside_Diameter'))
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
    return jsont[key]
  else:
    return ''

def fixHtml(htmls):
  htmls = htmls.replace("&amp;","&")
  return html.unescape(htmls)

def getTax(root,key):
  #Find Key in TAX file
  #node id= key
  #return ''
  #print ("GetTax")
  try:
    node = root.findall(".//*[@id='"+key+"']")
    #Take parent
    #node.parent
    parent = node[0].get('parent')
    #print ("Parent ("+key+"): "+parent)
    #node id=node.parent
    parentnode = root.findall(".//*[@id='"+parent+"']")
    #Take property name="supersection"
    #print ("Parentnode ("+key+"): "+parentnode[0].text)
    parentfound = parentnode[0].findall(".//*[@name='supersection']")
    print ("Parent found ("+key+"): "+parentfound[0].text)
    return parentfound[0].text
  except Exception as e:
    print (e)
    return 'Global'

def loadSettings(settingfile):
  with open(settingfile, "r",encoding='utf-8') as fh:
    text = fh.read()
    settings = json.loads(text)
  return settings


def parse(dir, offset):

  #*********************** SETTINGS ******************************
  settings = loadSettings('settings.json')
  direct = 'jsonde'
  country = 'de'
  lang = 'de'
  country_sub = 'de'
  imageurl='https://YOURURL/rsc/image/upload/'
  pageurl='https://YOURURL.com/web/p/'
  updateSourceStatus = True
  deleteOlder = True
  sourceId = settings['sourceId']
  orgId = settings['orgId']
  apiKey = settings['apiKey']

  total=0
  #*********************** SETTINGS ******************************
  # Setup the push client
  push = CoveoPush.Push(sourceId, orgId, apiKey, p_Endpoint='https://api-eu.cloud.coveo.com/push/v1',p_Mode=CoveoConstants.Constants.Mode.Stream, p_Save=True, p_Offset=offset)
  # Set the maximum
  push.SetSizeMaxRequest(15*1024*1024)

  # Start the batch
  push.Start(updateSourceStatus, deleteOlder)
  totalf=0
  #url = '0100034.json'
  root = ET.parse('../'+country+'/endeca/projects/'+country_sub+'/test_data/baseline/SRCH_'+lang+'_TAXONOMY.xml').getroot()
  urls = glob.glob(direct+'\\'+dir)
  for url in urls:
      #if (url.startswith('https___uk')):
    print (str(total)+'/'+str(totalf)+' - '+url)

    try:
      if ('_' in url):
       with open(url, "r",encoding='utf-8') as fh:
        text = fh.read()
        fh.close()
        totalf=totalf+1
        jsont = json.loads(text)
        #only parse when longDescription is in
        if 'longDescription' in jsont:
          data={}
          #print (jsont)
          data['p_image'] = imageurl+getKey(jsont,'imagePrimary')
          data['p_name'] = getKey(jsont,'longDescription')
          data['p_sku'] = getKey(jsont,'groupNbr')
          data['site'] = getKey(jsont,'site')
          data['p_date'] =  getKey(jsont,'introductionDate')
          data['p_mpn'] = getKey(jsont,'manufacturerPartNumber')
          #print (data['p_sku'])
          #print (data['p_mpn'])
          split_sku=''
          mpn=data['p_mpn']
          if (mpn):
            print('MPN==>'+mpn)
          else:
            mpn=''
            print('mpn is null')

          try:
            splitSpaces = splitSpace(data['p_sku'])+';'+splitSpace(mpn)
            split_sku = splitSKU(data['p_sku'])+';'+splitSKU(mpn)+';'+splitSpaces
            split_sku = split_sku.replace(';',' ')+' '+data['p_sku'].replace('-','').replace('.','')+' '+mpn.replace('-','').replace('.','')
          except:
            pass
          #print (split_sku)
          data['p_brand'] = getKey(jsont,'brand')
          data['p_price'] = getKey(jsont,'breakPrice1')
          data['p_price_low'] = data['p_price']
          data['p_desc'] = getKey(jsont,'longDescription')

          
          all_text = ''
          p_all_text = '<html><body>'
          for content in jsont:
            p_all_text += ' '+jsont[content]
            key ='p_'+content.replace(' ','_') 
            data[key]=jsont[content]
            if (key not in allattributes):
              allattributes.append(key)
            #print (p_all_text)
          data['p_in_stock']= False#jsont['props']['pageProps']['articleResult']['data']['article']['productAvailability']['productPageStockLevel']
          data['p_productid']= getKey(jsont,'ecProductID')
          #data['p_producturl']= pageurl+getKey(jsont,'groupNbr')
          data['p_producturl']= pageurl+getKey(jsont,'recordID')
          
          #print (p_all_text)
          #print (p_in_stock)
          #next

          data['p_head_cat'] = getTax(root,getKey(jsont,'familyID'))
          data['p_sub_cat'] = getKey(jsont,'sectionName')
          data['p_item_cat'] = getKey(jsont,'familyName')
          data['p_cat']=data['p_head_cat']+';'+data['p_head_cat']+'|'+data['p_sub_cat']+';'+data['p_head_cat']+'|'+data['p_sub_cat']+'|'+data['p_item_cat']
          #print (p_head_cat)
          #print (p_sub_cat)
          #print (p_item_cat)
          
          p_all_text+=' '+split_sku+'</body></html'
          data['p_all_text']=p_all_text
          
          
          push.Add(add_document(data,''))
          #print (attr)
          total = total +1
          #if (total>5000):
          #  break
        else:
          print ("MAYDAY: Not LongDescription in: "+url)

    except Exception as e:
        print (e)
        pass
  # End the Push
  push.End(updateSourceStatus, deleteOlder)

if __name__ == "__main__":
    dir = sys.argv[1]
    offset = sys.argv[2]
    print(dir)
    print(offset)
    parse(dir,int(offset))


