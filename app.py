import streamlit as st
import pandas as pd

# --- [설정] 선생님의 정보 ---
SHEET_ID = "1ez0BaGad9zQjA2S6wF48V-Fh8S5isjq00rodbFpwUkl"
SHEET_NAME = "Sheet1"  # 시트 이름을 영어로 바꾸신 것 반영

@st.cache_data(ttl=300)  # 5분마다 자동으로 시트 내용을 새로고침합니다.
def load_data(sheet_id, sheet_name):
    # 영문 시트 이름은 특수문자 에러를 일으키지 않습니다.
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    return pd.read_csv(url)

# 페이지 레이아웃 설정
st.set_page_config(page_title="교내 학사력 관리 시스템", layout="wide")

st.title("📅 스마트 학사력 및 주간 업무")

try:
    # 데이터 불러오기
    df = load_data(SHEET_ID, SHEET_NAME)
    
    st.success(f"✅ 구글 시트({SHEET_NAME})와 실시간으로 연결되었습니다.")

    # 화면 탭 구성
    tab1, tab2 = st.tabs(["🗓️ 전체 학사력 조회", "📝 주간 업무 안내"])

    with tab1:
        st.subheader("📊 현재 등록된 학사 일정")
        if not df.empty:
            # 표의 인덱스(번호)를 숨기고 화면에 꽉 차게 표시
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("시트에 데이터가 없습니다. 내용을 입력해 주세요.")

    with tab2:
        st.info("💡 구글 시트에서 내용을 수정하면 이 웹앱에 자동으로 반영됩니다.")
        st.write("1. **입력:** 구글 시트 'Sheet1'에 내용을 작성하세요.")
        st.write("2. **확인:** 웹앱 주소를 공유받은 모든 선생님이 이 화면을 보게 됩니다.")
        st.write("3. **반영:** 수정 후 약 5분 뒤에 웹앱에 나타납니다.")

except Exception as e:
    st.error("❌ 연결 중 오류가 발생했습니다.")
    st.write(f"상세 원인: {e}")
    st.info("해결 방법: 구글 시트 공유 설정이 [링크가 있는 모든 사용자 - 뷰어]인지 다시 확인해 주세요.")
