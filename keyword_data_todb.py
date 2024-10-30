# db로 저장
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import LONGTEXT, TEXT
from db_info import user, password, host, port, database

####pandas dataframe에서는 불러올때 타입을 기본str로 불러와서 긴내용의 데이터삽입을 하려면 dtype을 설정해줘야함####
dtype = {
    '판례내용' : LONGTEXT,
    '판시사항': TEXT,
    '판결요지': TEXT,
    '참조조문': TEXT,
    '참조판례': TEXT,
    '판례내용_이유': LONGTEXT,
    '판례내용_상단': LONGTEXT,
    '판례내용_이유(전처리)': LONGTEXT,
    '판례내용_이유(불용어제거)': LONGTEXT
}
#판례내용_이유,판례내용_이유(전처리),판례내용_이유(불용어제거),클러스터,키워드

# DB정보
user = user
password = password
host = host
port = port
database = database

# CSV 파일 로드
# df_injury = pd.read_csv('data/상해_본문2.csv')
# df_fraud = pd.read_csv('data/사기_본문2.csv')
# df_inheritance = pd.read_csv('data/상속_본문2.csv')
# df_labor = pd.read_csv('data/근로_본문2.csv')
df_fraud_keyword = pd.read_csv('data/df_fraud_keyword.csv')

# MySQL 데이터베이스 연결 설정
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# 데이터프레임을 MySQL 테이블에 저장
# df_injury.to_sql(name='injury_content', con=engine, if_exists='replace', index=False, dtype=dtype)
# df_fraud.to_sql('fraud_content', con=engine, if_exists='replace', index=False, dtype=dtype)
# df_inheritance.to_sql('inheritance_content', con=engine, if_exists='replace', index=False, dtype=dtype)
# df_labor.to_sql('labor_content', con=engine, if_exists='replace', index=False, dtype=dtype)
df_fraud_keyword.to_sql('fraud_keyword', con=engine, if_exists='replace', index=False, dtype=dtype)

# 연결 닫기
engine.dispose()

print("데이터베이스 저장 완료")
