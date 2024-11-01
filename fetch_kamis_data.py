import requests
import os
import json

# KAMIS API 키 가져오기
api_key = os.getenv("KAMIS_KEY")  # GitHub Secrets에서 불러온 API 키

# API 엔드포인트 URL
url = 'http://www.kamis.or.kr/service/price/xml.do?action=periodProductList'  # 실제 KAMIS API 엔드포인트로 바꾸기

# 요청 파라미터 설정
params = {
    'p_cert_key': 'KAMIS_KEY',                # 발급받은 API 키
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

    # 응답 데이터가 제대로 있는지 확인
    if isinstance(data.get('data'), list):
        filtered_data = []
        for item in data['data']:
            item_data = {
                "condition": data.get('condition', ''),  # 요청 메시지
                "data": data.get('data', ''),            # 응답 코드 또는 메시지
                "itemname": item.get('itemname', ''),    # 품목명
                "kindname": item.get('kindname', ''),    # 품종명
                "countyname": item.get('countyname', ''),# 시군구
                "marketname": item.get('marketname', ''),# 마켓명
                "yyyy": item.get('yyyy', ''),            # 연도
                "regday": item.get('regday', ''),        # 날짜
                "price": item.get('price', '')           # 가격
            }
            filtered_data.append(item_data)


        # JSON 파일로 저장
        with open('kamis_data.json', 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)
        print("JSON 파일로 저장 성공: kamis_data.json")

    else:
        # data가 리스트가 아닐 때, 오류 메시지 출력
        print("오류가 발생했습니다.")
        print("오류 코드 또는 메시지:", data.get('data'))

else:
    print(f"API 호출 실패: {response.status_code}")
    print("응답 내용:", response.text)
