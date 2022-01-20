#pip install lxml
#pip install beautifulsoup
#npm install requests
#npm install gzip
import requests
import locale
import gzip
import io
import json
import os
import time
from random import randint

key_column = 'groupNbr'
key_column2 = 'recordID'
eor = 'EOR'
current_key= ''
current_key2 = ''


def readFile(filename, locale):
  lang = 'de'
  products = open(filename, 'r',  encoding='utf-8')
  count = 0
  totalPr = 0
  record={}
  while True:
      count += 1
  
      # Get next line from file
      line = products.readline().strip('\n')
      if line:
        split = line.split('|')
        if (split[0]!=eor):
          record[split[0]]=split[1]
        if (split[0]==key_column):
          current_key = split[1]
        if (split[0]==key_column2):
          current_key2 = split[1]
        if (split[0]==eor):
          #end of record
          #save it
          totalPr = totalPr+1
          #first check if json is already there, if so load it and combine
          if not os.path.isfile('jsonde\\'+current_key+'.json'):
            #file not there create it
            #if ('subRangeName' in record):
            #  print (record['subRangeName'])
            #with open('json\\'+current_key+'.json',"w",encoding='cp1252') as file:
            with open('jsonde\\'+current_key+'.json',"w",encoding='utf-8') as file:              
              json.dump(record, file, ensure_ascii=True, indent=4)
              #json.dump(record,file,ensure_ascii=False)
          else:
            #File is there load it and combine
            #print("Load {}".format(current_key))
            with open('jsonde\\'+current_key+'.json', "r",encoding='utf-8') as fh:
              text = fh.read()
              #print (text)
              newrecord = json.loads(text)
            record.update(newrecord)
            #print (record)
            name = 'jsonde\\'+current_key+'.json'
            if (locale):
              name = 'jsonde\\'+current_key2+'.json'
            with open(name, "w", encoding='utf-8') as file:
              text = json.dumps(record, ensure_ascii=True)
              #print (text)
              file.write(text)
              #json.dump(record,file,ensure_ascii=False, indent=4)
              #file.write(record)
          record={}
      # if line is empty
      # end of file is reached
      #if (count>6000): 
      #  break
      if not line:
          break
      print("Line {}/{}".format(count,totalPr))
 
  products.close()
   
readFile('../de/endeca/projects/DE/test_data/baseline/SRCH_de_PRODUCT.dat', False)
readFile('../de/endeca/projects/DE/test_data/baseline/SRCH_de_GLOBAL_ATTRIBUTES.dat', False)
readFile('../de/endeca/projects/DE/test_data/baseline/SRCH_de_LOCALE_PRODUCT.dat', True)
