import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="건강식 피드백", page_icon="🌿", layout="wide")

ADMIN_PASSWORD = "8323"
DATA_FILE = "health_survey_results.csv"

page = st.sidebar.radio("메뉴", ["📝 설문조사", "📊 관리자 대시보드"])

if page == "📝 설문조사":
    st.title("🌿 건강식 만족도 조사")
    with st.form("survey_form"):
        name = st.text_input("이름")
        rating = st.radio("만족도", ["매우 불만족", "불만족", "보통", "만족", "매우 만족"])
        comment = st.text_area("의견")
        submit = st.form_submit_button("제출")
        if submit:
            data = {"이름": name, "만족도": rating, "의견": comment}
            df = pd.DataFrame([data])
            df.to_csv(DATA_FILE, mode='a', header=not os.path.exists(DATA_FILE), index=False)
            st.success("소중한 의견 감사합니다!")
else:
    st.title("🔒 관리자 대시보드")
    pw = st.text_input("비밀번호", type="password")
    if pw == ADMIN_PASSWORD:
        if os.path.exists(DATA_FILE):
            st.dataframe(pd.read_csv(DATA_FILE))
        else:
            st.write("데이터가 없습니다.")
    elif pw:
        st.error("비밀번호가 틀렸습니다.")
