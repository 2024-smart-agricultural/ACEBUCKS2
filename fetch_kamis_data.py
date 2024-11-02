import requests
import os
import json

# KAMIS API 키 가져오기
api_key = os.getenv("KAMIS_KEY")  # GitHub Secrets에서 불러온 API 키
cert_id = os.getenv("P_CERT_ID")  # GitHub Secrets에서 불러온 인증 ID

# API 엔드포인트 URL
url = 'http://www.kamis.or.kr/service/price/xml.do?action=periodRetailProductList'

# 요청 파라미터 설정
params = {
    'p_cert_key': api_key,
    'p_cert_id': cert_id,
    'p_returntype': 'json',               # JSON 형식으로 응답 받기
    'p_startday': '20240103',             # 시작 날짜
    'p_endday': '20241031',               # 종료 날짜
    'p_productclscode': '01',             # 소매 가격 조회
    'p_itemcategorycode': '200',          # 특정 부류 코드
    'p_itemcode': '225',                  # 특정 품목 코드
    'p_kindcode': '00',                   # 특정 품종 코드
    'p_productrankcode': '01',            # 등급 코드
    'p_countycode': '1101',               # 서울 지역
    'p_convert_kg_yn': 'Y'                # kg 단위로 환산
}

# API 호출
response = requests.get(url, params=params)

# 응답 데이터 확인 및 JSON 파일로 저장
if response.status_code == 200:
    data = response.json()
    
    # 에러 코드 확인
    error_code = data.get("error_code", "")
    if error_code == "000":
        print("Success: 데이터를 정상적으로 가져왔습니다.")
        
        # 응답 데이터에서 필요한 정보를 추출
        item_data_list = []
        for item in data.get('data', []):
            item_data = {
                "itemname": item.get("itemname", ""),
                "kindname": item.get("kindname", ""),
                "countyname": item.get("countyname", ""),
                "marketname": item.get("marketname", ""),
                "yyyy": item.get("yyyy", ""),
                "regday": item.get("regday", ""),
                "price": item.get("price", "")
            }
            item_data_list.append(item_data)
        
        # JSON 파일로 저장
        with open("kamis_data.json", "w", encoding="utf-8") as f:
            json.dump(item_data_list, f, ensure_ascii=False, indent=4)
        print("JSON 파일로 저장 성공: kamis_data.json")
        
    elif error_code == "001":
        print("No Data: 요청 조건에 맞는 데이터가 없습니다.")
    elif error_code == "200":
        print("Wrong Parameters: 잘못된 파라미터가 포함되었습니다.")
    elif error_code == "900":
        print("Unauthenticated request: 인증에 실패하였습니다. 인증 키와 ID를 확인하세요.")
    else:
        print("알 수 없는 에러 코드:", error_code)

else:
    print(f"API 호출 실패: {response.status_code}")
    print("응답 내용:", response.text)
