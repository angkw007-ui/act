import streamlit as st
import pandas as pd

st.set_page_config(page_title="창체 시수 계산기", layout="wide")

st.title("🏫 창의적 체험활동 계획 수립 도우미")
st.info("활동 시간을 입력하면 자율/동아리/봉사/진로 영역별로 자동 계산됩니다.")

# 1. 데이터 입력부
with st.sidebar:
    st.header("📍 활동 입력")
    date = st.date_input("날짜 선택")
    category = st.selectbox("활동 영역", ["자율활동", "동아리활동", "봉사활동", "진로활동"])
    content = st.text_input("활동 내용", placeholder="예: 학급 자치 회의")
    hours = st.number_input("단위 시간(교시)", min_value=1, max_value=8, value=1)
    
    if st.button("활동 추가하기"):
        new_data = {"날짜": date, "영역": category, "내용": content, "시간": hours}
        if 'df' not in st.session_state:
            st.session_state.df = pd.DataFrame(columns=["날짜", "영역", "내용", "시간"])
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_data])], ignore_index=True)
        st.success("추가되었습니다!")

# 2. 계산 및 출력부
if 'df' in st.session_state and not st.session_state.df.empty:
    df = st.session_state.df
    
    # 영역별 합계 계산
    summary = df.groupby("영역")["시간"].sum().reset_index()
    
    # 대시보드 시각화
    cols = st.columns(4)
    targets = {"자율활동": 18, "동아리활동": 34, "봉사활동": 8, "진로활동": 10} # 예시 기준 시수
    
    for i, (name, target) in enumerate(targets.items()):
        current = summary[summary["영역"] == name]["시간"].sum()
        with cols[i]:
            st.metric(name, f"{current}시간", f"목표: {target}h")
            st.progress(min(current / target, 1.0))
            
    st.divider()
    st.subheader("📋 전체 활동 내역")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("왼쪽 사이드바에서 활동을 먼저 입력해주세요.")