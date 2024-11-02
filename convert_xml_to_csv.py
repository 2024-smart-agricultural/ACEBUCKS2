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
        data = {
            "itemname": item.find("itemname").text,
            "kindname": item.find("kindname").text,
            "countyname": item.find("countyname").text,
            "marketname": item.find("marketname").text,
            "yyyy": item.find("yyyy").text,
            "regday": item.find("regday").text,
            "price": item.find("price").text
        }
        all_data.append(data)

# 데이터프레임으로 변환
df = pd.DataFrame(all_data)
df.to_csv("kamis_data.csv", index=False)
print("CSV 파일로 저장 완료: kamis_data.csv")
