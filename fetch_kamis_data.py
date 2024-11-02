import requests
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom

# KAMIS API 키 가져오기
api_key = os.getenv("KAMIS_KEY")  # GitHub Secrets에서 불러온 API 키
cert_id = os.getenv("P_CERT_ID")  # GitHub Secrets에서 불러온 인증 ID

# API 엔드포인트 URL
url = 'http://www.kamis.or.kr/service/price/xml.do?action=periodRetailProductList'

# 요청 파라미터 설정
params = {
    'p_cert_key': api_key,
    'p_cert_id': cert_id,
    'p_returntype': 'xml',
    'p_startday': '20240103',
    'p_endday': '20241031',
    'p_productclscode': '01',
    'p_itemcategorycode': '200',
    'p_itemcode': '225',
    'p_kindcode': '00',
    'p_productrankcode': '04',
    'p_countycode': '1101',
    'p_convert_kg_yn': 'Y'
}

# API 호출
response = requests.get(url, params=params)

# 응답 데이터 확인 및 XML 파일로 저장
if response.status_code == 200:
    # XML 데이터 파싱
    root = ET.fromstring(response.content)
    
    # 새 XML 문서 생성
    document = Element('document')
    condition = SubElement(document, 'condition')
    condition_item = SubElement(condition, 'item')

    # 요청 파라미터를 condition 부분에 추가
    for key, value in params.items():
        param = SubElement(condition_item, key)
        param.text = value

    # data 부분을 추가
    data = SubElement(document, 'data')
    error_code = SubElement(data, 'error_code')
    error_code.text = root.find('.//error_code').text if root.find('.//error_code') is not None else ''

    # XML 응답에서 item 요소를 찾고 각 항목을 data에 추가
    for item in root.findall(".//item"):
        data_item = SubElement(data, 'item')
        item_fields = {
            "itemname": item.find('itemname').text if item.find('itemname') is not None else '',
            "kindname": item.find('kindname').text if item.find('kindname') is not None else '',
            "countyname": item.find('countyname').text if item.find('countyname') is not None else '',
            "marketname": item.find('marketname').text if item.find('marketname') is not None else '',
            "yyyy": item.find('yyyy').text if item.find('yyyy') is not None else '',
            "regday": item.find('regday').text if item.find('regday') is not None else '',
            "price": item.find('price').text if item.find('price') is not None else ''
        }
        for field_name, field_value in item_fields.items():
            field_element = SubElement(data_item, field_name)
            field_element.text = field_value

    # XML을 문자열로 변환 후, 파일로 저장
    xml_str = minidom.parseString(ET.tostring(document)).toprettyxml(indent="  ")
    with open("kamis_data.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)
    print("XML 파일로 저장 성공: kamis_data.xml")

else:
    print(f"API 호출 실패: {response.status_code}")
    print("응답 내용:", response.text)
