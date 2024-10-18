#lawSearch_total.csv db로 저장
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from db_info import user, password, host, port, database

df = pd.read_csv('data/lawSearch_total.csv')

user = user
password = password
host = host
port = port
database = database

# MySQL 데이터베이스 연결 설정
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}', echo=False)

# 데이터프레임을 MySQL 테이블에 저장 
df.to_sql(name='injury_list', con=engine, if_exists='replace', index=False)

# 연결 닫기
engine.dispose()

print("데이터베이스 저장완료")