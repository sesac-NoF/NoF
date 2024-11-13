from konlpy.tag import Okt
import pandas as pd
from db_info import user, password, host, port, database
import mysql.connector

#데이터 로드
db_connection = mysql.connector.connect(
user = user,
password = password,
host = host,
port = port,
database = database,
)
cursor = db_connection.cursor()
cursor.execute("select * from injury_content")
result = cursor.fetchall()
df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
df['판례내용'] = df['판례내용'].fillna('') #NaN값 처리

#Okt호출
okt = Okt()
#정규화한 뒤 명사추출
normalized = df['판례내용'].apply(lambda x: ' '.join(okt.nouns(okt.normalize(x))))


