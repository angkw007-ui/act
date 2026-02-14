import streamlit as st
import pandas as pd

# --- [정밀 설정] 선생님의 구글 시트 고유 정보 ---
# 1. 시트 ID (검증 완료)
SHEET_ID = "1ez0BaGad9zQjA2S6wF48V-Fh8S5isjq00rodbFpwUkl"
# 2. 탭 고유 번호 (선생님의 주소창 gid값 반영)
GID = "960793714" 

@st.cache_data(ttl=300)
def load_data(sheet_id, gid):
    # 시트 이름 대신 고유 번호(gid)를 직접 호출하여 404 에러를 원천 차단합니다.
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# 페이지 레이아웃 설정
st.set_page_config(page_title="구례중 스마트 학사력", layout="wide")

st.title("📅 실시간 연동 학사 관리 시스템")
st.info("구글 시트의 데이터가 실시간으로 반영되는 시스템입니다.")

try:
    # 데이터 로딩 실행
    df = load_data(SHEET_ID, GID)
    
    st.success("✅ 학사력 데이터 연결에 성공했습니다!")

    # 화면 구성
    tab1, tab2 = st.tabs(["🗓️ 전체 일정 조회", "📖 관리자 안내"])

    with tab1:
        st.subheader("📊 2026학년도 주요 학사 일정")
        if not df.empty:
            # 첫 번째 행을 컬럼으로 사용하여 깔끔하게 출력
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("시트에 데이터가 보이지 않습니다. 내용을 확인해 주세요.")

    with tab2:
        st.markdown("""
        ### 💡 데이터 수정 방법
        1. 연결된 [구글 시트]에서 내용을 수정합니다.
        2. 수정 후 약 **5분** 뒤에 이 웹앱에 자동으로 반영됩니다.
        3. 즉시 확인하려면 브라우저의 **새로고침(F5)**을 눌러주세요.
        """)

except Exception as e:
    st.error("❌ 연결 중 예상치 못한 오류가 발생했습니다.")
    st.write(f"알림: {e}")
    st.info("시트의 [공유] 설정이 '링크가 있는 모든 사용자-편집자/뷰어' 상태인지 마지막으로 확인해 주세요.")
