import streamlit as st
from PIL import Image
from datetime import datetime, timedelta
import pandas as pd

from ui.description import app_description
from ui.eda import analyze_customers
from ui.home import home_page
from ui.ml import predict_new_customer
from ui.process import development_process

def sidebar():
    # 로고 추가
    try:
        logo = Image.open('path_to_your_logo.png')
        st.sidebar.image(logo, width=200)
    except FileNotFoundError:
        st.sidebar.title("고객 분석 시스템")

    st.sidebar.markdown("---")

    # 주요 메뉴 선택 (아이콘 포함)
    pages = {
        "🏠 홈": home_page,
        "📖 앱 소개": app_description,
        "👥 고객 관리": predict_new_customer,
        "📊 고객 분석": analyze_customers
    }
    
    choice = st.sidebar.radio("메뉴 선택", list(pages.keys()))

    st.sidebar.markdown("---")

    # 개발 과정 버튼 추가
    if st.sidebar.button("🛠️ 개발 과정"):
        choice = "🛠️ 개발 과정"

    st.sidebar.markdown("---")

    # 사용자 정보 섹션
    st.sidebar.subheader("사용자 정보")
    col1, col2 = st.sidebar.columns([1, 3])
    with col1:
        st.image("image/admin.jpg", width=50)  # 프로필 이미지 예시
    with col2:
        st.write("사용자: 관리자")
        st.write("부서: 데이터 분석팀")

    yesterday = datetime.now() - timedelta(days=1)
    formatted_date = yesterday.strftime("%Y-%m-%d")
    st.sidebar.text(f"마지막 접속일: {formatted_date}")

    # 추가 정보
    with st.sidebar.expander("시스템 정보"):
        st.write("버전: v1.0.0")
        st.write("최종 업데이트: 2025-02-06")

    st.sidebar.markdown("---")

    st.sidebar.info('고객센터 : 031-xxx-xxxx')

    return choice, pages

def main():
    choice, pages = sidebar()

    if choice == "🛠️ 개발 과정":
        development_process()
    else:
        pages[choice]()

if __name__ == '__main__':
    main()
