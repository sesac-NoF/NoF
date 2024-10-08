import pandas as pd
import requests
import xml.etree.ElementTree as ET
from re import I

OC = 'ykdb0508'
target = 'prec'
url = 'http://www.law.go.kr/DRF/lawSearch.do?'
data = []
for i in range(226,451):
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
    print(ET.tostring(root, encoding='utf-8').decode('utf-8'))
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
    print('error')
df = pd.DataFrame(data=data, columns=['판례일련번호','사건명','사건번호','선고일자','법원명','사건종류명','판례상세링크'])
df.to_csv('df_data.csv')


# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry

# session = requests.Session()
# retry = Retry(connect=5, backoff_factor=0.5)
# adapter = HTTPAdapter(max_retries=retry)
# session.mount('http://www.law.go.kr/DRF/lawService.do?', adapter)

# df = pd.read_csv('df_data.csv')

# OC = 'ykdb0508'
# target = 'prec'
# url = 'http://www.law.go.kr/DRF/lawService.do?'
# data = []

# for i in range(1,df['판례일련번호'].value_counts().sum()+1):
#     params = {
#         'OC' : OC,
#         'target' : target,
#         'type' : 'XML',
#         'ID' : df['판례일련번호'].iloc[i-1]
#     }
#     response = requests.get(url, params=params, timeout=20)

#     if response.status_code == 200:
#         root = ET.fromstring(response.content)
#         CASE_NUM = root.find('.//사건번호')
#         JUD = root.find('.//선고')
#         JUD_TYPE = root.find('.//판결유형')
#         ISSUE = root.find('.//판시사항')
#         SUMMARY_JUD = root.find('.//판결요지')
#         REF_STAT = root.find('.//참조조문')
#         REF_CASE = root.find('.//참조판례')
#         CASE_CONTENT = root.find('.//판례내용')
      
#         data.append([
#                         df['판례일련번호'].iloc[i-1],
#                         CASE_NUM.text if CASE_NUM is not None else None,
#                         JUD.text if JUD is not None else None,
#                         JUD_TYPE.text if JUD_TYPE is not None else None,
#                         ISSUE.text if ISSUE is not None else None,
#                         SUMMARY_JUD.text if SUMMARY_JUD is not None else None,
#                         REF_STAT.text if REF_STAT is not None else None,
#                         REF_CASE.text if REF_CASE is not None else None,
#                         CASE_CONTENT.text if CASE_CONTENT is not None else None
#                     ])
#     else:
#         print(i,'error')
#     print(i)
    
# df2 = pd.DataFrame(data=data, columns=['판례정보일련번호','사건번호','선고','판결유형','판시사항','판결요지','참조조문','참조판례','판례내용'])
# df2.to_csv('df_data2.csv', index=False)