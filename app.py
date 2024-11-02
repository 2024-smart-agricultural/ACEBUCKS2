import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# CSV 데이터 로드
df = pd.read_csv("kamis_data.csv")

# Streamlit 페이지 설정
st.title("KAMIS 데이터 시각화")
st.write("품목 가격 변동")

# 예시 그래프: 날짜별 가격 변동
fig, ax = plt.subplots()
for item in df["itemname"].unique():
    item_data = df[df["itemname"] == item]
    ax.plot(item_data["regday"], item_data["price"], label=item)

ax.set_xlabel("날짜")
ax.set_ylabel("가격")
ax.legend()
st.pyplot(fig)
