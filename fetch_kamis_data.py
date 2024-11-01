import requests
import os
import json
from dataclasses import dataclass, asdict
from typing import Dict, Union, List


@dataclass
class Certification:
    """KAMIS API 인증 정보를 담는 데이터 클래스입니다."""
    cert_key: str
    cert_id: str


@dataclass
class PeriodProductListParams:
    """KAMIS API의 기간별 상품 목록 요청 파라미터를 정의하는 데이터 클래스입니다."""
    p_startday: str
    p_endday: str
    p_productclscode: str = '01'
    p_itemcategorycode: str = '200'
    p_itemcode: str = '225'
    p_kindcode: str = '00'
    p_productrankcode: str = '01'
    p_countrycode: str = '3511'
    p_convert_kg_yn: str = 'Y'
    p_returntype: str = 'json'


class KamisOpenApiClient:
    """KAMIS 오픈 API 클라이언트 클래스입니다."""
    
    def __init__(self, cert: Certification, base_url: str = "http://www.kamis.or.kr/service/price/xml.do"):
        self.cert = cert
        self.base_url = base_url

    def build_url(self, action: str, params: Dict[str, Union[str, List[str]]]) -> str:
        """API 엔드포인트 URL을 생성합니다."""
        params_with_cert = {
            **asdict(params),
            'action': action,
            'p_cert_key': self.cert.cert_key,
            'p_cert_id': self.cert.cert_id,
            'p_returntype': 'json',
        }
        return f"{self.base_url}?{requests.compat.urlencode(params_with_cert)}"

    def request(self, action: str, params: PeriodProductListParams) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """KAMIS API에 요청을 보내고 JSON 응답을 반환합니다."""
        url = self.build_url(action, params)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def period_product_list(self, params: PeriodProductListParams) -> List[Dict[str, str]]:
        """기간별 상품 목록을 요청하고 데이터를 파싱하여 반환합니다."""
        response_data = self.request('periodProductList', params)
        
        # 오류 코드가 있으면 오류 메시지 반환
        if isinstance(response_data.get('data'), str):
            print("오류 발생:", response_data['data'])
            return []

        # 데이터 필드가 정상적으로 반환된 경우
        parsed_data = []
        for item in response_data['data']:
            parsed_item = {
                'countyname': item.get('countyname', ''),
                'itemname': item.get('itemname', ''),
                'kindname': item.get('kindname', ''),
                'unit': item.get('unit', ''),
                'price': item.get('price', ''),
                'weekprice': item.get('weekprice', ''),
                'monthprice': item.get('monthprice', ''),
                'yearprice': item.get('yearprice', '')
            }
            parsed_data.append(parsed_item)
        return parsed_data

    def save_to_json(self, data: List[Dict[str, str]], filename: str = 'kamis_data.json') -> None:
        """데이터를 JSON 파일로 저장합니다."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"{filename} 파일로 저장 성공")


# 사용 예제
if __name__ == "__main__":
    # 환경 변수에서 인증 정보 불러오기
    cert = Certification(
        cert_key=os.getenv("KAMIS_KEY", "YOUR_KAMIS_KEY"),
        cert_id=os.getenv("P_CERT_ID", "YOUR_CERT_ID")
    )
    client = KamisOpenApiClient(cert)

    # 요청 파라미터 설정
    params = PeriodProductListParams(
        p_startday='20240101',
        p_endday='20241231'
    )

    # API 호출 및 데이터 저장
    data = client.period_product_list(params)
    if data:
        client.save_to_json(data)
