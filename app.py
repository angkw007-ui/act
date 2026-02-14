import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. 설정 및 데이터 로드 ---
# 선생님이 주신 '웹에 게시' CSV 직통 주소입니다.
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRVGPDJQxWDyHoy6x7V8LFRZT2OBWY-OOdCrSwOQ3LuYkzCjpeYSU3XzQonEdPqEhVy7nsGIGPIldt8/pub?output=csv"
PLAN_FILE = "weekly_plan.csv" # 주간 업무 저장용 로컬 파일

st.set_page_config(page_title="구례중 업무관리 시스템", layout="wide")

# 구글 시트 데이터 로드 함수
@st.cache_data(ttl=60)
def load_base_data():
    try:
        # 데이터 로드 및 전처리
        df = pd.read_csv(URL)
        # 모든 컬럼을 문자열로 변환하고 결측치는 빈칸처리
        df = df.fillna("")
        return df
    except Exception as e:
        st.error(f"시트 로드 오류: {e}")
        return pd.DataFrame()

# 주간 업무 파일 로드/저장 함수
def load_weekly_plans():
    if os.path.exists(PLAN_FILE):
        return pd.read_csv(PLAN_FILE)
    return pd.DataFrame(columns=["날짜", "부서", "업무내용"])

# --- 2. 사이드바: 주간 업무 입력창 ---
st.sidebar.header("📝 주간 업무/행사 등록")
st.sidebar.info("여기 입력하면 학사력에 자동 합쳐집니다.")

with st.sidebar.form("weekly_form", clear_on_submit=True):
    input_date = st.date_input("날짜 선택", datetime.now())
    input_dept = st.selectbox("담당 부서", ["교무부", "학생부", "연구부", "정보부", "행정실", "기타"])
    input_event = st.text_input("업무 및 행사명")
    submit = st.form_submit_button("등록하기")

    if submit and input_event:
        # 날짜 형식 통일 (예: 2026-03-02)
        new_data = pd.DataFrame([[str(input_date), input_dept, input_event]], columns=["날짜", "부서", "업무내용"])
        df_weekly = load_weekly_plans()
        pd.concat([df_weekly, new_data]).to_csv(PLAN_FILE, index=False, encoding='utf-8-sig')
        st.sidebar.success("등록 완료! 화면을 새로고침(F5) 하세요.")

# --- 3. 메인 화면: 통합 뷰 ---
st.title("🏫 구례중 주간/월간 업무 통합 시스템")

tab1, tab2 = st.tabs(["🗓️ 통합 학사력 (자동합산)", "📋 부서별 주간계획"])

with tab1:
    st.subheader("📊 실시간 학사력 및 주간업무 통합조회")
    
    base_df = load_base_data()   # 구글 시트 원본
    weekly_df = load_weekly_plans() # 웹앱에서 추가한 업무
    
    if not base_df.empty:
        # 두 데이터를 하나로 합침
        # (시트의 컬럼명과 입력 데이터의 컬럼명이 달라도 모두 보여줍니다)
        combined_df = pd.concat([base_df, weekly_df], axis=0, ignore_index=True)
        
        # --- 월별 연한 색상 구분 함수 ---
        def style_rows(row):
            # '월'이나 '날짜' 정보가 들어있는 첫 번째 열을 기준으로 색상 지정
            # 홀수달(3,5,7...)과 짝수달(4,6,8...)을 구분합니다.
            try:
                # 데이터에서 숫자(월) 추출 시도
                first_val = str(row.iloc[0])
                month_num = int(''.join(filter(str.isdigit, first_val[:3]))) 
                if month_num % 2 == 0:
                    return ['background-color: #F0F8FF'] * len(row) # 연한 하늘색 (짝수달)
                else:
                    return ['background-color: #FFF5EE'] * len(row) # 연한 주황색 (홀수달)
            except:
                return [''] * len(row)

        # 표 출력: 화면에 꽉 차게(use_container_width), 월말까지 보이게 높이 넉넉히
        st.dataframe(
            combined_df.style.apply(style_rows, axis=1),
            use_container_width=True, 
            height=800, # 컴퓨터 화면에서 스크롤 없이 가급적 다 보이게 설정
            hide_index=True
        )
    else:
        st.warning("구글 시트 데이터를 가져올 수 없습니다. 웹 게시 설정을 확인해주세요.")

with tab2:
    st.subheader("📂 부서별 주간 업무 집중 보기")
    if not weekly_df.empty:
        dept_filter = st.multiselect("필터링할 부서 선택", ["교무부", "학생부", "연구부", "정보부", "행정실"], default=["교무부"])
        filtered_df = weekly_df[weekly_df['부서'].isin(dept_filter)]
        st.table(filtered_df)
    else:
        st.write("아직 등록된 주간 업무가 없습니다. 왼쪽 사이드바에서 입력해 보세요!")
