import re
from db_info import user, password, host, port, database
import pandas as pd
import mysql.connector

#MySQL을 통해 판례목록과 본문을 결합한 데이터 로드
db_connection = mysql.connector.connect(
user = user,
password = password,
host = host,
port = port,
database = database,
)
cursor = db_connection.cursor()
cursor.execute("select * from injury_list il inner join injury_content ic on il.판례일련번호=ic.판례정보일련번호") 
result = cursor.fetchall()
df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])


df['판례내용'] = df['판례내용'].apply(lambda x: re.sub(r'\[이\s+유\]', '【이    유】', x))
df['판례내용'] = df['판례내용'].replace(r'\s{2,}', ' ', regex=True) #공백의 길이가 2개 이상이면 1개로 변환

# '【이' 앞부분과 '【이'를 포함한 뒷부분으로 나누는 코드
df['판례내용_상단'] = df['판례내용'].str.split('【이').str[0]
df['판례내용_이유'] = df['판례내용'].str.extract(r'(【이.*?】.*)') 


# 새로운 리스트를 생성하여 전처리된 데이터를 저장
service_reason = []

for idx in range(len(df)):
    content = df['판례내용_이유'].iloc[idx]  
    if isinstance(content, str):
        # 이유의 내용을 분리
        content_parts = re.split(r'유】', content)
        reason_dict = {}
        for j in range(len(content_parts)):
            if content_parts[j].replace(' ', '') == '【이':
                cleaned_content = content_parts[j+1] #【이유】뒤의 내용
                cleaned_content = re.sub(r'<br/>|\r|\n|【|】', '',cleaned_content).strip()
                cleaned_content = re.sub(r'\s+', ' ', cleaned_content)  
                # 결과를 딕셔너리에 저장
                reason_dict['이유'] = cleaned_content
        
        # 전처리된 내용을 리스트에 추가
        service_reason.append(reason_dict)
    else:
        # 비문자열 데이터 처리 (빈 딕셔너리 추가)
        service_reason.append({})

# 결과를 '판례내용_이유(전처리)' 열에 저장
df['판례내용_이유_전처리'] = service_reason
