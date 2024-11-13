from db_info import user, password, host, port, database
import pandas as pd
import mysql.connector
import re

db_connection = mysql.connector.connect(
user = user,
password = password,
host = host,
port = port,
database = database,
)

cursor = db_connection.cursor()

cursor.execute("select * from labor_content")

result = cursor.fetchall()

df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])

df['참조판례']=df['참조판례'].fillna('참조판례 없음') #공백은 '참조판례 없음'으로 대체함.

#참조판례 정리
clean_part=[]
for part in df['참조판례']:
    part = part.strip()
    part = re.sub(r'[\[\]［］].*?[\]\］]', '', part)  # 대괄호와 그 안의 내용 제거
    part = re.sub(r'\s*[가-힣]\.\s*', '', part)  # '가.', '나.', '다.'와 같은 패턴 제거
    part = part.strip('<br/>')  # 공백 제거
    part = part.replace('/', ',')  # '/'를 ','로 변경
    part = re.sub(r'\s+', ' ', part).strip()
    clean_part.append(part)

df['참조판례']=clean_part