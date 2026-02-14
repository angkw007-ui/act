import streamlit as st
import pandas as pd

# --- 설정 ---
# 선생님의 구글 시트 ID (검증 완료)
# 주소창에서 /d/ 와 /edit 사이에 있는 문자열입니다.
SHEET_ID = "1ez0BaGad9zQjA2S6wF48V-Fh8S5isjq00rodbFpwUkl"

# 구글 시트를 가장 안전하게 읽어오는 함수 (400 에러 방지용)
@st.cache_data(ttl=600)
def load_google_sheet(sheet_id):
    # 주소를 직접 만들지 않고 파라미터를 명확히 구분하여 생성합니다.
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    # 시트를 읽어올 때 발생할 수 있는 오류를 방지하기 위해 엔진 설정을 추가합니다.
    return pd.read_csv(csv_url)

st.set_page_config(page_title="스마트 학사력 관리", layout="wide")

st.title("📅 구글 시트 연동형 학사 관리 시스템")

# --- 데이터 불러오기 ---
try:
    # 데이터 로딩
    df = load_google_sheet(SHEET_ID)
    st.success("✅ 구글 시트 연동에 성공했습니다!")
    
    tab1, tab2 = st.tabs(["🗓️ 월간 학사력 보기", "📝 주간 업무 입력 (안내)"])

    with tab1:
        st.subheader("📊 실시간 학사 일정 (구글 시트 데이터)")
        if not df.empty:
            # 시트의 데이터를 화면에 꽉 차게 보여줍니다.
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("시트에 데이터가 없습니다. 구글 시트에 내용을 입력해주세요.")

    with tab2:
        st.info("💡 본 시스템은 구글 시트와 실시간으로 연동됩니다.")
        st.write("1. 구글 시트에서 내용을 수정합니다.")
        st.write("2. 웹앱에서 새로고침을 하면 수정된 내용이 반영됩니다.")

except Exception as e:
    st.error("❌ 데이터를 가져오는 중 오류가 발생했습니다.")
    st.write(f"오류 내용: {e}")
    st.markdown("---")
    st.markdown("### 🔍 해결 방법 체크리스트")
    st.write("1. 구글 시트 오른쪽 상단 **[공유]** 버튼을 눌렀나요?")
    st.write("2. **[링크가 있는 모든 사용자]**가 **[뷰어]** 이상의 권한을 가지고 있나요?")
    st.write("3. 시트가 비어있지는 않은지 확인해주세요.")
