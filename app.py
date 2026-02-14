import streamlit as st
import pandas as pd

# --- 설정 ---
# 선생님의 구글 시트 ID (검증 완료)
SHEET_ID = "1ez0BaGad9zQjA2S6wF48V-Fh8S5isjq00rodbFpwUkl" 
# 시트 하단 탭 이름 (검증 완료)
SHEET_NAME = "2026.주요학사력" 

# 구글 시트를 가장 안정적으로 가져오는 함수
@st.cache_data(ttl=600)
def load_google_sheet(sheet_id):
    # 가장 오류가 적은 export 방식의 URL을 사용합니다.
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    # 시트가 여러 개일 경우 첫 번째 시트를 가져옵니다.
    return pd.read_csv(url)

st.set_page_config(page_title="스마트 학사력 관리", layout="wide")

st.title("📅 구글 시트 연동형 학사 관리 시스템")

# --- 데이터 불러오기 ---
try:
    # 데이터 로드 시도
    base_df = load_google_sheet(SHEET_ID)
    st.success("✅ 구글 시트 연동 성공!")
    
    tab1, tab2 = st.tabs(["🗓️ 월간 학사력 보기", "📝 주간 업무 입력 (안내)"])

    with tab1:
        st.subheader(f"📊 실시간 학사 일정")
        if not base_df.empty:
            # 캡처하신 시트의 3월부터 1월까지의 구조를 그대로 보여줍니다.
            st.dataframe(base_df, use_container_width=True, hide_index=True)
        else:
            st.warning("시트에 데이터가 없습니다.")

    with tab2:
        st.info("💡 조회 전용 모드입니다. 구글 시트에서 내용을 수정하면 웹앱에 반영됩니다.")

except Exception as e:
    st.error(f"❌ 연결 실패! 상세 내용을 확인해주세요.")
    st.write(f"에러 메시지: {e}")
    st.info("시트의 '공유' 설정이 [링크가 있는 모든 사용자 - 뷰어/편집자]로 되어 있는지 다시 확인해주세요.")
