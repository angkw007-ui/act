import streamlit as st

# 페이지 설정: 화면을 넓게 쓰고 제목을 정합니다.
st.set_page_config(page_title="2026 구례중 주요업무일정", layout="wide")

# 상단 제목
st.title("📅 2026 구례중학교 주요업무 시스템 (실시간)")

# --- [중요] 여기에 1단계에서 복사한 '매립' 주소를 넣으세요 ---
# 주의: 끝이 /pubhtml 형태여야 시트의 모든 탭(1, 2, 3)이 다 보입니다.
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRVGPDJQxWDyHoy6x7V8LFRZT2OBWY-OOdCrSwOQ3LuYkzCjpeYSU3XzQonEdPqEhVy7nsGIGPIldt8/pubhtml?widget=true&headers=false"

# 구글 시트를 화면에 꽉 차게 그리는 마법의 코드
st.components.v1.iframe(sheet_url, height=900, scrolling=True)

st.info("💡 하단의 탭(2026.data, Month, Week)을 클릭하여 이동할 수 있습니다. 수정은 구글 시트에서 하세요!")
