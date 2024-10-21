import pandas as pd
import requests
import xml.etree.ElementTree as ET

####### 목록 #########
OC = 'ykdb0508'
target = 'prec'
url = 'http://www.law.go.kr/DRF/lawSearch.do?'
data = []

for i in range(1, 25):  # Adjust the range based on the number of pages
    params = {
        'OC': OC,
        'target': target,
        'type': 'XML',
        'display': 100,
        'search': 1,
        'page': i
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        items = root.findall('.//prec')

        if len(items) != 0:
            for item in items:
                ORDER_NUM = item.find('.//판례일련번호').text if item.find('.//판례일련번호') is not None else ''
                CASE_NAME = item.find('.//사건명').text if item.find('.//사건명') is not None else ''
                CASE_NUM = item.find('.//사건번호').text if item.find('.//사건번호') is not None else ''
                CASE_DATE = item.find('.//선고일자').text if item.find('.//선고일자') is not None else ''
                SCOURT = item.find('.//법원명').text if item.find('.//법원명') is not None else ''
                CASE = item.find('.//사건종류명').text if item.find('.//사건종류명') is not None else ''
                LINK = item.find('.//판례상세링크').text if item.find('.//판례상세링크') is not None else ''

                data.append([ORDER_NUM, CASE_NAME, CASE_NUM, CASE_DATE, SCOURT, CASE, LINK])
    else:
        print(f'Error on page {i}: Status code {response.status_code}')

# Convert to DataFrame
df = pd.DataFrame(data=data, columns=['판례일련번호', '사건명', '사건번호', '선고일자', '법원명', '사건종류명', '판례상세링크'])

######## 본문 ########

OC = 'ykdb0508'
target = 'prec'
url = 'http://www.law.go.kr/DRF/lawService.do?'
data2 = []

for i in range(226, 450):  # 수정된 부분
    params = {
        'OC': OC,
        'target': target,
        'type': 'XML',
        'ID': df['판례일련번호'].iloc[i-1]
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        print(root.find('.//사건번호').text, root.find('.//사건명').text)
        CASE_NUM = root.find('.//사건번호')
        JUD = root.find('.//선고')
        JUD_TYPE = root.find('.//판결유형')
        ISSUE = root.find('.//판시사항')
        SUMMARY_JUD = root.find('.//판결요지')
        REF_STAT = root.find('.//참조조문')
        REF_CASE = root.find('.//참조판례')
        CASE_CONTENT = root.find('.//판례내용')

        data2.append([
            df['판례일련번호'].iloc[i-1],  # 판례일련번호
            CASE_NUM.text if CASE_NUM is not None else None,  # 사건번호
            JUD.text if JUD is not None else None,  # 선고
            JUD_TYPE.text if JUD_TYPE is not None else None,  # 판결유형
            ISSUE.text if ISSUE is not None else None,  # 판시사항
            SUMMARY_JUD.text if SUMMARY_JUD is not None else None,  # 판결요지
            REF_STAT.text if REF_STAT is not None else None,  # 참조조문
            REF_CASE.text if REF_CASE is not None else None,  # 참조판례
            CASE_CONTENT.text if CASE_CONTENT is not None else None  # 판례내용
        ])
    else:
        print('error')

df2 = pd.DataFrame(data=data2, columns=['판례정보일련번호', '사건번호', '선고', '판결유형', '판시사항', '판결요지', '참조조문', '참조판례', '판례내용'])

df2.to_csv('case.csv')

