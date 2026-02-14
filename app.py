import streamlit as st
import pandas as pd
from datetime import datetime

# --- [1. 설정 및 데이터 로드] ---
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRVGPDJQxWDyHoy6x7V8LFRZT2OBWY-OOdCrSwOQ3LuYkzCjpeYSU3XzQonEdPqEhVy7nsGIGPIldt8/pub?output=csv"

st.set_page_config(page_title="구례중 스마트 학사력", layout="wide")

# CSS: 가운데 정렬, 헤더 클릭 방지, 열 너비 강제 조정
st.markdown("""
    <style>
    th, td { text-align: center !important; vertical-align: middle !important; }
    th { pointer-events: none !important; cursor: default !important; }
    /* '일' 열 너비를 줄이기 위한 스타일 */
    [data-testid="stDataFrame"] div[class*="StyledTableCell"] { min-width: 50px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=10)
def load_data():
    try:
        # 1행(3월, 4월...)과 2행(일, 요일...)을 고려하여 로드
        df = pd.read_csv(URL, header=1)
        # 중복된 컬럼명 정리 (일, 요일, 주요일정 반복 구조)
        new_cols = []
        month_count = 3
        for i, col in enumerate(df.columns):
            if "Unnamed" in col:
                new_cols.append(f"{month_count}월_필드_{i}")
            else:
                new_cols.append(col)
        df.columns = new_cols
        return df.fillna("")
    except:
        return pd.DataFrame()

# 세션 상태로 주간 업무 저장
if 'weekly_tasks' not in st.session_state:
    st.session_state.weekly_tasks = []

# --- [2. 상단: 주간 계획 입력 (학사력 직접 반영)] ---
st.title("🏫 구례중 스마트 학사 관리 시스템")

with st.container():
    col1, col2, col3, col4 = st.columns([2, 2, 5, 2])
    with col1:
        in_date = st.date_input("날짜 선택", datetime(2026, 3, 2))
    with col2:
        in_dept = st.selectbox("부서", ["교무", "학생", "연구", "정보", "행정"])
    with col3:
        in_task = st.text_input("업무 내용 입력", placeholder="예: 신입생 오리엔테이션")
    with col4:
        st.write("") # 간격 맞춤
        if st.button("🚀 학사력 즉시 반영", use_container_width=True):
            if in_task:
                st.session_state.weekly_tasks.append({
                    'm': in_date.month, 'd': in_date.day, 'text': f"[{in_dept}] {in_task}"
                })
                st.rerun()

st.markdown("---")

# --- [3. 통합 학사력 렌더링] ---
df = load_data()

if not df.empty:
    # 주간 업무를 데이터프레임에 실제 삽입
    for task in st.session_state.weekly_tasks:
        month_str = f"{task['m']}월"
        # 해당 월의 '주요일정' 열 찾기 (보통 월 표시 바로 다음 다음 열)
        for i, col in enumerate(df.columns):
            if month_str in col:
                # 시트 구조상 '일' 열로부터 2칸 오른쪽이 주요일정
                row_idx = task['d'] - 1
                if row_idx < len(df):
                    old = str(df.iloc[row_idx, i+2])
                    df.iloc[row_idx, i+2] = (old + " / " + task['text']).strip(" / ")

    # --- 색상 및 UI 적용 함수 ---
    def apply_ui(row):
        styles = []
        for i, col in enumerate(df.columns):
            style = 'text-align: center;'
            
            # 1. 월별 색상 (홀수월: 연녹색, 짝수월: 연파란색)
            # 열 인덱스를 기준으로 월을 판별
            month_idx = (i // 3) + 3 
            if month_idx % 2 != 0: style += 'background-color: #E8F5E9;' # 연녹색
            else: style += 'background-color: #E3F2FD;' # 연파란색
            
            # 2. 연휴/빨간날 색상 (연한 빨강)
            cell_val = str(row.iloc[i])
            holidays = ["휴업", "공휴", "절", "날", "신정", "추석", "일"]
            if any(h in cell_val for h in holidays) and len(cell_val) < 10:
                style += 'background-color: #FFEBEE; color: #D32F2F; font-weight: bold;'
            
            styles.append(style)
        return styles

    # 최종 표 출력
    st.dataframe(
        df.style.apply(apply_ui, axis=1),
        use_container_width=True,
        height=750,
        hide_index=True
    )
else:
    st.info("시트 데이터를 불러오고 있습니다...")
