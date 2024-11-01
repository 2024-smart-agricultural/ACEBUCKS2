import requests
import os

# KAMIS API 키 가져오기
api_key = os.getenv("KAMIS_KEY")  # GitHub Secrets에서 불러온 API 키

# API 엔드포인트 URL
url = 'http://www.kamis.or.kr/service/price/xml.do?action=periodProductList'  # 실제 KAMIS API 엔드포인트로 바꾸기

# 요청 파라미터 설정
params = {
    'key': api_key,
    'p_cert_key': 'YOUR_KEY',         # 발급받은 API 키
    'p_cert_id': 'YOUR_API_ID',           # 발급받은 사용자 ID
    'p_returntype': 'json',               # JSON 형식으로 응답 받기
    'p_startday': '20240101',             # 시작 날짜
    'p_endday': '20241231',               # 종료 날짜
    'p_productclscode': '01',             # 소매 가격 조회
    'p_itemcategorycode': '200',          # 예: 과일 부류 코드
    'p_itemcode': '225',                  # 예: 사과 품목 코드
    'p_kindcode': '00',                   # 특정 품종 코드 (없으면 00으로)
    'p_productrankcode': '01',            # 1등급
    'p_countrycode': '3511',              # 서울 지역
    'p_convert_kg_yn': 'Y'                # kg 단위로 환산
}

# API 호출
response = requests.get(url, params=params)

# 응답 데이터 확인
if response.status_code == 200:
    data = response.json()  # JSON 형태로 응답을 받을 경우
    print("데이터 가져오기 성공:", data)
else:
    print(f"API 호출 실패: {response.status_code}")
