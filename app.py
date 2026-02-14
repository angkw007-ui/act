import streamlit as st
import pandas as pd

# --- [설정] 선생님의 구글 시트 ID ---
# 캡처 화면에서 확인된 ID입니다.
SHEET_ID = "1ez0BaGad9zQjA2S6wF48V-Fh8S5isjq00rodbFpwUkl"

@st.cache_data(ttl=300)  # 5분마다 자동으로 시트의 새로운 내용을 가져옵니다.
def load_data(sheet_id):
    # 가장 에러가 없는 export 방식을 사용합니다.
    # 이 방식은 첫 번째 시트를 자동으로 가져옵니다.
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(url)

# 페이지 레이아웃 및 디자인
st.set_page_config(page_title="교내 스마트 학사력", layout="wide")

st.title("📅 실시간 연동 학사 관리 시스템")
st.markdown("---")

try:
    # 데이터 불러오기 실행
    df = load_data(SHEET_ID)
    
    st.success("✅ 구글 시트 데이터 연결에 성공했습니다!")

    # 탭 구성
    tab1, tab2 = st.tabs(["🗓️ 전체 일정 보기", "ℹ️ 사용 안내"])

    with tab1:
        st.subheader("📊 현재 등록된 주요 학사 일정")
        if not df.empty:
            # 표 형식으로 출력 (화면에 꽉 차게, 인덱스 번호 제외)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("시트에 데이터가 없습니다. 구글 시트 내용을 확인해 주세요.")

    with tab2:
        st.info("💡 구글 시트에서 내용을 수정하고 약 5분 뒤 새로고침(F5)을 하세요.")
        st.write("1. **관리자:** 구글 시트에서 일정을 추가/수정/삭제합니다.")
        st.write("2. **사용자:** 공유된 웹앱 링크를 통해 실시간 일정을 조회합니다.")
        st.write("3. **장점:** 별도의 로그인 없이 누구나 최신 학사력을 확인할 수 있습니다.")

except Exception as e:
    st.error("❌ 시트 연결 중 오류가 발생했습니다.")
    st.write(f"상세 에러 내역: {e}")
    st.info("체크리스트: 구글 시트의 [공유] 설정이 '링크가 있는 모든 사용자 - 뷰어'인지 확인해 주세요.")
