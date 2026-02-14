import streamlit as st
import pandas as pd

# --- [설정] 선생님의 구글 시트 ID (이미 확인됨) ---
SHEET_ID = "1ez0BaGad9zQjA2S6wF48V-Fh8S5isjq00rodbFpwUkl"

@st.cache_data(ttl=300)  # 5분마다 자동으로 시트 내용을 업데이트합니다.
def load_data(sheet_id):
    # 가장 오류가 적은 'export' 주소 체계를 사용합니다.
    # 이 주소는 시트의 첫 번째 탭(Sheet1)을 CSV 형태로 바로 가져옵니다.
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(url)

# 페이지 설정
st.set_page_config(page_title="교내 스마트 학사력", layout="wide")

st.title("📅 실시간 연동 학사 관리 시스템")
st.markdown("---")

try:
    # 데이터 불러오기 시도
    df = load_data(SHEET_ID)
    
    st.success("✅ 구글 시트 데이터 연동 성공!")

    # 탭 구성
    tab1, tab2 = st.tabs(["🗓️ 전체 학사력 보기", "📝 사용 및 수정 안내"])

    with tab1:
        st.subheader("📊 현재 등록된 주요 학사 일정")
        if not df.empty:
            # 시트의 데이터를 화면에 출력 (인덱스 숨김, 너비 자동 조절)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("시트에 데이터가 없습니다. 구글 시트 내용을 확인해 주세요.")

    with tab2:
        st.info("💡 구글 시트에서 내용을 수정하면 웹앱에 실시간으로 반영됩니다.")
        st.write("1. **관리자:** 구글 시트에서 일정을 추가하거나 수정하세요.")
        st.write("2. **사용자:** 공유된 웹앱 링크로 접속해 최신 학사력을 확인하세요.")
        st.write("3. **반영 시간:** 수정 후 약 5분 뒤에 웹앱에 나타납니다. (즉시 확인하려면 새로고침 F5)")

except Exception as e:
    st.error("❌ 데이터를 가져오지 못했습니다.")
    st.write(f"상세 에러 내역: {e}")
    st.info("해결책: 구글 시트 오른쪽 상단 [공유] 버튼을 눌러 '링크가 있는 모든 사용자'에게 공개되어 있는지 꼭 확인해 주세요!")
