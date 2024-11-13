import pandas as pd
import re
import csv

df = pd.read_csv('data/lawService_dh.csv') #데이터 로드

# 판례내용을 분리하고 <br/>, \n 제거
CASE_CONTENT = df['판례내용'].replace('<br/>', '').replace('\n', '')

split_cont = CASE_CONTENT.split('【') # 【 기준으로 split

# split 한 내용 】 로 한번더 split 해서 컬럼과 내용으로 구분
data_split = {}
for i in range(1,len(split_cont)):
    print(split_cont[i])
    split_cont2 = split_cont[i].split('】')
    col = split_cont2[0]
    val = split_cont2[1].strip()
    data_split[col] = val

con_data = []  # 데이터프레임에서 추출한 '【】'안의 내용들을 담을 리스트
for i in range(len(df)):
    content = df['판례내용'].iloc[i]
    content = content.replace('<br/>', '').replace('\n', '')
    # 판례내용을 분리하고 <br/>, \n 제거

    val = re.split(r'【+.*?】+', content) #'【】'밖의 내용
    col = re.findall(r'【+(.*?)】+', content) #'【】'안의 내용
    split_datas = {}
    for j in range(1, len(val)):
        val[j] = val[j].strip()
        val[j] = re.sub(r'\s+', ' ', val[j])
        col[j-1] = col[j-1].replace(' ','')
        split_datas[col[j-1]] = val[j]
    con_data.append(split_datas)

result = set() #법률용어사전용 단어 추출
for i in range(len(con_data)):
    x = set(con_data[i].keys())
    result = set.union(result, x)

result_list = list(result)
# 리스트를 CSV 파일로 저장하기
with open("data/detail_list.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(result_list)