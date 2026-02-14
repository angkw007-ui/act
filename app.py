import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- [1. 기본 설정 및 데이터 로드] ---
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRVGPDJQxWDyHoy6x7V8LFRZT2OBWY-OOdCrSwOQ3LuYkzCjpeYSU3XzQonEdPqEhVy7nsGIGPIldt8/pub?output=csv"
PLAN_FILE = "weekly_plan.csv"

st.set_page_config(page_title="구례중 통합 업무 시스템", layout="wide")

# CSS를 활용한 UI 디테일 조정 (가가운데 정렬 및 폰트)
st.markdown("""
    <style>
    .main { text-align: center; }
    div[data-testid="stExpander"] div[role="button"] p { font-weight: bold; font-size: 1.1rem; }
    th { background-color: #f0f2f6 !important; text-align: center !important; }
    td { text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_base_data():
    try:
        # 첫 행(Unnamed)을 건너뛰고 불러옵니다.
        df = pd.read_csv(URL, header=1) 
        return df.fillna("")
    except:
        return pd.DataFrame()

def load_weekly_plans():
    if os.path.exists(PLAN_FILE):
        return pd.read_csv(PLAN_FILE)
    return pd.DataFrame(columns=["날짜", "부서", "업무내용"])

# --- [2. 주간 계획 입력 섹션 (상단 배치)] ---
st.title("🏫 구례중 주간/월간 업무 통합 시스템")

with st.expander("📅 신규 주간 업무/행사 등록 (여기를 클릭하세요)", expanded=True):
    col1, col2, col3 = st.columns([2, 2, 4])
    with col1:
        # 달력에서 직접 날짜 선택
        input_date = st.date_input("날짜 선택", datetime.now())
    with col2:
        input_dept = st.selectbox("담당 부서", ["교무부", "학생부", "연구부", "정보부", "행정실", "기타"])
    with col3:
        input_event = st.text_input("업무 및 행사명 (입력 후 엔터)")
    
    if st.button("🚀 학사력에 즉시 반영"):
        if input_event:
            new_data = pd.DataFrame([[str(input_date), input_dept, input_event]], columns=["날짜", "부서", "업무내용"])
            df_weekly = load_weekly_plans()
            pd.concat([df_weekly, new_data]).to_csv(PLAN_FILE, index=False, encoding='utf-8-sig')
            st.success(f"'{input_event}' 업무가 등록되었습니다!")
            st.rerun() # 실시간 반영을 위해 앱 재실행
        else:
            st.warning("내용을 입력해주세요.")

st.markdown("---")

# --- [3. 통합 학사력 출력 섹션] ---
st.subheader("🗓️ 실시간 통합 학사력")

base_df = load_base_data()
weekly_df = load_weekly_plans()

if not base_df.empty:
    # --- 색상 및 스타일 정의 ---
    def apply_style(row):
        styles = []
        for i, val in enumerate(row):
            col_name = base_df.columns[i]
            style = 'text-align: center;'
            
            # 1. 열 너비 조절 (맨 앞 '일' 열은 좁게)
            if "일" in col_name and len(col_name) <= 2:
                style += 'width: 40px;'

            # 2. 월별 배경색 (홀수월: 연녹색, 짝수월: 연파란색)
            # 컬럼명에서 숫자 추출 (예: '3월' -> 3)
            try:
                month_num = int(''.join(filter(str.isdigit, col_name)))
                if month_num % 2 != 0:
                    style += 'background-color: #E8F5E9;' # 연녹색
                else:
                    style += 'background-color: #E3F2FD;' # 연파란색
            except:
                pass

            # 3. 연휴 및 빨간날 처리 (글자에 '날', '절', '일(빨간색)' 등이 포함될 경우)
            holiday_keywords = ["신정", "구정", "추석", "어린이날", "크리스마스", "현충일", "광복절", "삼일절", "제헌절", "개천절", "한글날"]
            if any(key in str(val) for key in holiday_keywords) or "휴업" in str(val):
                style += 'background-color: #FFEBEE; color: #D32F2F; font-weight: bold;' # 연빨강 배경

            styles.append(style)
        return styles

    # 표 출력
    st.dataframe(
        base_df.style.apply(apply_style, axis=1),
        use_container_width=True,
        height=700,
        hide_index=True
    )
    
    # 주간 업무 별도 표시 (하단)
    if not weekly_df.empty:
        with st.expander("📌 최근 등록된 주간 업무 목록"):
            st.table(weekly_df.sort_values(by="날짜", ascending=False))

else:
    st.error("구글 시트 데이터를 불러올 수 없습니다.")
