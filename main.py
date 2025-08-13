# streamlit_app.py
import streamlit as st
import pandas as pd
import altair as alt

# CSV 불러오기
df = pd.read_csv("countriesMBTI_16types.csv")

# 국가 목록
countries = df["Country"].unique()

# Streamlit UI
st.title("국가별 MBTI 비율 TOP 10")
selected_country = st.selectbox("국가를 선택하세요:", countries)

# 선택한 국가의 데이터만 추출
row = df[df["Country"] == selected_country].iloc[0]
mbti_data = row.drop("Country")

# 비율 순으로 정렬
mbti_df = pd.DataFrame({
    "MBTI": mbti_data.index,
    "비율": mbti_data.values
}).sort_values("비율", ascending=False).head(10)

# Altair 그래프
chart = (
    alt.Chart(mbti_df)
    .mark_bar()
    .encode(
        x=alt.X("비율", title="비율", scale=alt.Scale(domain=[0, mbti_df["비율"].max()*1.1])),
        y=alt.Y("MBTI", sort="-x", title="MBTI 유형"),
        tooltip=["MBTI", "비율"]
    )
    .properties(width=600, height=400)
)

st.altair_chart(chart, use_container_width=True)

# 데이터 테이블 표시
st.dataframe(mbti_df)
