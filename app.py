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
    main_menu = ['🏠 홈', '📖 앱 소개', '👥 고객 관리', '📊 고객 분석']
    choice = st.sidebar.radio(
        "메뉴 선택",
        main_menu,
    )

    # 구분선 추가
    st.sidebar.markdown("---")

    # 개발 과정 메뉴 별도 배치
    if st.sidebar.button('🛠️ 개발 과정'):
        choice = '🛠️ 개발 과정'

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

    return choice

    

def main():
    if 'page' not in st.session_state:
        st.session_state.page = '홈'

    # 사이드바는 항상 표시
    choice = sidebar()

    # 세션 상태에 따라 페이지 표시
    if st.session_state.page == '개발 과정':
        development_process()
    elif choice == '🏠 홈':
        home_page()
    elif choice == '📖 앱 소개':
        app_description()
    elif choice == '👥 고객 관리':
        predict_new_customer()
    elif choice == '📊 고객 분석':
        analyze_customers()

if __name__ == '__main__':
    main()