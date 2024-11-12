import pandas as pd
import requests
import xml.etree.ElementTree as ET

OC = 'younwjdtjr'
target = 'prec'
url = 'http://www.law.go.kr/DRF/lawSearch.do?'
data = []
for i in range(451,676):
  params = {
      'OC' : OC,
      'target' : target,
      'type' : 'XML',
      'display' : 100,
      'search' : 1,
      'page' : i
  }

  response = requests.get(url, params=params)

  if response.status_code == 200:
    root = ET.fromstring(response.content)
    items = root.findall('.//prec')
    # xml구조확인
    # print(ET.tostring(root, encoding='utf-8').decode('utf-8'))
    if len(items) != 0:
      for item in items:
        ORDER_NUM = item.find('.//판례일련번호')
        CASE_NAME = item.find('.//사건명')
        CASE_NUM = item.find('.//사건번호')
        CASE_DATE = item.find('.//선고일자')
        SCOURT = item.find('.//법원명')
        CASE = item.find('.//사건종류명')
        LINK = item.find('.//판례상세링크')
        data.append([ORDER_NUM.text, CASE_NAME.text, CASE_NUM.text, CASE_DATE.text, SCOURT.text, CASE.text, LINK.text])
  else:
    print(response.status_code)
df = pd.DataFrame(data=data, columns=['판례일련번호','사건명','사건번호','선고일자','법원명','사건종류명','판례상세링크'])

df.to_csv('data/list_API.csv', index=False)