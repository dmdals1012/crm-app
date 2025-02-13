import streamlit as st

def home_page():
    st.title("👔 의류 쇼핑몰 CRM 📊")
    
    st.markdown("""
    ## 시작하기
    
    왼쪽 사이드바에서 원하는 기능을 선택하세요:
    
    - **앱 소개**: 시스템의 상세한 설명과 사용 방법을 확인합니다.
    - **고객 유형 예측**: 새로운 고객 정보를 입력하고 예측 결과를 확인합니다.
    - **데이터 분석**: 데이터를 분석하고 인사이트를 얻습니다.
    
    궁금한 점이 있으시면 언제든 고객센터로 문의해 주세요.
    """)
    
    st.image("image/crm2.jpg")
