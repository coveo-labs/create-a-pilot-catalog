
import requests
import locale
import gzip
import io
import json
import os
import time
import csv
from random import randint

key_column = 'groupNbr'
eor = 'EOR'
current_key= ''

import csv

    
def readFile(filename, products, path):
  #with open(filename, encoding='utf-8') as csv_file:
  with open(filename) as csv_file:
    #csv_reader = csv.reader(csv_file, delimiter='\t')
    rows = csv.DictReader(csv_file, delimiter='\t')
    count = 0
    for row in rows:
      rec={}
      count = count+1
      if products:
        current_key = row['productid']
      else:
        current_key = row['pid']
        rec[row['ATTRIBUTE']]=row['VALUE']
      print(str(count)+" ==> Processing: "+current_key)
      if not os.path.isfile(path+'\\'+current_key+'.json'):
        #file not there create it
        if (not products):
          print("MAYDAY THIS SHOULD NOT HAPPEN")
        else:
          with open(path+'\\'+current_key+'.json',"w",encoding='utf-8') as file:              
            json.dump(row, file, ensure_ascii=True, indent=4)
      else:
        #File is there load it and combine
        print("Load {}".format(current_key))
        with open(path+'\\'+current_key+'.json', "r",encoding='utf-8') as fh:
          text = fh.read()
          #print (text)
          newrecord = json.loads(text)
        if products:
          row.update(newrecord)
        else:
          rec.update(newrecord)
        #print (record)
        with open(path+'\\'+current_key+'.json', "w", encoding='utf-8') as file:
          if products:
            text = json.dumps(row, ensure_ascii=True)
          else:
            text = json.dumps(rec, ensure_ascii=True)
          #print (text)
          file.write(text)
          #json.dump(record,file,ensure_ascii=False, indent=4)
          #file.write(record)
      record={}

#
readFile('C:\\Customers\\CLIENT\\Coveo Sales Catdata\\Coveo Products sales cat.csv',True,'json_sales')
readFile('C:\\Customers\\CLIENT\\Coveo Sales Catdata\\Attributes sales cat 1.csv',False,'json_sales')
readFile('C:\\Customers\\CLIENT\\Coveo Sales Catdata\\Attributes sales cat 2.csv',False,'json_sales')
readFile('C:\\Customers\\CLIENT\\Coveo Sales Catdata\\Attributes sales cat 3.csv',False,'json_sales')

#
readFile('C:\\Customers\\CLIENT\\Coveo Master cat products\\Coveo Products master cat 1.csv',True,'json')
readFile('C:\\Customers\\CLIENT\\Coveo Master cat products\\Coveo Products master cat 2.csv',True,'json')
readFile('C:\\Customers\\CLIENT\\Coveo Master cat products\\Coveo Products master cat 3.csv',True,'json')
readFile('C:\\Customers\\CLIENT\\Coveo Master cat products\\Coveo Products master cat 4.csv',True,'json')
#
readFile('C:\\Customers\CLIENT\\Coveo Master cat attributes\\Attributes all 1.csv',False, 'json')
readFile('C:\\Customers\CLIENT\\Coveo Master cat attributes\\Attributes all 2.csv',False, 'json')
readFile('C:\\Customers\CLIENT\\Coveo Master cat attributes\\Attributes all 3.csv',False, 'json')
readFile('C:\\Customers\CLIENT\\Coveo Master cat attributes\\Attributes all 4.csv',False, 'json')
readFile('C:\\Customers\CLIENT\\Coveo Master cat attributes\\Attributes all 5.csv',False, 'json')
readFile('C:\\Customers\CLIENT\\Coveo Master cat attributes\\Attributes all 6.csv',False, 'json')
readFile('C:\\Customers\CLIENT\\Coveo Master cat attributes\\Attributes all 7.csv',False, 'json')
readFile('C:\\Customers\CLIENT\\Coveo Master cat attributes\\Attributes all 8.csv',False, 'json')
readFile('C:\\Customers\CLIENT\\Coveo Master cat attributes\\Attributes all 9.csv',False, 'json')
readFile('C:\\Customers\CLIENT\\Coveo Master cat attributes\\Attributes all 10.csv',False, 'json')
readFile('C:\\Customers\CLIENT\\Coveo Master cat attributes\\Attributes all 11.csv',False, 'json')
readFile('C:\\Customers\CLIENT\\Coveo Master cat attributes\\Attributes all 12.csv',False, 'json')

