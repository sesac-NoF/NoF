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
        root = ET.fromstring(response.text)
        items = root.findall('.//law')
        if len(items) != 0:
            for item in items:
                LAW_NUM = item.find('.//법령일련번호')
                CODE = item.find('.//현행연혁코드')
                LAW_NAME_KR = item.find('.//법령명한글')
                LAW_NAME = item.find('.//법령약칭명')
                LAW_ID = item.find('.//법령ID')
                ANC_YD = item.find('.//공포일자')
                ANC_NUM = item.find('.//공포번호')
                SPL = item.find('.//제개정구분명')
                ORG_CODE = item.find('.//소관부처코드')
                ORG_NAME = item.find('.//소관부처명')
                LAW_CASE = item.find('.//법령구분명')
                EF_YD = item.find('.//시행일자')
                LAW_LINK = item.find('.//법령상세링크')
                data.append([LAW_NUM.text, CODE.text, LAW_NAME_KR.text, LAW_NAME.text, LAW_ID.text, ANC_YD.text, ANC_NUM.text, 
                            SPL.text, ORG_CODE.text, ORG_NAME.text, LAW_CASE.text, EF_YD.text, LAW_LINK.text])
    else:
        print(response.status_code)
df = pd.DataFrame(data=data, columns=['법령일련번호','현행연혁코드','법령명한글','법령약칭명','법령ID','공포일자','공포번호','제개정구분명','소관부처코드','소관부처명','법령구분명','시행일자','볍령상세링크'])
df.to_csv('data/law_list_data.csv', index=False)