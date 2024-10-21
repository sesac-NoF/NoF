#lawSearch_total.csv db로 저장
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import LONGTEXT, TEXT
from db_info import user, password, host, port, database

# dtype = {
#     '법령일련번호' : INT,
#     '현행연혁코드': TEXT,
#     '벌령명한글': TEXT,
#     '법령약칭명': TEXT,
#     '법령ID': TEXT,
#     '공포일자': TEXT,
#     '공포번호': TEXT,
#     '제개정구분명': TEXT,
#     '소관부처코드': TEXT,
#     '소관부처명': TEXT,
#     '법령구분명': TEXT,
#     '시행일자': TEXT,
#     '법령상세링크': TEXT,
# }

df = pd.read_csv('data/laws_original.csv')

user = user
password = password
host = host
port = port
database = database


# MySQL 데이터베이스 연결 설정
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}', echo=False)

# 데이터프레임을 MySQL 테이블에 저장 
df.to_sql(name='law_content', con=engine, if_exists='replace', index=False)

# 연결 닫기
engine.dispose()

print("데이터베이스 저장완료")