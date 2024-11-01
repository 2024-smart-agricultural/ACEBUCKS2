import requests
import os
import json

# KAMIS API 키 가져오기
api_key = os.getenv("KAMIS_KEY")  # GitHub Secrets에서 불러온 API 키

# API 엔드포인트 URL
url = 'http://www.kamis.or.kr/service/price/xml.do?action=periodProductList'  # 실제 KAMIS API 엔드포인트로 바꾸기

# 요청 파라미터 설정
params = {
    'p_cert_key': api_key,                # 발급받은 API 키
    'p_cert_id': 'P_CERT_ID',             # 발급받은 사용자 ID
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

# 응답 데이터 확인 및 JSON 파일로 저장
if response.status_code == 200:
    data = response.json()  # JSON 형태로 응답을 받음
    print("API 응답 데이터 전체:", data)  # 전체 데이터 구조를 출력해 확인

    # JSON 파일로 저장 (필요시 전체 데이터 저장)
    with open('kamis_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("JSON 파일로 저장 성공: kamis_data.json")

else:
    print(f"API 호출 실패: {response.status_code}")
    print("응답 내용:", response.text)  # 에러 발생 시 응답 내용 출력
