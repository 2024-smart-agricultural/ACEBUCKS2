# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV 데이터 로드
df = pd.read_csv("kamis_data.csv")

# 제목과 설명
st.title("KAMIS 농산물 가격 데이터 시각화")
st.write("이 웹 애플리케이션은 KAMIS에서 수집한 농산물 가격 데이터를 시각화합니다.")

# 데이터프레임 미리보기
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# 날짜 형식 변환 (필요한 경우)
df["regday"] = pd.to_datetime(df["regday"], errors='coerce')

# 날짜별 가격 그래프 예시
st.subheader("날짜별 가격 변동")
selected_item = st.selectbox("품목을 선택하세요:", df["itemname"].unique())

# 선택한 품목의 데이터 필터링
filtered_data = df[df["itemname"] == selected_item]

# 날짜 범위 선택 슬라이더
start_date, end_date = st.slider(
    "날짜 범위를 선택하세요:",
    min_value=filtered_data["regday"].min(),
    max_value=filtered_data["regday"].max(),
    value=(filtered_data["regday"].min(), filtered_data["regday"].max())
)

# 날짜 필터링
filtered_data = filtered_data[
    (filtered_data["regday"] >= start_date) & 
    (filtered_data["regday"] <= end_date)
]

# 그래프 그리기
st.subheader(f"{selected_item}의 날짜별 가격 변동")
if not filtered_data.empty:
    fig, ax = plt.subplots()
    ax.plot(filtered_data["regday"], filtered_data["price"], marker='o')
    ax.set_xlabel("날짜")
    ax.set_ylabel("가격")
    ax.set_title(f"{selected_item}의 가격 변동")
    st.pyplot(fig)
else:
    st.write("선택한 날짜 범위에 데이터가 없습니다.")
