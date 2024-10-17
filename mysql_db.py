#lawSearch_total.csv db로 저장
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from db_info import user, password, host, port, database

df = pd.read_csv('data/lawSearch_total.csv')
df_injury = pd.read_csv('data/상해_목록.csv')
df_fraud = pd.read_csv('data/사기_목록.csv')
df_inheritance = pd.read_csv('data/상속_목록.csv')
df_labor = pd.read_csv('data/근로_목록.csv')


user = user
password = password
host = host
port = port
database = database

# MySQL 데이터베이스 연결 설정
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}', echo=False)

# 데이터프레임을 MySQL 테이블에 저장 
df_injury.to_sql(name='injury_list', con=engine, if_exists='replace', index=False)
df_fraud.to_sql(name='fraud_list', con=engine, if_exists='replace', index=False)
df_inheritance.to_sql(name='inheritance_list', con=engine, if_exists='replace', index=False)
df_labor.to_sql(name='labor_list', con=engine, if_exists='replace', index=False)

# 연결 닫기
engine.dispose()

print("데이터베이스 저장완료")