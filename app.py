# app.py
import streamlit as st
import pandas as pd

# CSV 데이터 로드
df = pd.read_csv("kamis_data.csv")

# 제목과 설명
st.title("KAMIS 농산물 가격 데이터 입력")
st.write("이 웹 애플리케이션은 선택한 지역의 농산물 품목을 나열하고, 각 품목에 대해 수량을 입력할 수 있도록 합니다.")

# 지역 선택
st.subheader("1. 지역 선택")
selected_county = st.selectbox("지역을 선택하세요:", df["countyname"].unique())

# 선택한 지역의 품목 나열
st.write(f"선택한 지역 ({selected_county})의 품목 리스트:")

# 선택한 지역에 해당하는 데이터 필터링
filtered_data = df[df["countyname"] == selected_county]

# 품목별 입력 칸 생성
quantities = {}
for item_name in filtered_data["itemname"].unique():
    quantity = st.number_input(
        f"{item_name}의 수량 입력 (기본값: 100)",
        min_value=0,
        value=100  # 기본값을 100으로 설정
    )
    quantities[item_name] = quantity  # 수량 저장

# 선택된 수량 확인 (디버그용)
st.write("선택된 수량:", quantities)
