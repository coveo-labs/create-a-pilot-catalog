import json

fieldsToCreate=[
  "MCM_BEST_FOR",
  "appliancetype",
  "boilertype",
  "brand",
  "btuhband",
  "builtininclusivetemperaturecontrollerclassrating",
  "bymodelnumber",
  "byrangename",
  "cableentry",
  "capacitykghrrecoveryequipmentonly",
  "class",
  "clothingsize",
  "colour",
  "connectionsize",
  "connectionsize1",
  "connectiontype",
  "connectiontype1",
  "connectiontype2",
  "coolingkwband",
  "cylindersize",
  "diameter",
  
  "finish",
  "finspacing",
  "fueltype",
  
  "hotwaterstorageenergyefficiencyclass",
  "kw",
  "length",
  
  "litre",
  "mountingheightm",
  "packquantity",
  "phase",
  "position",
  "pressure",
  "productclass",
  "productstatus",
  "producttype",
  "pumpfeed",
  "range",
  "ratedmaximumpoweratstcw",
  "refrigerant",
  "seasonalspaceheatingenergyefficiencyclass",
  "sector",
  "spraypattern",
  "style",
  "thickness",
  "tofitodxthread",
  "type",
  "voltage",
  "waterentry",
  ]

fieldsToCreateInt=[
    "capacitylitres", 
  "capacitymah", 
"widthmm",
"lengthmm", 
"heightmm", 
"fans", 
]  
template=""" {
          "dateFormat": "",
          "includeInQuery": true,
          "hierarchicalFacet": false,
          "mergeWithLexicon": false,
          "description": "",
          "useCacheForComputedFacet": false,
          "sort": false,
          "type": "STRING",
          "smartDateFacet": false,
          "multiValueFacet": true,
          "multiValueFacetTokenizers": ";",
          "useCacheForNestedQuery": true,
          "name": "[NAME]",
          "stemming": false,
          "includeInResults": true,
          "ranking": false,
          "useCacheForSort": false,
          "facet": false,
          "useCacheForNumericQuery": false
      }"""
templateInt="""
{
          "dateFormat": "",
          "includeInQuery": true,
          "hierarchicalFacet": false,
          "mergeWithLexicon": false,
          "description": "",
          "useCacheForComputedFacet": false,
          "sort": true,
          "type": "DOUBLE",
          "smartDateFacet": false,
          "multiValueFacet": false,
          "multiValueFacetTokenizers": ";",
          "useCacheForNestedQuery": true,
          "name": "[NAME]",
          "stemming": false,
          "includeInResults": true,
          "ranking": false,
          "useCacheForSort": false,
          "facet": true,
          "useCacheForNumericQuery": false
      }"""

fulljson=[]
for key in fieldsToCreate:
   temp = template
   temp = temp.replace('[NAME]','p_'+key.lower())
   fulljson.append(json.loads(temp))

for key in fieldsToCreateInt:
   temp = templateInt
   temp = temp.replace('[NAME]','p_'+key.lower())
   fulljson.append(json.loads(temp))

with open('fields.json',"w",encoding='utf-8') as file:              
    json.dump(fulljson, file, ensure_ascii=True, indent=4)
