ㅁimport streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- [1. 데이터 로드 및 환경 설정] ---
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRVGPDJQxWDyHoy6x7V8LFRZT2OBWY-OOdCrSwOQ3LuYkzCjpeYSU3XzQonEdPqEhVy7nsGIGPIldt8/pub?output=csv"

st.set_page_config(page_title="구례중 통합 업무 시스템", layout="wide")

# UI 스타일: 가운데 정렬 및 헤더 클릭 방지용 CSS
st.markdown("""
    <style>
    .main { text-align: center; }
    /* 헤더 클릭 방지 및 커서 기본값 설정 */
    th { pointer-events: none !important; cursor: default !important; background-color: #f8f9fa !important; text-align: center !important; }
    td { text-align: center !important; }
    div[data-testid="stDataFrame"] { font-family: 'Malgun Gothic', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=10)
def load_data():
    try:
        # 시트의 2번째 줄부터 읽어오기 (Unnamed 제거)
        df = pd.read_csv(URL, header=1)
        # 헤더 이름을 깔끔하게 정리 (숫자만 남기기 등)
        df.columns = [c.replace(".1", "").replace(".2", "") for c in df.columns]
        return df.fillna("")
    except:
        return pd.DataFrame()

# 세션 상태를 이용해 입력된 주간 업무를 임시 저장 (실제 운영시 DB나 파일저장 연결 가능)
if 'weekly_data' not in st.session_state:
    st.session_state.weekly_data = []

# --- [2. 주간 업무 입력 (학사력 직접 반영)] ---
st.title("🏫 구례중 주간/월간 업무 통합 시스템")

with st.container():
    st.subheader("📝 주간 계획 입력 (입력 시 해당 날짜 칸에 즉시 추가)")
    c1, c2, c3, c4 = st.columns([2, 2, 4, 2])
    with c1:
        sel_date = st.date_input("날짜", datetime(2026, 3, 2)) # 2026학년도 기준
    with c2:
        sel_dept = st.selectbox("부서", ["교무", "학생", "연구", "정보", "행정"])
    with c3:
        sel_task = st.text_input("업무 내용", placeholder="예: 학부모 상담주간")
    with c4:
        if st.button("🚀 학사력 반영"):
            if sel_task:
                st.session_state.weekly_data.append({
                    'month': sel_date.month,
                    'day': sel_date.day,
                    'text': f"[{sel_dept}] {sel_task}"
                })
                st.success("반반영되었습니다!")
                st.rerun()

st.markdown("---")

# --- [3. 통합 학사력 렌더링] ---
df = load_data()

if not df.empty:
    # 주간 업무를 데이터프레임에 병합
    for item in st.session_state.weekly_data:
        target_col = f"{item['month']}월"
        # '주요일정' 열을 찾아서 텍스트 추가 (시트 구조에 따라 열 인덱스 조정)
        for i, col in enumerate(df.columns):
            if target_col in col and "주요일정" in df.iloc[0, i+2 if i+2 < len(df.columns) else i]:
                row_idx = item['day'] - 1
                if row_idx < len(df):
                    original_val = df.iloc[row_idx, i+2]
                    df.iloc[row_idx, i+2] = f"{original_val} / {item['text']}" if original_val else item['text']

    # --- 색상 입히기 함수 ---
    def style_calendar(row):
        styles = []
        for col in df.columns:
            base = 'text-align: center;'
            # 월별 색상 (홀수: 연녹색, 짝수: 연파란색)
            try:
                m_num = int(''.join(filter(str.isdigit, col[:3])))
                if m_num % 2 != 0: base += 'background-color: #E8F5E9;'
                else: base += 'background-color: #E3F2FD;'
            except: pass
            
            # 열 너비 조정 ('일' 열은 좁게)
            if col == "일": base += 'width: 30px;'
            
            # 연휴/빨간날 감지 (글자에 특정 키워드 포함 시)
            cell_val = str(row[col])
            if any(k in cell_val for k in ["휴업", "공휴", "절", "날", "신정", "추석"]):
                base += 'background-color: #FFEBEE; color: #D32F2F; font-weight: bold;'
            
            styles.append(base)
        return styles

    # 표 출력
    st.dataframe(
        df.style.apply(style_calendar, axis=1),
        use_container_width=True,
        height=800,
        hide_index=True
    )
else:
    st.warning("데이터를 불러오는 중입니다. 잠시만 기다려주세요.")
