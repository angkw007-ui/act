import streamlit as st
import pandas as pd
from datetime import datetime

# --- 설정 ---
# 선생님의 구글 시트 ID를 아래 따옴표 안에 넣어주세요
SHEET_ID = "1ez0BaGad9zQjA2S6wF48V-Fh8S5isjq00rodbFpwUkI" 
SHEET_NAME = "2026.주요 학사력" # 시트 하단 탭 이름

# 구글 시트를 판다스 데이터프레임으로 읽어오는 함수
@st.cache_data(ttl=600) # 10분마다 새로고침
def load_google_sheet(sheet_id, sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    return pd.read_csv(url)

st.set_page_config(page_title="스마트 학사력 관리", layout="wide")

# 로고 및 타이틀
st.title("📅 구글 시트 연동형 학사 관리 시스템")

# --- 데이터 불러오기 ---
try:
    base_df = load_google_sheet(SHEET_ID, SHEET_NAME)
    st.success("✅ 구글 시트와 성공적으로 연결되었습니다!")
except Exception as e:
    st.error(f"❌ 시트를 불러올 수 없습니다. 공유 설정을 확인해주세요. 에러: {e}")
    base_df = pd.DataFrame()

# --- 화면 구성 ---
tab1, tab2 = st.tabs(["🗓️ 월간 학사력 보기", "📝 주간 업무 입력 (기능 준비 중)"])

with tab1:
    st.subheader("구글 시트 실시간 학사 일정")
    if not base_df.empty:
        # 선생님 시트 구조에 맞게 필터링 및 정리 (예시: '주요일정' 열이 있는 경우)
        st.dataframe(base_df, use_container_width=True)
    else:
        st.info("시트에 데이터가 없습니다.")

with tab2:
    st.info("💡 주간 업무 입력 기능은 구글 시트 API 설정이 추가로 필요합니다. 현재는 조회 전용입니다.")
    st.write("구글 시트에서 직접 내용을 수정하면 10분 내로 웹앱에 반영됩니다.")
