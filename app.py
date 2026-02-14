import streamlit as st
import pandas as pd

# --- [정밀 설정] 선생님의 구글 시트 정보 ---
# 주소창에서 확인된 고유 ID입니다.
SHEET_ID = "1ez0BaGad9zQjA2S6wF48V-Fh8S5isjq00rodbFpwUkl"
# 주소창 끝에 있는 gid=960793714 값을 직접 넣었습니다.
GID = "960793714" 

@st.cache_data(ttl=300)
def load_data(sheet_id, gid):
    # 시트 이름 대신 gid 번호를 사용하여 404 에러를 원천 차단합니다.
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# 페이지 레이아웃 설정
st.set_page_config(page_title="구례중 스마트 학사력", layout="wide")

st.title("📅 실시간 연동 학사 관리 시스템")
st.markdown("---")

try:
    # gid 번호를 통해 정확한 탭의 데이터를 가져옵니다.
    df = load_data(SHEET_ID, GID)
    
    st.success("✅ 구글 시트 데이터 연결에 성공했습니다!")

    tab1, tab2 = st.tabs(["🗓️ 전체 학사력 조회", "ℹ️ 시스템 안내"])

    with tab1:
        st.subheader("📊 2026학년도 주요 학사 일정")
        if not df.empty:
            # 첫 번째 행을 제목으로 사용하여 표를 출력합니다.
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("시트에 데이터가 없습니다. 내용을 확인해 주세요.")

    with tab2:
        st.info("💡 구글 시트에서 내용을 수정하면 웹앱에 자동으로 반영됩니다.")
        st.write("1. **수정:** 구글 시트에서 일정이나 업무를 변경하세요.")
        st.write("2. **반영:** 수정 후 약 5분 뒤에 웹앱에 나타납니다.")
        st.write("3. **즉시 확인:** 브라우저의 새로고침(F5)을 눌러주세요.")

except Exception as e:
    st.error("❌ 연결 중 예상치 못한 오류가 발생했습니다.")
    st.write(f"상세 에러 내역: {e}")
    st.info("팁: 구글 시트의 [공유] 설정이 '링크가 있는 모든 사용자-뷰어'인지 마지막으로 확인해 주세요.")
