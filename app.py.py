import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 설정
st.set_page_config(page_title="건강식 피드백", page_icon="🌿", layout="wide")

ADMIN_PASSWORD = "8323"
DATA_FILE = "health_survey_results.csv"

# 페이지 선택
page = st.sidebar.radio("메뉴", ["📝 설문조사", "📊 관리자 대시보드"])

if page == "📝 설문조사":
    st.title("🌿 건강식 만족도 조사")
    with st.form("survey_form"):
        name = st.text_input("이름")
        rating = st.radio("만족도", ["매우 불만족", "불만족", "보통", "만족", "매우 만족"])
        comment = st.text_area("의견")
        marketing = st.checkbox("마케팅 정보 수신 동의")
        submit = st.form_submit_button("제출")
        
        if submit:
            data = {"이름": name, "만족도": rating, "의견": comment, "마케팅동의": marketing}
            df = pd.DataFrame([data])
            df.to_csv(DATA_FILE, mode='a', header=not os.path.exists(DATA_FILE), index=False)
            st.success("소중한 의견 감사합니다!")

else:
    st.title("🔒 관리자 대시보드")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if password == ADMIN_PASSWORD:
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            st.metric("총 참여자 수", len(df))
            st.dataframe(df)
        else:
            st.warning("아직 수집된 데이터가 없습니다.")
    elif password != "":
        st.error("비밀번호가 틀렸습니다.")
