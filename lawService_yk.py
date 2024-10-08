import pandas as pd
import requests
import xml.etree.ElementTree as ET
from re import I

# OC = 'ykdb0508'
# target = 'prec'
# url = 'http://www.law.go.kr/DRF/lawSearch.do?'
# data = []
# for i in range(226,451):
#   params = {
#       'OC' : OC,
#       'target' : target,
#       'type' : 'XML',
#       'display' : 100,
#       'search' : 1,
#       'page' : i
#   }

#   response = requests.get(url, params=params)

#   if response.status_code == 200:
#     root = ET.fromstring(response.content)
#     items = root.findall('.//prec')
#     # xml구조확인
#     print(ET.tostring(root, encoding='utf-8').decode('utf-8'))
#     if len(items) != 0:
#       for item in items:
#         ORDER_NUM = item.find('.//판례일련번호')
#         CASE_NAME = item.find('.//사건명')
#         CASE_NUM = item.find('.//사건번호')
#         CASE_DATE = item.find('.//선고일자')
#         SCOURT = item.find('.//법원명')
#         CASE = item.find('.//사건종류명')
#         LINK = item.find('.//판례상세링크')
#         data.append([ORDER_NUM.text, CASE_NAME.text, CASE_NUM.text, CASE_DATE.text, SCOURT.text, CASE.text, LINK.text])
#   else:
#     print('error')
# df = pd.DataFrame(data=data, columns=['판례일련번호','사건명','사건번호','선고일자','법원명','사건종류명','판례상세링크'])
# df.to_csv('df_data.csv')


import requests
import pandas as pd
import xml.etree.ElementTree as ET
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 세션 및 재시도 설정
session = requests.Session()
retry = Retry(connect=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://www.law.go.kr/DRF/lawService.do?', adapter)

# 기존 데이터 로드 및 처리 시작점 확인
try:
    df_existing = pd.read_csv('df_data2.csv')  # 기존에 저장된 파일이 있으면 불러옴
    processed_ids = df_existing['판례정보일련번호'].tolist()  # 이미 처리한 판례 ID 목록
except FileNotFoundError:
    df_existing = pd.DataFrame()  # 파일이 없으면 새로운 데이터프레임 생성
    processed_ids = []  # 처리된 판례 ID가 없으므로 빈 리스트

# CSV 파일 불러오기
df = pd.read_csv('df_data.csv')

# API 요청 정보 설정
OC = 'ykdb0508'
target = 'prec'
url = 'http://www.law.go.kr/DRF/lawService.do?'
data = []

# API 요청 및 데이터 수집 루프 (중단된 곳부터 시작)
for i in range(1, df['판례일련번호'].value_counts().sum() + 1):
    case_id = df['판례일련번호'].iloc[i-1]

    # 이미 처리된 판례일련번호는 건너뜀
    if case_id in processed_ids:
        continue

    params = {
        'OC': OC,
        'target': target,
        'type': 'XML',
        'ID': case_id
    }

    try:
        # 타임아웃 시간을 늘려서 60초로 설정
        response = session.get(url, params=params, timeout=60)

        if response.status_code == 200:
            # XML 응답 데이터를 파싱
            root = ET.fromstring(response.content)
            CASE_NUM = root.find('.//사건번호')
            JUD = root.find('.//선고')
            JUD_TYPE = root.find('.//판결유형')
            ISSUE = root.find('.//판시사항')
            SUMMARY_JUD = root.find('.//판결요지')
            REF_STAT = root.find('.//참조조문')
            REF_CASE = root.find('.//참조판례')
            CASE_CONTENT = root.find('.//판례내용')

            # 수집한 데이터를 리스트에 추가
            data.append([
                case_id,
                CASE_NUM.text if CASE_NUM is not None else None,
                JUD.text if JUD is not None else None,
                JUD_TYPE.text if JUD_TYPE is not None else None,
                ISSUE.text if ISSUE is not None else None,
                SUMMARY_JUD.text if SUMMARY_JUD is not None else None,
                REF_STAT.text if REF_STAT is not None else None,
                REF_CASE.text if REF_CASE is not None else None,
                CASE_CONTENT.text if CASE_CONTENT is not None else None
            ])
        
        else:
            print(f"{i} error: Status code {response.status_code}")

    except requests.exceptions.Timeout:
        print(f"Timeout occurred on record {i} / 판례일련번호: {case_id}. Retrying...")
        continue  # 타임아웃 발생 시 루프를 계속 진행

    except requests.exceptions.ConnectionError:
        print(f"Connection error on record {i}. Saving progress and retrying...")
        break  # 연결 오류가 발생하면 중단하고 저장 후 재시작할 수 있도록 함

    # 처리한 판례일련번호를 출력
    print(f"Processed record {i} / 판례일련번호: {case_id}")
    
    # 일정 간격으로 중간 저장 (10번째 루프마다)
    if i % 10 == 0 or i == df['판례일련번호'].value_counts().sum():
        # 수집된 데이터를 데이터프레임으로 변환
        df_temp = pd.DataFrame(data=data, columns=[
            '판례정보일련번호', '사건번호', '선고', '판결유형', '판시사항', '판결요지', '참조조문', '참조판례', '판례내용'
        ])
        
        # 기존 데이터에 새로운 데이터를 추가하여 저장
        df_combined = pd.concat([df_existing, df_temp], ignore_index=True)
        df_combined.to_csv('df_data2.csv', index=False)
        
        # 새로운 데이터는 중간 저장 후 초기화
        data = []
        df_existing = df_combined  # 기존 데이터 업데이트

        print(f"Checkpoint: Data saved up to record {i}")

