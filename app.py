import streamlit as st
import pandas as pd
import urllib.parse  # 띄어쓰기 에러를 해결하기 위한 도구

# --- 설정 ---
# 선생님의 구글 시트 ID (캡처해주신 주소창에서 확인된 값)
SHEET_ID = "1ez0BaGad9zQjA2S6wF48V-Fh8S5isjq00rodbFpwUkl" 
SHEET_NAME = "2026.주요학사력" 

# 구글 시트를 안전하게 읽어오는 함수
@st.cache_data(ttl=600)
def load_google_sheet(sheet_id, sheet_name):
    # 띄어쓰기나 한글을 웹 주소 형식으로 변환 (핵심 수정!)
    encoded_name = urllib.parse.quote(sheet_name)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_name}"
    return pd.read_csv(url)

st.set_page_config(page_title="스마트 학사력 관리", layout="wide")

st.title("📅 구글 시트 연동형 학사 관리 시스템")

# --- 데이터 불러오기 ---
try:
    # 띄어쓰기 문제를 해결한 함수 호출
    base_df = load_google_sheet(SHEET_ID, SHEET_NAME)
    st.success("✅ 구글 시트와 연결에 성공했습니다!")
    
    tab1, tab2 = st.tabs(["🗓️ 월간 학사력 보기", "📝 주간 업무 입력 (안내)"])

    with tab1:
        st.subheader(f"📊 {SHEET_NAME} 일정")
        if not base_df.empty:
            # 시트 내용을 예쁘게 표로 보여주기
            st.dataframe(base_df, use_container_width=True, hide_index=True)
        else:
            st.warning("시트에 데이터가 없습니다. 내용을 입력해주세요.")

    with tab2:
        st.info("💡 조회 전용 모드입니다. 구글 시트에서 내용을 수정하면 웹앱에 자동 반영됩니다.")

except Exception as e:
    st.error(f"❌ 연결 실패! 공유 설정을 다시 확인해주세요.")
    st.write(f"상세 에러 내용: {e}")
