import streamlit as st
from PIL import Image
from datetime import datetime, timedelta
import pandas as pd

from ui.description import app_description
from ui.home import home_page
from ui.ml import predict_new_customer
from ui.eda import analyze_age_avg, analyze_age_counts, analyze_category_amounts, analyze_cluster_age_distribution, analyze_cluster_purchase, analyze_cluster_rating, analyze_cluster_sales, analyze_gender_counts, analyze_item_amounts, analyze_location_amounts, analyze_payment_counts, analyze_season_amounts, analyze_season_category, load_data

def sidebar():
    # 사이드바 제목
    st.sidebar.title("👔 의류 온라인쇼핑몰 CRM 📊")

    st.sidebar.markdown("---")

    # 주요 메뉴 선택 (아이콘 포함)
    pages = {
        "🏠 홈": home_page,
        "📖 앱 소개": app_description,
        "🎯 고객 유형 예측": predict_new_customer,
        "📊 데이터 분석": lambda: data_analysis_page()
    }
    
    choice = st.sidebar.radio("메뉴 선택", list(pages.keys()))

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

def data_analysis_page():
    data = load_data()
    if data is None:
        st.error("데이터를 불러오는 데 실패했습니다.")
        return

    tab1, tab2, tab3 = st.tabs(["고객 분석", "매출 분석", "클러스터 분석"])
    
    with tab1:
        st.header("고객 관련 데이터 분석")
        st.write("고객 관련 데이터를 분석하여 인사이트를 도출합니다.")
        analyze_gender_counts(data)
        analyze_payment_counts(data)
        analyze_age_counts(data)
        analyze_age_avg(data)
    
    with tab2:
        st.header("매출 관련 데이터 분석")
        st.write("매출 관련 데이터를 분석하여 인사이트를 도출합니다.")
        analyze_category_amounts(data)
        analyze_location_amounts(data)
        analyze_season_amounts(data)
        analyze_item_amounts(data)
        analyze_season_category(data)
    
    with tab3:
        st.header("클러스터 관련 데이터 분석")
        st.write("클러스터 관련 데이터를 분석하여 인사이트를 도출합니다.")
        analyze_cluster_purchase(data)
        analyze_cluster_rating(data)
        analyze_cluster_sales(data)
        analyze_cluster_age_distribution(data)

def main():
    choice = sidebar()

    if choice == "🏠 홈":
        home_page()
    elif choice == "📖 앱 소개":
        app_description()
    elif choice == "🎯 고객 유형 예측":
        predict_new_customer()
    elif choice == "📊 데이터 분석":
        data_analysis_page()

if __name__ == '__main__':
    main()
