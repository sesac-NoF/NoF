from db_info import user, password, host, port, database
import pandas as pd
import mysql.connector
import re
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import LONGTEXT, TEXT

def clean_clause(text): #참조조문 클리닝

    # '1.\n', '2.\n' 등의 숫자 뒤에 마침표와 줄바꿈이 있는 패턴 제거
    text = re.sub(r'\d+\.\s*', '', text)
    # '\n' 줄바꿈 문자를 공백으로 대체
    text = text.replace('\n', ' ')
    groups=text.replace('<br/>','').replace('[증명책임]','').replace('/',',').replace('내지',',').split(',')
    groups=[group for group in groups if group.strip() != '']
    results = []
    
    for group in groups:
        group = group.strip()  # 각 그룹의 양쪽 공백 제거
        group=re.sub(r'(가|나|다|라|마|바|사|아|자|차|카|타|파|하)\.', '', group) # 가., 나., 다., 라., 마., 바., 사., 아., 자., 차., 카., 타., 파., 하. 댜. 형태만 제거
        group=re.sub(r'(갸|냐|댜|랴|먀|뱌|샤|야|쟈|챠|캬|탸|퍄|햐)\.', '', group) # 가나다라의 오타도 제거
        
        group=re.sub(r'[\[\［]\d+[\]\］]\s*', '', group)  # '[1]', '[2]' 형식 제거
        group = group.strip()  # 각 그룹의 양쪽 공백 제거
        # 쉼표로 나눠 조각을 분리
        parts = re.split(r',\s*', group)                

        transformed_parts = []

        for part in parts:    # 조, 항, 호 뒤에 문자가 붙어 있는 경우 처리

            # 조, 항, 호 뒤에 괄호와 공백 없는 문자가 있는 경우 공백 추가 (괄호 예외 처리) 
            part = re.sub(r'([0-9]+조|[0-9]+항|[0-9]+호)(?![\s\(\[])', r'\1 ', part)          
            
            part = part.strip()
            # 변환된 조문 추가
            transformed_parts.append(part)

        # 각 그룹을 쉼표로 연결하고 결과에 추가
        if transformed_parts:  # transformed_parts가 비어있지 않으면
            results.append(', '.join(transformed_parts))

    # 전체 결과를 반환
    return ', '.join(results) 

def extract_law_names(series): #참조조문에서 법 이름 추출
    law_names_set=set()
    pattern = r'([가-힣]+?(법\s*시행령|시행령|에\s*관한\s*법률|시행규칙|규칙|협정|의사록|관례|고시|대통령령|경제명령|법|령)(\([^)]*\))?)'
    # 정규 표현식을 사용하여 괄호를 기준으로 분리
    
    def split_outside_parentheses(text): #괄호 안의 쉼표는 분리 기준 아니게
        result = []
        start = 0
        stack = []  # 괄호 스택

        for i, char in enumerate(text):
            if char in "{(":
                stack.append(char)  # 괄호 열기
            elif char in "})" and stack:
                stack.pop()  # 괄호 닫기
            elif char == "," and not stack:
                # 스택이 비어 있을 때의 쉼표는 분리 기준
                result.append(text[start:i].strip())
                start = i + 1

        # 마지막 남은 부분 추가
        result.append(text[start:].strip())
        return result

    for text in series:
        # 1. 쉼표로 문자열을 분리 (괄호 안 쉼표 무시)
        parts = split_outside_parentheses(text)
        for part in parts:
            # 불필요한 \n 및 공백 제거
            part = re.sub(r'\n+', ' ', part)
            part = re.sub(r'\s+', ' ', part)  # 여러 공백을 하나로 줄임
            part = re.sub(r'[\[\]]', '', part)  # [] 괄호 제거
            part = re.sub(r'〔\d+〕', '', part)
            part = part.strip()
            part = re.sub(r'\{[^}]*\}', '', part)  # 중괄호 안의 내용 제거

            split_pattern = r'([^()]*)(\s*\([^()]*\))?'

            matches = re.findall(split_pattern, part)
            matches = [(off_maren.replace(',', '').strip(), maren.strip()) for off_maren, maren in matches]

            for match in matches:
                before_parentheses = match[0].strip()  # 괄호 이전 내용
                in_parentheses = match[1].strip() if match[1] else ''  # 괄호 내용
                # '숫자. ' 형식이 있다면 제거
                before_parentheses = re.sub(r'^\d+\.\s*', '', before_parentheses)
                # print('in: ',in_parentheses)

                # 법 이름 추출: 중괄호가 제거된 `before_parentheses`에서 패턴 찾기
                match = re.search(pattern, before_parentheses)
                if match:
                    # 패턴이 일치하는 위치까지 추출
                    law_name = before_parentheses[:match.end()] + in_parentheses
                    if len(law_name) > 1:  # 길이가 1보다 큰 경우만 추가
                        law_names_set.add(law_name)

    return list(law_names_set)

