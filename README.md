[app.py](https://github.com/user-attachments/files/28478672/app.py)
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ── 설정 ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="건기식 피드백 설문", page_icon="🌿", layout="wide")

ADMIN_PASSWORD = "8323"   # 👈 원하는 비밀번호로 바꾸세요
CSV_FILE       = "health_survey_results.csv"

STAR_MAP = {
    "⭐ 1점 – 매우 불만족": 1,
    "⭐⭐ 2점 – 불만족":     2,
    "⭐⭐⭐ 3점 – 보통":     3,
    "⭐⭐⭐⭐ 4점 – 만족":   4,
    "⭐⭐⭐⭐⭐ 5점 – 매우 만족": 5,
}
STAR_LABELS = list(STAR_MAP.keys())

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.main { background-color: #f9fbf9; }
[data-testid="stSidebar"] { background-color: #1e3d18; }
[data-testid="stSidebar"] * { color: #e8f5e9 !important; }
[data-testid="stSidebar"] .stRadio label { color: #e8f5e9 !important; }
.stButton>button {
    border-radius: 25px;
    background: linear-gradient(135deg, #2d5a27, #4a7c42);
    color: white; width: 100%; border: none;
    padding: 12px; font-size: 1.05rem; font-weight: 700;
}
.sec-header {
    background: linear-gradient(90deg, #2d5a27, #5a9e52);
    color: white; padding: 9px 16px; border-radius: 8px;
    margin: 22px 0 10px; font-weight: 700; font-size: 1rem;
}
.consent-req {
    background: #fffde7; border-left: 5px solid #ffc107;
    padding: 13px 18px; border-radius: 8px; margin: 6px 0;
    font-size: .93rem; line-height: 1.6;
}
.consent-opt {
    background: #f1f8e9; border-left: 5px solid #66bb6a;
    padding: 13px 18px; border-radius: 8px; margin: 6px 0;
    font-size: .93rem; line-height: 1.6;
}
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #2d5a27, #4a7c42);
    border-radius: 12px; padding: 16px 20px;
}
[data-testid="metric-container"] [data-testid="metric-label"]
    { color: rgba(255,255,255,.85) !important; }
[data-testid="metric-container"] [data-testid="metric-value"]
    { color: #fff !important; font-size: 1.7rem !important; }
</style>
""", unsafe_allow_html=True)

# ── 헬퍼 ─────────────────────────────────────────────────────────────────────
def load_data() -> pd.DataFrame:
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame()

def save_response(row: dict):
    exists = os.path.exists(CSV_FILE)
    pd.DataFrame([row]).to_csv(
        CSV_FILE, mode="a", header=not exists, index=False, encoding="utf-8-sig"
    )

# ── 세션 상태 ─────────────────────────────────────────────────────────────────
if "survey_done" not in st.session_state:
    st.session_state.survey_done = False

# ── 사이드바 ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 건강기능식품\n### 소비자 설문조사")
    st.markdown("---")
    page = st.radio("메뉴", ["🌿 설문조사 참여", "📊 관리자 대시보드"],
                    label_visibility="collapsed")
    st.markdown("---")
    st.metric("총 응답 수", f"{len(load_data())}건")


# ═══════════════════════════════════════════════════════════════════════════════
# 설문조사 페이지
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🌿 설문조사 참여":

    # 제출 완료 화면
    if st.session_state.survey_done:
        st.title("🌿 건강기능식품 소비자 설문조사")
        st.markdown("---")
        st.success("### 🎉 설문이 제출되었습니다! 소중한 의견 감사드립니다.")
        st.balloons()
        if st.button("↩️ 다시 참여하기"):
            st.session_state.survey_done = False
            st.rerun()
        st.stop()

    st.title("🌿 건강기능식품 소비자 설문조사")
    st.markdown("여러분의 솔직한 의견이 더 나은 제품 개발에 직접 반영됩니다.")
    st.markdown("---")

    with st.form("survey_form"):

        # Q1. 기본 정보
        st.markdown('<div class="sec-header">📋 Q1. 기본 정보</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            gender = st.radio("성별", ["여성", "남성", "응답 안 함"], horizontal=True)
        with col2:
            age = st.selectbox("연령대", ["10대", "20대", "30대", "40대", "50대", "60대 이상"])

        # Q2. 복용 목적
        st.markdown('<div class="sec-header">🎯 Q2. 복용 목적 (다중 선택)</div>', unsafe_allow_html=True)
        purposes = st.multiselect(
            "해당하는 항목을 모두 선택해 주세요.",
            ["면역력 개선", "피로 회복", "장 건강", "피부 관리", "다이어트", "기타"],
            placeholder="복수 선택 가능",
        )

        # Q3. 만족도 평가
        st.markdown('<div class="sec-header">⭐ Q3. 제품 만족도 평가 (5점 척도)</div>', unsafe_allow_html=True)
        r_form      = st.select_slider("① 목넘김 및 제형 만족도 (알약 크기·맛·향)", STAR_LABELS, STAR_LABELS[2])
        r_effect    = st.select_slider("② 효과 체감 만족도",                         STAR_LABELS, STAR_LABELS[2])
        r_repurchase = st.select_slider("③ 재구매 의사",                              STAR_LABELS, STAR_LABELS[2])

        # Q4. 주관식
        st.markdown('<div class="sec-header">✏️ Q4. 주관식 피드백</div>', unsafe_allow_html=True)
        comment = st.text_area(
            "섭취 후 느낀 긍정적 변화나 불편했던 점을 자유롭게 작성해 주세요.",
            height=120,
            placeholder="예: 2주 복용 후 피로감이 줄었습니다. 알약 크기가 조금 컸어요.",
        )

        # 동의 항목
        st.markdown('<div class="sec-header">🔒 동의 항목</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="consent-req"><b>[필수]</b> 개인정보 수집 및 이용 동의<br>'
            '<small>📌 수집 목적: 신제품 개발 및 피드백 분석 &nbsp;|&nbsp; 보유 기간: 목적 달성 후 파기</small></div>',
            unsafe_allow_html=True,
        )
        privacy = st.checkbox("개인정보 수집 및 이용에 동의합니다. ✅ (필수)")

        st.markdown(
            '<div class="consent-opt"><b>[선택]</b> 마케팅 정보 수신 동의<br>'
            '<small>💌 신제품 출시 알림 수신 — 동의 안 하셔도 제출 가능합니다.</small></div>',
            unsafe_allow_html=True,
        )
        marketing = st.checkbox("신제품 출시 알림 및 마케팅 정보 수신에 동의합니다. (선택)")

        st.markdown("---")
        submitted = st.form_submit_button("🚀 제출하기", use_container_width=True, type="primary")

    # 제출 처리
    if submitted:
        if not privacy:
            st.error("⚠️ 개인정보 수집 및 이용 동의는 필수 항목입니다. 체크 후 다시 제출해 주세요.")
        else:
            save_response({
                "제출시간":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "성별":         gender,
                "연령대":       age,
                "복용목적":     ", ".join(purposes) if purposes else "",
                "제형만족도":   STAR_MAP[r_form],
                "효과체감만족도": STAR_MAP[r_effect],
                "재구매의사":   STAR_MAP[r_repurchase],
                "주관식피드백": comment.strip(),
                "개인정보동의": True,
                "마케팅동의":   marketing,
            })
            st.session_state.survey_done = True
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# 관리자 대시보드
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 관리자 대시보드":
    st.title("📊 설문 결과 관리자 대시보드")

    pwd = st.text_input("관리자 비밀번호를 입력하세요:", type="password")
    if pwd == "":
        st.info("비밀번호를 입력하면 대시보드가 표시됩니다.")
        st.stop()
    if pwd != ADMIN_PASSWORD:
        st.error("비밀번호가 틀렸습니다.")
        st.stop()

    # ── 데이터 로드 ────────────────────────────────────────────────────────────
    df = load_data()
    if df.empty:
        st.info("아직 수집된 데이터가 없습니다.")
        st.stop()

    total = len(df)
    df["마케팅동의"] = df["마케팅동의"].astype(str).str.lower().isin(["true", "1", "yes"])
    m_yes = int(df["마케팅동의"].sum())
    m_pct = m_yes / total * 100

    # ── KPI ────────────────────────────────────────────────────────────────────
    st.markdown("---")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("👥 총 참여자",     f"{total}명")
    k2.metric("📣 마케팅 동의",   f"{m_yes}명")
    k3.metric("📈 마케팅 동의율", f"{m_pct:.1f}%")
    k4.metric("⭐ 효과체감 평균", f"{df['효과체감만족도'].astype(float).mean():.2f}점")

    st.markdown("---")

    # ── 복용 목적 바 차트 + 마케팅 동의 도넛 ──────────────────────────────────
    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.subheader("🎯 복용 목적별 응답 현황")
        all_p: list[str] = []
        for v in df["복용목적"]:
            if pd.notna(v) and str(v).strip():
                all_p.extend(p.strip() for p in str(v).split(","))
        if all_p:
            pur = pd.Series(all_p).value_counts().reset_index()
            pur.columns = ["복용목적", "응답수"]
            pur = pur.sort_values("응답수", ascending=True)
            fig_bar = px.bar(
                pur, x="응답수", y="복용목적", orientation="h",
                color="응답수", color_continuous_scale="Greens", text="응답수",
            )
            fig_bar.update_traces(textposition="outside")
            fig_bar.update_layout(
                height=330, plot_bgcolor="white", paper_bgcolor="white",
                coloraxis_showscale=False, xaxis_title="응답 수", yaxis_title="",
                margin=dict(l=10, r=50, t=10, b=10),
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("복용 목적 응답 데이터가 없습니다.")

    with col_r:
        st.subheader("📣 마케팅 동의 현황")
        fig_donut = go.Figure(go.Pie(
            labels=["동의", "미동의"], values=[m_yes, total - m_yes],
            hole=0.58, marker_colors=["#2d5a27", "#e0e0e0"],
            textinfo="label+percent", textfont_size=13, pull=[0.04, 0],
        ))
        fig_donut.update_layout(
            height=330,
            annotations=[dict(
                text=f"<b>{m_pct:.0f}%</b><br>동의",
                x=0.5, y=0.5, font=dict(size=18, color="#2d5a27"), showarrow=False,
            )],
            legend=dict(orientation="h", y=-0.05, x=0.5, xanchor="center"),
            margin=dict(l=10, r=10, t=10, b=30),
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # ── 평균 만족도 ────────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("⭐ 제품 만족도 평균 점수")

    score_map = {
        "제형만족도":    "목넘김·제형 만족도",
        "효과체감만족도": "효과 체감 만족도",
        "재구매의사":    "재구매 의사",
    }
    avg_df = pd.DataFrame([
        {"항목": lbl, "평균": round(df[col].astype(float).mean(), 2)}
        for col, lbl in score_map.items()
    ])

    cp, cb = st.columns([2, 3])
    with cp:
        for _, row in avg_df.iterrows():
            v = row["평균"]
            st.markdown(f"**{row['항목']}**")
            st.progress(v / 5, text=f"{'⭐'*round(v)}{'☆'*(5-round(v))}  **{v:.2f} / 5점**")
            st.markdown(" ")

    with cb:
        colors = ["#2d5a27", "#4a7c42", "#7cb67a"]
        fig_score = go.Figure()
        for i, row in avg_df.iterrows():
            fig_score.add_trace(go.Bar(
                x=[row["평균"]], y=[row["항목"]], orientation="h",
                marker_color=colors[i],
                text=[f"  {row['평균']:.2f}점"], textposition="outside",
            ))
        fig_score.add_vline(x=3, line_dash="dash", line_color="gray",
                            annotation_text="중간값(3.0)")
        fig_score.update_layout(
            height=260, plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(range=[0, 6.5], title="평균 점수"),
            yaxis_title="", showlegend=False,
            margin=dict(l=10, r=70, t=20, b=20),
        )
        st.plotly_chart(fig_score, use_container_width=True)

    # ── 주관식 피드백 테이블 ────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("✏️ 주관식 피드백 모아보기")
    fb = df[
        df["주관식피드백"].notna() & (df["주관식피드백"].astype(str).str.strip() != "")
    ][["제출시간", "성별", "연령대", "주관식피드백"]].rename(columns={"주관식피드백": "피드백 내용"})

    if fb.empty:
        st.info("아직 주관식 피드백이 없습니다.")
    else:
        st.dataframe(fb, use_container_width=True, height=280)

    # ── 다운로드 ───────────────────────────────────────────────────────────────
    st.markdown("---")
    csv_bytes = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        "📥 전체 데이터 CSV 다운로드",
        csv_bytes,
        f"health_survey_{datetime.now().strftime('%Y%m%d')}.csv",
        "text/csv",
    )
    st.caption(f"마지막 새로고침: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
