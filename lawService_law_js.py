import pandas as pd
import requests
import xml.etree.ElementTree as ET


df = pd.read_csv('data/law_list_data.csv')

OC = 'younwjdtjr'
target = 'law'
url = 'http://www.law.go.kr/DRF/lawService.do?'
data1 = []
data2 = []
for n in range(len(df)):
    print(n)
    params = {
        'OC' : OC,
        'target' : target,
        'type' : 'XML',
        'ID' : df['법령ID'].iloc[n]
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        LAW_ID = root.find('.//법령ID')
        jomun = root.find('.//조문')
        jomun_list = jomun.findall('.//조문단위')
        # print(jomun_list)

        for i in range(len(jomun_list)):
            jomun_num = jomun_list[i].find('.//조문번호')
            jomun_is = jomun_list[i].find('.//조문여부')
            jomun_title = jomun_list[i].find('.//조문제목')
            jomun_date = jomun_list[i].find('.//조문시행일자')
            jomun_content = jomun_list[i].find('.//조문내용')
            hang_list = jomun[i].findall('.//항')
            if len(hang_list)!=0:   ##항이 있는 경우
                for j in range(len(hang_list)):
                    hang_num = hang_list[j].find('.//항번호')
                    hang_content = hang_list[j].find('.//항내용')
                    ho_list = hang_list[j].findall('.//호')
                    if len(ho_list) == 0:  # 호가 없는경우
                        ho_num = ''
                        ho_content = ''
                        data1.append([LAW_ID.text if LAW_ID is not None else '',
                                jomun_num.text if jomun_num is not None else '', 
                                jomun_is.text if jomun_is is not None else '', 
                                jomun_title.text if jomun_title is not None else '', 
                                jomun_date.text if jomun_date is not None else '', 
                                jomun_content.text if jomun_content is not None else '',
                                hang_num.text if hang_num is not None else '',
                                hang_content.text if hang_content is not None else '',
                                ho_num if ho_num is not None else '', 
                                ho_content if ho_content is not None else ''])
                    else:  # 호가 있는경우
                        for k in range(len(ho_list)):
                            ho_num = ho_list[k].find('.//호번호')
                            ho_content = ho_list[k].find('.//호내용')
                            data1.append([LAW_ID.text if LAW_ID is not None else '',
                                    jomun_num.text if jomun_num is not None else '', 
                                    jomun_is.text if jomun_is is not None else '', 
                                    jomun_title.text if jomun_title is not None else '', 
                                    jomun_date.text if jomun_date is not None else '', 
                                    jomun_content.text if jomun_content is not None else '',
                                    hang_num.text if hang_num is not None else '',
                                    hang_content.text if hang_content is not None else '',
                                    ho_num.text if ho_num is not None else '', 
                                    ho_content.text if ho_content is not None else ''])      
            else:  # 항이 없는 경우
                hang_num = ''
                hang_content = ''
                ho_list = jomun_list[i].findall('.//호')
                if len(ho_list) == 0:  # 호가 없는 경우
                    ho_num = ''
                    ho_content = ''
                    data1.append([LAW_ID.text if LAW_ID is not None else '',
                            jomun_num.text if jomun_num is not None else '', 
                            jomun_is.text if jomun_is is not None else '', 
                            jomun_title.text if jomun_title is not None else '', 
                            jomun_date.text if jomun_date is not None else '', 
                            jomun_content.text if jomun_content is not None else '',
                            hang_num if hang_num is not None else '',
                            hang_content if hang_content is not None else '',
                            ho_num if ho_num is not None else '', 
                            ho_content if ho_content is not None else ''])
                else:  #호가 있는 경우
                    for k in range(len(ho_list)):
                        ho_num = ho_list[k].find('.//호번호')
                        ho_content = ho_list[k].find('.//호내용')
                        data1.append([LAW_ID.text if LAW_ID is not None else '',
                                jomun_num.text if jomun_num is not None else '', 
                                jomun_is.text if jomun_is is not None else '', 
                                jomun_title.text if jomun_title is not None else '', 
                                jomun_date.text if jomun_date is not None else '', 
                                jomun_content.text if jomun_content is not None else '',
                                hang_num if hang_num is not None else '',
                                hang_content if hang_content is not None else '',
                                ho_num.text if ho_num is not None else '', 
                                ho_content.text if ho_content is not None else ''])

# print(data1)
df_lawcont = pd.DataFrame(data=data1, columns=['법령ID','조문번호','조문여부','조문제목','조문시행일자','조문내용','항번호','항내용','호번호','호내용'])
df_lawcont.to_csv('data/1.csv', index=False)