def clean_extracted_law_names(law_names):
    #법 이름 앞에 '구'와 법 이름 뒤 괄호 제거함수
    cleaned_law_names = []
    # 패턴 뒤의 괄호와 '구 ' 접두사 제거
    for law in law_names:
        # "제3조", "제4항", "제5호", "제6목" 등과 같은 패턴 제거
        law = re.sub(r'제\d+(조|항|호|목)\s*', '', law)
        
        # '구 ' 접두사 제거
        law = law.replace('구 ', '')
        
        # 패턴 뒤의 괄호 제거
        # 예: "폭력행위 등 처벌에 관한 법률(2014. 12. 30. 법률 제12896호로 개정되기 전의 것)" -> "폭력행위 등 처벌에 관한 법률"
        law = re.sub(r'(부칙|법\s*시행령|시행령|에\s*관한\s*법률|시행규칙|규칙|협정|의사록|관례|고시|대통령령|경제명령|법|령)\S(\([^)]*\))', r'\1', law)
        
        # 앞쪽의 마침표와 공백 제거
        law = re.sub(r'^\s*\.?\s*', '', law)        

        # '\\ ' 제거
        law = re.sub(r'\\\s*', '', law)
                
        cleaned_law_names.append(law.strip())  # 최종적으로 공백 제거 후 리스트에 추가
    
    return cleaned_law_names

