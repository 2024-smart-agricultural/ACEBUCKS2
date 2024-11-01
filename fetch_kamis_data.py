import requests
import os

# KAMIS API 키 가져오기
api_key = os.getenv("KAMIS_KEY")  # GitHub Secrets에서 불러온 API 키

# API 엔드포인트 URL
url = 'http://www.kamis.or.kr/service/price/xml.do?action=periodProductList'  # 실제 KAMIS API 엔드포인트로 바꾸기

# 요청 파라미터 설정
params = {
    'key': api_key,
    'parameter_name': 'parameter_value'  # 문서에 맞게 필요한 파라미터 설정
}

# API 호출
response = requests.get(url, params=params)

# 응답 데이터 확인
if response.status_code == 200:
    data = response.json()  # JSON 형태로 응답을 받을 경우
    print("데이터 가져오기 성공:", data)
else:
    print(f"API 호출 실패: {response.status_code}")
