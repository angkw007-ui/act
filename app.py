import streamlit as st
import pandas as pd

# --- [설정] 선생님의 구글 시트 고유 정보 ---
# 주소창에서 확인된 고유 ID입니다.
SHEET_ID = "1ez0BaGad9zQjA2S6wF48V-Fh8S5isjq00rodbFpwUkl"
# 선생님의 '2026.주요 학사력' 탭의 고유 번호(gid)입니다.
GID = "960793714" 

@st.cache_data(ttl=300)
def load_data(sheet_id, gid):
    # 이름 대신 고유 번호(gid)를 사용하여 404 에러를 원천 차단합니다.
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# 페이지 설정
st.set_page_config(page_title="구례중 스마트 학사력", layout="wide")

st.title("📅 실시간 연동 학사 관리 시스템")
st.info("구글 시트의 데이터가 실시간으로 반영되는 시스템입니다.")

try:
    # 고유 번호로 데이터 로드
    df = load_data(SHEET_ID, GID)
    
    st.success("✅ 학사력 데이터 연결에 성공했습니다!")

    # 탭 구성
    tab1, tab2 = st.tabs(["🗓️ 전체 학사력 조회", "📖 사용 안내"])

    with tab1:
        st.subheader("📊 2026학년도 주요 업무 및 학사력")
        if not df.empty:
            # 시트 내용을 표로 출력
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("시트에 데이터가 없습니다. 내용을 확인해 주세요.")

    with tab2:
        st.markdown("### 💡 관리자 가이드")
        st.write("1. 구글 시트에서 내용을 수정하면 이 웹앱에 **5분 이내**로 자동 반영됩니다.")
        st.write("2. 행(Row)이나 열(Column)을 마음껏 추가하셔도 됩니다.")
        st.write("3. 즉시 반영을 원하시면 웹 브라우저의 **새로고침(F5)**을 눌러주세요.")

except Exception as e:
    st.error("❌ 연결 중 예상치 못한 오류가 발생했습니다.")
    st.write(f"상세 에러 내용: {e}")
    st.info("시트의 [공유] 설정이 여전히 '링크가 있는 모든 사용자-편집자/뷰어'인지 확인해 주세요.")
