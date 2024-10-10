import pandas as pd
import requests
import xml.etree.ElementTree as ET

OC = 'younwjdtjr'
target = 'law'
url = 'http://www.law.go.kr/DRF/lawSearch.do?'
data = []

for i in range(1,56):
    params = {
      'OC' : OC,
      'target' : target,
      'type' : 'XML',
      'display' : 100,
      'search' : 1,
      'page' : i
    }
  
    response = requests.get(url, params=params)
  
    if response.status_code==200:
        root = ET.fromstring(response.content)
        items = root.findall('.//LawSearch')
        print(items)
    else:
        print(response.status_code)    
