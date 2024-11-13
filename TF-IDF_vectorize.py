from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# 피클 파일에서 Series 불러오기
with open('data/okt.pkl', 'rb') as f:
    normalized = pickle.load(f)
    
#불용어 읽어오기
stopwords_file_path = 'stopwords.txt'
stopwords = []
with open(stopwords_file_path, 'r', encoding='utf-8') as file:
    stopwords = [line.strip() for line in file.readlines()]

def remove_stopwords(text): # 불용어 제거함수
    tokens = text.split() 
    filtered_tokens = [word for word in tokens if word not in stopwords] 
    return ' '.join(filtered_tokens)  

normalized_cleaned = [remove_stopwords(' '.join([word for word in text.split() if word not in stopwords])) for text in normalized]

# TF-IDF 벡터라이저 적용
vectorizer = TfidfVectorizer(min_df=2, max_df=0.95)
tfidf_matrix = vectorizer.fit_transform(normalized_cleaned)