def add_law_prefix(x): # 법과 시행령 이름을 붙이는 함수 
    if isinstance(x, str):  
        previous_law = None  # 이전 법 이름 저장
        new_references = []
        
        # 쉼표를 기준으로 나누되, 괄호 안의 쉼표는 무시
        parts = re.split(r',(?![^()]*\))', x)
        
        for part in parts:
            part = part.strip()
            part = re.sub(r'[\[\]［］].*?[\]\］]', '', part)
            part = re.sub(r'\s*[가-힣]\.\s*', '', part)
            part = part.strip('<br/>')
            part = part.replace('/', ',')
            part = re.sub(r'\s+', ' ', part).strip()
            # print(previous_law)

            # '같은법', '같은 법', '동법'이 어디에든 등장하면 previous_law로 대체
            if previous_law:
                # print('이전법 :',previous_law)
                part = re.sub(r'(같은\s*법|같은\s*령|같은\s*시행령|같은\s*규칙|같은\s*시행규칙|같은\s*법령|같은\s*법률|같은\s*령\s*시행규칙|동법)', previous_law, part)
                # print('변경된 파트: ',part)

            # 현재 조각에 법 이름이 있는 경우, previous_law 업데이트
            for law_name in law_names:
                if law_name in part:
                   law_name = law_name.replace('구 ', '')
        
                   # 패턴 뒤의 괄호 제거
                   law_name = re.sub(r'(부칙|법\s*시행령|시행령|에\s*관한\s*법률|시행규칙|규칙|협정|의사록|관례|고시|대통령령|경제명령|법|령)(\([^)]*\))', r'\1', law_name)   

                   previous_law = law_name  # 이전 법 이름을 현재 법 이름으로 설정

                   part = re.sub(r'구\s*', '', part)  # 구문에서 '구 ' 제거

                   part = re.sub(r'(부칙|법\s*시행령|시행령|에\s*관한\s*법률|시행규칙|규칙|협정|의사록|관례|고시|대통령령|경제명령|법|령)(\([^)]*\))', r'\1', part)

                   break
                
            match = re.search(r'현행\s*([^)]*?)\)', part)  # "현행"과 "참조" 사이의 내용만 추출

            if match is None:
                # 1-1. "(현행 ~ 참조)"가 없고 previous_law 존재하고 part에 없는 경우, 법 이름을 붙인다.
                if previous_law and re.match(r'제\d+조', part) and not any(law in part for law in law_dup_reduce) and previous_law not in part:
                    part = f"{previous_law} {part}"
                    
            else:
                # "(현행 ~ 참조)"가 존재하는 경우
                content_between = match.group(1)

                # 2. "(현행 ~ 참조)" 구문 안에 법 이름 패턴이 있는지 확인
                in_pattern = r'([가-힣]+?(법\s*시행령|시행령|에\s*관한\s*법률|시행규칙|규칙|협정|의사록|관례|고시|대통령령|경제명령|법|령))'
                law_match = re.search(in_pattern, content_between)

                if law_match is None: # (현행 제34조 참조)  이런거밖에 없다는 뜻

                    # 2-1. 법 이름이 없는 경우, 괄호 밖의 법 이름을 사용하여 내용을 변환

                    if previous_law:
                        if re.search(r'제\d+조', content_between):
                            part = f"{previous_law} {content_between}"

                    else:
                        part = content_between

                else:
                    # 2-2. 법 이름이 존재하는 경우, current_law를 설정하고 ','로 나눈 후 처리
                    current_law = law_match.group(0).strip()

                    # ','로 구분된 각 조항 처리
                    references = content_between.split(',')

                    updated_references = []
                    for ref in references:
                        ref = ref.strip()
                        
                        # 2-2-1. '제%d조' 형식이 있다면 current_law를 붙이기
                        if re.match(r'제\d+조', ref):
                            ref = f"{current_law} {ref}"
                        
                        # 2-2-1. ',' 뒤에 또 다른 법 이름이 있으면 current_law 갱신
                        next_law_match = re.search(in_pattern, ref)
                        if next_law_match:
                            current_law = next_law_match.group(0).strip()
                        updated_references.append(ref)


                    # 2-3. 변환된 내용으로 part 전체를 대체
                    updated_content = ', '.join(updated_references)

                    part = updated_content
            
            # 처리된 part를 new_references에 추가
            new_references.append(part)

        # 최종 조각들을 쉼표로 결합하여 반환
        return ', '.join(new_references)
    
    return x  # 문자열이 아닐 경우 그대로 반환

def replace_laws(reason):  # 사전 정의된 법률 용어 대체 딕셔너리
    law_replacements = {
        '헌법': '대한민국헌법',
        '상속세법': '상속세 및 증여세법',
        '지가공시및토지등의평가에관한법률': '부동산 가격공시에 관한 법률',
        '매장및묘지등에관한법률': '장사 등에 관한 법률'
    }
    
    # Series 내 각 항목에 대해 대체 수행
    for old, new in law_replacements.items():
        reason = reason.str.replace(old, new, regex=False)
    # "참조"라는 글자가 나오면 제거
    reason = reason.str.replace('참조', '', regex=False)
    reason = reason.str.replace('시행령시행령', '시행령', regex=False)

    return reason

def extract_JoandLaw(text): #참조조문 법 이름과 조 만 살려두기
    pattern=r'\b[가-힣\s]+(?:부칙|법\s*시행령|시행령|에\s*관한\s*법률|시행규칙|규칙|협정|의사록|관례|고시|대통령령|경제명령|법|령)? 제\d+조'
    matches=re.findall(pattern,text)

    # 모든 요소에서 "현행" 제거
    matches = [match.replace('현행', '').strip() for match in matches]

    # 각 요소가 "및"으로 시작하는 경우에만 "및" 제거
    matches = [match[1:].strip() if match.startswith('및') else match for match in matches]


    return ', '.join(matches)

