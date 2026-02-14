import streamlit as st
import pandas as pd

# --- 설정 (선생님의 시트 정보) ---
SHEET_ID = "1ez0BaGad9zQjA2S6wF48V-Fh8S5isjq00rodbFpwUkl"
# 시트 이름을 영어로 바꾸셨다면 아래에도 똑같이 적어주세요. (예: Sheet1)
SHEET_NAME = "2026.data" 

@st.cache_data(ttl=600)
def load_data(sheet_id, sheet_name):
    # 영문 시트 이름은 주소창에서 오류를 일으키지 않습니다.
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    return pd.read_csv(url)

st.set_page_config(page_title="학사력 관리 시스템", layout="wide")

st.title("📅 교내 학사력 및 업무 관리")

try:
    df = load_data(SHEET_ID, SHEET_NAME)
    
    # 상단 성공 메시지
    st.success(f"✅ '{SHEET_NAME}' 시트 연결 완료!")

    # 탭 메뉴 구성
    tab1, tab2 = st.tabs(["🗓️ 월간 학사력", "📝 주간 계획 안내"])

    with tab1:
        st.subheader("📊 실시간 학사 일정")
        # 데이터가 있으면 화면에 표시
        if not df.empty:
            # 첫 번째 열이 날짜라면 정렬해서 보여주기
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("시트에 데이터가 없습니다.")

    with tab2:
        st.info("💡 구글 시트에서 내용을 수정하고 약 5~10분 뒤 새로고침하면 반영됩니다.")
        st.write("1. 구글 시트에서 일정을 관리하세요.")
        st.write("2. 웹앱은 전 교사가 동시에 조회할 수 있습니다.")

except Exception as e:
    st.error("❌ 시트를 불러오는데 실패했습니다.")
    st.write(f"오류 메시지: {e}")
    st.info("팁: 구글 시트의 탭 이름이 코드의 SHEET_NAME과 정확히 일치하는지 확인해주세요!")
