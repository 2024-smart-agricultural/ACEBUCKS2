import xml.etree.ElementTree as ET
import pandas as pd

# XML 파일 목록
xml_files = ["kamis_data_1.xml", "kamis_data_2.xml", "kamis_data_3.xml", "kamis_data_4.xml", "kamis_data_5.xml"]

# XML 데이터에서 데이터프레임 생성
all_data = []
for file in xml_files:
    tree = ET.parse(file)
    root = tree.getroot()
    for item in root.findall(".//item"):
        yyyy = item.find("yyyy").text if item.find("yyyy") is not None else ''
        regday = item.find("regday").text if item.find("regday") is not None else ''
        
        # 날짜 결합 (yyyy + regday 형식으로)
        date = f"{yyyy}-{regday}" if yyyy and regday else None
        
        # price를 숫자로 변환 (문자열인 경우도 처리)
        price_text = item.find("price").text if item.find("price") is not None else ''
        try:
            price = float(price_text)  # 소수 포함 숫자 형식으로 변환
        except ValueError:
            price = None  # 변환할 수 없는 경우 None으로 설정

        data = {
            "itemname": item.find("itemname").text if item.find("itemname") is not None else '',
            "kindname": item.find("kindname").text if item.find("kindname") is not None else '',
            "countyname": item.find("countyname").text if item.find("countyname") is not None else '',
            "marketname": item.find("marketname").text if item.find("marketname") is not None else '',
            "date": date,  # 결합된 날짜
            "price": price  # 숫자형으로 변환된 가격
        }
        all_data.append(data)

# 데이터프레임으로 변환
df = pd.DataFrame(all_data)

# 날짜 형식으로 변환
df["date"] = pd.to_datetime(df["date"], errors='coerce')

# 데이터프레임을 CSV 파일로 저장
df.to_csv("kamis_data.csv", index=False)
print("CSV 파일로 저장 완료: kamis_data.csv")