def process_clause(row): #같은~pattern과 동법 처리
    # 각 항목을 쉼표로 나눔
    parts = row.split(',')
    processed_parts = []
    # 이전 항목을 저장할 변수
    prev_part = ""
    
    for part in parts:
        part = part.strip()  # 공백 제거
        # "같은법" 또는 "동시행령"이 포함된 경우
        if re.search(r'같은\s*법|같은\s*령|같은\s*시행령|같은\s*규칙|같은\s*시행규칙|같은\s*법령|같은\s*법률|같은\s*령\s*시행규칙|동법', part): #해당사항만 늘려가자
            # 이전 항목이 있고 '/'가 있다면 '/' 앞의 문자열에서 마지막 ',' 이후의 내용을 추출
            if prev_part and '/' in prev_part:
                ref_part = prev_part.rsplit('/', 1)[0]  # '/' 기준으로 나누기
                # 마지막 쉼표 이후의 내용을 추출
                aft_part = part.rsplit('/', 1)[0]
                aft_part=ref_part +'/' + part.rsplit('/', 1)[1]
                processed_parts.append(aft_part)
            else:
                processed_parts.append(part)  # 이전 항목이 없으면 그대로 추가
        else:
            # 이전 항목 저장
            processed_parts.append(part)
            prev_part = part  # 현재 항목을 이전 항목으로 저장
    
    return ', '.join(processed_parts)



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

df['참조조문']=df['참조조문'].fillna('참조조문 없음').replace({'\n': '참조조문 없음'})
df['참조판례'] = df['참조판례'].replace({'\n': '참조판례 없음'})

ccl=df['참조조문'].apply(clean_clause)

law_names = extract_law_names(ccl)
law_names_cleaned=clean_extracted_law_names(law_names)
law_dup_reduce=list(set(law_names_cleaned))
# 법 이름 길이가 긴 순서대로 정렬 (내림차순)
law_names = sorted(law_names, key=len, reverse=True)

reason=ccl.apply(add_law_prefix)
updated_reason = replace_laws(reason)

result=updated_reason.apply(extract_JoandLaw)

#제XX조 앞을 /로 분리
final=result.apply(lambda x: re.sub(r' (제\d+조)', r'/\1', x))
final=final.fillna('참조조문 없음').replace('','참조조문 없음')

finale=final.apply(process_clause)

df_preprocess=pd.DataFrame(data=df['판례정보일련번호'])
df_preprocess['참조조문_1차전처리']=ccl
df_preprocess['참조조문_전처리']=updated_reason
df_preprocess['참조조문_파라미터']=finale
df_preprocess['참조판례_전처리']=df['참조판례']
df_preprocess.to_csv('data/injury_case_clause_preprocessed.csv',index=False)

####pandas dataframe에서는 불러올때 타입을 기본str로 불러와서 긴내용의 데이터삽입을 하려면 dtype을 설정해줘야함####
dtype = {
    '참조조문_1차전처리': TEXT,
    '참조조문_전처리': TEXT,
    '참조조문_파라미터': TEXT,
    '참조판례_전처리': TEXT
}
#판례내용_이유,판례내용_이유(전처리),판례내용_이유(불용어제거),클러스터,키워드

# DB정보
user = user
password = password
host = host
port = port
database = database

# CSV 파일 로드
df_injury_case_clause_preprocessed = pd.read_csv('data/injury_case_clause_preprocessed.csv')

# MySQL 데이터베이스 연결 설정
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# 데이터프레임을 MySQL 테이블에 저장
df_injury_case_clause_preprocessed.to_sql('injury_case_clause_preprocessed', con=engine, if_exists='replace', index=False, dtype=dtype)
# 연결 닫기
engine.dispose()

print("데이터베이스 저장 완료")