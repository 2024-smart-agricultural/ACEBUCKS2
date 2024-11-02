# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 데이터 로드 및 A~G 열 중 비어있는 값이 있는 행 삭제
df = pd.read_csv("kamis_data.csv")
df = df.dropna(subset=["itemname", "kindname", "countyname", "marketname", "date", "price"])

# 'price' 열을 숫자로 변환하고 쉼표 제거
df['price'] = df['price'].replace({',': ''}, regex=True)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# 날짜 열을 datetime으로 변환
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# 유효한 날짜만 필터링
valid_dates = df['date'].dropna().unique()
if not valid_dates.size:
    st.error("유효한 날짜가 없습니다.")
    st.stop()

# 제목과 설명
st.title("생과일 쥬스 전문전 과일 유통 경로 도우미")
st.write("이 웹 애플리케이션은 선택한 날짜와 지역을 기준으로 어느 유통 경로를 통해 과일 수입을 하는 것이 이익인지를 분석해주는 서비스입니다.")

# 날짜 선택 (기본값을 가장 최신 날짜로 설정) - CSV 파일에 있는 날짜만 선택 가능
st.subheader("1. 날짜 선택")
selected_date = st.date_input(
    "날짜를 선택하세요:",
    min_value=valid_dates.min(),
    max_value=valid_dates.max(),
    value=valid_dates.max()
)
if pd.to_datetime(selected_date) not in valid_dates:
    st.error("선택한 날짜가 유효하지 않습니다. CSV 파일에 있는 날짜만 선택할 수 있습니다.")
    st.stop()

# 'nan', '평균', '평년'을 제외한 지역 리스트 생성
valid_counties = df["countyname"].dropna().unique()
valid_counties = [county for county in valid_counties if county not in ['평균', '평년']]

# 지역 선택
st.subheader("2. 지역 선택")
selected_county = st.selectbox("지역을 선택하세요:", valid_counties)

# 잔수 설정 및 품목 중량 입력 필드 생성
st.subheader("3. 잔수 설정 및 4. 품목 중량 입력")

# 각 품목별 잔수와 중량의 변환 비율 설정
conversion_factors = {
    '토마토': 3,
    '멜론': 3,
    '파인애플': 3,
    '바나나': 2,
    '레몬': 2
}

filtered_data = df[(df["countyname"] == selected_county) & (df["date"] == pd.to_datetime(selected_date))]

# 콜백 함수 정의: 잔수를 변경하면 중량을 업데이트
def update_weight(item_name):
    factor = conversion_factors[item_name]
    if f"{item_name}_glass_count" in st.session_state:
        st.session_state[f"{item_name}_weight"] = st.session_state[f"{item_name}_glass_count"] // factor

# 콜백 함수 정의: 중량을 변경하면 잔수를 업데이트
def update_glass_count(item_name):
    factor = conversion_factors[item_name]
    if f"{item_name}_weight" in st.session_state:
        st.session_state[f"{item_name}_glass_count"] = st.session_state[f"{item_name}_weight"] * factor

quantities = {}
glass_counts = {}

# 잔수와 중량 설정 필드 생성
cols_glass = st.columns(5)
cols_weight = st.columns(5)

for i, item_name in enumerate(filtered_data["itemname"].unique()):
    factor = conversion_factors[item_name]
    with cols_glass[i % 5]:
        glass_counts[item_name] = st.number_input(
            f"{item_name} (잔수)", min_value=0, value=300,
            key=f"{item_name}_glass_count", on_change=update_weight, args=(item_name,)
        )

    with cols_weight[i % 5]:
        quantities[item_name] = st.number_input(
            f"{item_name} (중량)", min_value=0, value=100,
            key=f"{item_name}_weight", on_change=update_glass_count, args=(item_name,)
        )

# 각 품목별 1잔당 가격 정의
glass_prices = {
    '토마토': 3000,
    '멜론': 3500,
    '바나나': 3000,
    '파인애플': 3000,
    '레몬': 3500
}

# Market별 Total Price 계산 및 색상 지정
total_prices = {}
colors = []
for market_name in filtered_data["marketname"].unique():
    market_data = filtered_data[filtered_data["marketname"] == market_name]

    total_price = 0
    missing_data = False
    for item_name, quantity in quantities.items():
        item_data = market_data[market_data["itemname"] == item_name]
        if not item_data.empty:
            item_price = item_data["price"].iloc[0]  # 선택한 날짜의 가격
            if pd.notna(item_price):  # 가격이 존재하는 경우에만 계산
                total_price += item_price * quantity
            else:
                missing_data = True
        else:
            missing_data = True

    total_prices[market_name] = total_price / 10000  # 만원 단위로 변환
    colors.append('red' if missing_data else 'blue')  # 누락된 데이터가 있으면 빨간색, 아니면 파란색

# Market별 Total Price 출력
st.subheader("Market별 Total Price")
st.write(total_prices)

# Market별 Total Price 그래프 생성
fig = go.Figure()

# Market 데이터를 기준으로 점을 추가
for idx, (market, price) in enumerate(total_prices.items()):
    fig.add_trace(go.Scatter(
        x=[market],
        y=[price],
        mode='markers',
        hovertext=[f"{price}만원"],  # 마우스를 올렸을 때만 가격 표시
        marker=dict(
            color=colors[idx],
            size=10
        ),
        name=market
    ))

# 레이아웃 설정
fig.update_layout(
    title={
        'text': f"{selected_county}의 Market별 Total Price",
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
    },
    xaxis_title="Market Name",
    yaxis_title="Total Price (만원)",
    hovermode="x"
)

# 그래프 표시
st.plotly_chart(fig)

# 파란색 점을 가진 Market들에 대해서만 수익 계산
market_profits = {}

for market_name in filtered_data["marketname"].unique():
    if colors[filtered_data["marketname"].unique().tolist().index(market_name)] == 'red':
        continue  # 빨간색 점인 Market은 제외

    market_data = filtered_data[filtered_data["marketname"] == market_name]
    total_profit = 0
    multiplier = 1.0 if '유통' in market_name else 0.9

    # 각 항목에 대해 계산
    for item_name, quantity in quantities.items():
        glass_count = glass_counts[item_name]
        item_data = market_data[market_data["itemname"] == item_name]

        if not item_data.empty:
            item_price = item_data["price"].iloc[0]
            if pd.notna(item_price):  # 가격이 존재할 경우에만 계산
                glass_price = glass_prices.get(item_name, 0)
                profit = (glass_count * multiplier * glass_price - quantity * item_price)
                total_profit += profit

    # 유통이 포함되지 않은 Market은 10000을 빼기
    if '유통' not in market_name:
        total_profit -= 10000

    market_profits[market_name] = total_profit / 10000  # 만원 단위로 환산

# 결과 테이블 출력
st.subheader("관심 Market별 수익 계산 결과")
st.write(pd.DataFrame.from_dict(market_profits, orient='index', columns=['Total Profit (만원)']))

# 최고 수익 Market을 찾고, 추천 문구 추가
if market_profits:
    best_market = max(market_profits, key=market_profits.get)
    st.markdown(f"### 대표님, 금일 과일 구입은 '**{best_market}**'을 이용하시는 것이 합리적입니다.")
