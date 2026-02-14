import streamlit as st
import pandas as pd

# --- [정밀 설정] 선생님의 시트 고유 정보 ---
# 주소창에서 확인된 고유 ID
SHEET_ID = "1ez0BaGad9zQjA2S6wF48V-Fh8S5isjq00rodbFpwUkl"
# 스크린샷에서 확인된 탭 고유 번호 (gid)
GID = "960793714" 

@st.cache_data(ttl=60) # 1분마다 시트의 변경사항을 확인합니다.
def load_data(sheet_id, gid):
    # 이름이 아닌 고유 번호(gid)를 사용하여 404 에러를 방지하는 직통 주소입니다.
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# 페이지 레이아웃 및 디자인
st.set_page_config(page_title="구례중 스마트 학사력", layout="wide")

st.title("📅 실시간 연동 학사 관리 시스템")
st.info("💡 구글 시트의 데이터가 실시간으로 반영됩니다.")

try:
    # 데이터 불러오기 실행
    df = load_data(SHEET_ID, GID)
    
    st.success("✅ 구글 시트 연결에 성공했습니다!")

    # 탭 구성
    tab1, tab2 = st.tabs(["🗓️ 전체 학사력 조회", "📖 관리 안내"])

    with tab1:
        st.subheader("📊 2026학년도 주요 학사 일정")
        if not df.empty:
            # 표 형식으로 출력 (화면에 꽉 차게, 인덱스 번호 제외)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("시트에 데이터가 비어 있습니다.")

    with tab2:
        st.markdown("""
        ### ⚙️ 시스템 관리 가이드
        1. **데이터 수정:** [구글 시트]에서 내용을 수정하면 이 앱에 자동 반영됩니다.
        2. **즉시 반영:** 수정 후 앱 화면에서 키보드의 **F5(새로고침)**를 누르세요.
        3. **주의사항:** 시트의 첫 번째 행은 제목(Header)으로 인식됩니다.
        """)

except Exception as e:
    st.error("❌ 데이터를 불러오는 데 실패했습니다.")
    st.write(f"상세 원인: {e}")
    st.info("해결책: 구글 시트 상단 [공유] 버튼 → [링크가 있는 모든 사용자 - 뷰어]로 되어 있는지 다시 한번 확인해 주세요.")
