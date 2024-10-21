#lawSearch_total.csv db로 저장
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import LONGTEXT, TEXT
from db_info import user, password, host, port, database

dtype = {
    '판례내용' : LONGTEXT,
    '판시사항': TEXT,
    '판결요지': TEXT,
    '참조조문': TEXT,
    '참조판례': TEXT,
}

df = pd.read_csv('data/lawService_total.csv')

user = user
password = password
host = host
port = port
database = database


# MySQL 데이터베이스 연결 설정
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}', echo=False)

# 데이터프레임을 MySQL 테이블에 저장 
df.to_sql(name='law_service_table', con=engine, if_exists='replace', index=False, dtype=dtype)

# 연결 닫기
engine.dispose()

print("데이터베이스 저장완료")