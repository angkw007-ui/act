import streamlit as st
import pandas as pd

# --- [최종 해결책] 웹에 게시된 CSV 주소 ---
# 위 '웹에 게시' 단계에서 복사한 주소를 아래 따옴표 사이에 붙여넣으세요.
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRVGPDJQxWDyHoy6x7V8LFRZT2OBWY-OOdCrSwOQ3LuYkzCjpeYSU3XzQonEdPqEhVy7nsGIGPIldt8/pubhtml"

@st.cache_data(ttl=60)
def load_data():
    # 웹에 발행된 데이터이므로 별도의 인증 없이 즉시 로드됩니다.
    return pd.read_csv(URL)

st.set_page_config(page_title="구례중 스마트 학사력", layout="wide")
st.title("📅 실시간 연동 학사 관리 시스템")

try:
    df = load_data()
    st.success("✅ 시스템이 정상적으로 연결되었습니다!")
    
    # 데이터 출력
    st.dataframe(df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error("❌ 데이터를 불러올 수 없습니다.")
    st.info("💡 위 코드의 'URL' 부분에 [웹에 게시]에서 만든 CSV 주소를 정확히 넣었는지 확인해주세요.")
