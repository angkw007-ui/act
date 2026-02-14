import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 페이지 설정
st.set_page_config(page_title="교내 주간/월간 업무관리", layout="wide")

# --- 1. 데이터 관리 로직 ---
PLAN_FILE = "plan.csv"  # 주간 계획 저장 파일
BASE_FILE = "base_calendar.csv"  # 학기 초 기본 학사일정

# 데이터 저장 파일이 없으면 새로 생성
if not os.path.exists(PLAN_FILE):
    df = pd.DataFrame(columns=["날짜", "부서", "교시", "대상", "행사명"])
    df.to_csv(PLAN_FILE, index=False, encoding='utf-8-sig')

# 데이터 불러오기 함수
def load_data():
    return pd.read_csv(PLAN_FILE, encoding='utf-8-sig')

# 학기 초 기본 데이터 불러오기 (파일이 있을 경우만)
def load_base_calendar():
    if os.path.exists(BASE_FILE):
        return pd.read_csv(BASE_FILE, encoding='utf-8-sig')
    return pd.DataFrame(columns=["날짜", "행사명"])

# --- 2. 사이드바: 업무 입력부 ---
st.sidebar.header("📝 업무 계획 입력")
with st.sidebar.form("input_form", clear_on_submit=True):
    dept = st.selectbox("소속 부서", ["교무부", "학생부", "연구부", "과학정보부", "행정실", "기타"])
    date = st.date_input("날짜 선택", datetime.now())
    time_slot = st.selectbox("교시/시간", ["1교시", "2교시", "3교시", "4교시", "5교시", "6교시", "7교시", "종일"])
    target = st.selectbox("대상 학년", ["1학년", "2학년", "3학년", "전체", "해당없음"])
    event_name = st.text_input("행사명(업무 내용)")
    
    submit = st.form_submit_button("등록하기")
    
    if submit:
        if event_name:
            new_entry = pd.DataFrame([[date.strftime("%Y-%m-%d"), dept, time_slot, target, event_name]], 
                                     columns=["날짜", "부서", "교시", "대상", "행사명"])
            df_current = load_data()
            df_updated = pd.concat([df_current, new_entry], ignore_index=True)
            df_updated.to_csv(PLAN_FILE, index=False, encoding='utf-8-sig')
            st.sidebar.success(f"'{event_name}' 등록 완료!")
        else:
            st.sidebar.error("행사명을 입력해주세요.")

# --- 3. 메인 화면: 출력부 ---
st.title("🏫 교내 업무 공유 시스템")

tab1, tab2, tab3 = st.tabs(["📅 월간 계획 (학사력)", "📋 부서별 주간 계획", "⚙️ 기본 설정"])

# 탭 1: 월간 계획 / 학사력 (자동 반영)
with tab1:
    st.subheader("이번 달 주요 행사 (기본 학사일정 + 부서별 업무)")
    
    # 데이터 통합
    all_plans = load_data()
    base_plans = load_base_calendar()
    
    # 날짜별로 행사명만 모으기
    combined = pd.concat([
        all_plans[['날짜', '행사명']],
        base_plans[['날짜', '행사명']]
    ])
    
    if not combined.empty:
        combined['날짜'] = pd.to_datetime(combined['날짜'])
        combined = combined.sort_values(by='날짜')
        # 사용자가 보기 편하게 표로 출력
        st.dataframe(combined, use_container_width=True, hide_index=True)
    else:
        st.info("등록된 일정이 없습니다.")

# 탭 2: 주간 계획 상세 뷰
with tab2:
    st.subheader("부서별 상세 주간 일정")
    view_dept = st.multiselect("확인할 부서를 선택하세요", ["교무부", "학생부", "연구부", "과학정보부", "행정실", "기타"], default=["교무부"])
    
    df_view = load_data()
    if not df_view.empty:
        filtered_df = df_view[df_view['부서'].isin(view_dept)]
        st.table(filtered_df.sort_values(by="날짜"))
    else:
        st.write("표시할 상세 계획이 없습니다.")

# 탭 3: 기본 학사력 관리 (CSV 업로드 기능 대신 설명)
with tab3:
    st.info("💡 학기 초 공통 학사일정은 'base_calendar.csv' 파일을 깃허브에 올리면 자동으로 반영됩니다.")
    st.write("CSV 파일 형식: 날짜(YYYY-MM-DD), 행사명")
