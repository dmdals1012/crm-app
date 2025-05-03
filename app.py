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
    st.sidebar.title("👔 의류 쇼핑몰 CRM 📊")

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

    tab1, tab2, tab3 = st.tabs([
        f"📊 고객 분석",
        f"📈 매출 분석",
        f"👨‍👩‍👧‍👦 클러스터 분석"
    ])
    
    with tab1:
        st.subheader("고객 분석")
        st.markdown(
            """
            <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;">
            <span style="font-weight:bold;color:#262730;">🎯 목표:</span> 고객 데이터를 다각도로 분석하여 <span style="color:#e44d26;">타겟 고객</span>을 설정하고, <span style="color:#e44d26;">개인화된 마케팅 전략</span>을 수립합니다.
            <br>
            <span style="font-weight:bold;color:#262730;">✨ 주요 분석 내용:</span> 성별, 연령대, 구매 이력 등을 분석하여 고객 특성을 파악합니다.
            </div>
            """,
            unsafe_allow_html=True
        )
        analyze_gender_counts(data)
        analyze_payment_counts(data)
        analyze_age_counts(data)
        analyze_age_avg(data)
    
    with tab2:
        st.subheader("매출 분석")
        st.markdown(
            """
            <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;">
            <span style="font-weight:bold;color:#262730;">📈 목표:</span> 매출 데이터를 분석하여 <span style="color:#e44d26;">매출 트렌드</span>를 파악하고, <span style="color:#e44d26;">수익 증대</span>를 위한 의사 결정을 지원합니다.
            <br>
            <span style="font-weight:bold;color:#262730;">📊 주요 분석 내용:</span> 카테고리별, 위치별, 시즌별 매출액 등을 분석하여 매출 현황을 파악합니다.
            </div>
            """,
            unsafe_allow_html=True
        )
        analyze_category_amounts(data)
        analyze_location_amounts(data)
        analyze_season_amounts(data)
        analyze_item_amounts(data)
        analyze_season_category(data)
    
    with tab3:
        st.subheader("클러스터 분석")
        st.markdown(
            """
            <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;">
            <span style="font-weight:bold;color:#262730;">👨‍👩‍👧‍👦 목표:</span> 고객을 <span style="color:#e44d26;">유사한 그룹</span>으로 나누어 각 클러스터의 특징을 분석하고, <span style="color:#e44d26;">맞춤형 서비스</span>를 제공합니다.
            <br>
            <span style="font-weight:bold;color:#262730;">🔑 주요 분석 내용:</span> 클러스터별 구매 패턴, 리뷰 평점 등을 분석하여 클러스터 특성을 파악합니다.
            </div>
            """,
            unsafe_allow_html=True
        )
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
