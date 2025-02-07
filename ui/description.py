import streamlit as st
import pandas as pd

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-attachment: fixed;
             background-size: cover
         }}
         .css-1d391kg {{
             background-color: rgba(255, 255, 255, 0.8);
             padding: 20px;
             border-radius: 10px;
         }}
         </style>
         """,
         unsafe_allow_html=True
    )


def app_description():
    st.title("고객 분석 및 관리 시스템")
    
    st.write("## 프로젝트 개요")
    st.write("이 앱은 고객 데이터를 분석하고 관리하는 종합 시스템입니다. 머신러닝 기술을 활용하여 고객 세그먼테이션을 수행하고, 데이터 시각화를 통해 인사이트를 제공합니다.")
    
    st.write("## 주요 기능")
    
    # 고객 데이터 분석
    st.write("### 1. 고객 데이터 분석")
    col1, col2 = st.columns(2)
    with col1:
        st.write("- **데이터 시각화**: 고객 데이터를 그래프, 차트 등으로 시각화하여 직관적인 인사이트 제공")
        st.write("- **통계적 분석**: 고객 행동 패턴, 구매 이력 등에 대한 심층적인 통계 분석 수행")
    with col2:
        st.write("- **리포팅 및 대시보드**: 주요 지표를 한눈에 볼 수 있는 맞춤형 대시보드 제공")
    
    # 고객 세그먼테이션
    st.write("### 2. 고객 세그먼테이션")
    col1, col2 = st.columns(2)
    with col1:
        st.write("- **머신러닝 기반 클러스터링**: K-means, 의사결정 트리, 랜덤 포레스트 등 다양한 알고리즘을 활용한 고객 그룹화")
        st.write("- **고객 그룹 특성 분석**: 각 세그먼트의 특징을 자동으로 추출하고 요약")
    with col2:
        st.write("- **다차원 세그먼테이션**: 인구통계학적, 행동적, 심리적 요소를 종합적으로 고려한 세분화")
    
    # 신규 고객 예측
    st.write("### 3. 신규 고객 예측")
    col1, col2 = st.columns(2)
    with col1:
        st.write("- **고객 그룹 예측**: 새로운 고객의 특성을 분석하여 가장 적합한 세그먼트에 자동 배정")
        st.write("- **맞춤형 마케팅 전략 제안**: 각 고객 그룹에 최적화된 마케팅 접근 방식 추천")
    with col2:
        st.write("- **리드 스코어링**: 잠재 고객의 구매 가능성을 점수화하여 우선순위 설정")
    
    # CRM 기능
    st.write("### 4. CRM 기능")
    col1, col2 = st.columns(2)
    with col1:
        st.write("- **리드 관리**: 잠재 고객 정보 관리 및 영업 기회 추적")
        st.write("- **이메일 마케팅**: 고객 세그먼트별 맞춤형 이메일 캠페인 설계 및 실행")
    with col2:
        st.write("- **판매 예측**: 과거 데이터를 기반으로 한 정확한 매출 예측")
        st.write("- **고객 서비스 통합**: 티켓 관리 시스템을 통한 효율적인 고객 지원")
    
    # 분석 및 보고
    st.write("### 5. 분석 및 보고")
    col1, col2 = st.columns(2)
    with col1:
        st.write("- **실시간 애널리틱스**: 고객 행동 및 캠페인 성과에 대한 실시간 분석")
        st.write("- **성과 메트릭**: 주요 성과 지표(KPI) 추적 및 목표 대비 실적 분석")
    with col2:
        st.write("- **커스텀 리포트**: 사용자 정의 보고서 생성 기능")
    
    st.write("이러한 기능들을 통해 기업은 고객을 더 깊이 이해하고, 효과적인 마케팅 전략을 수립하며, 고객 관계를 지속적으로 개선할 수 있습니다.")


    st.write("## 개발자 정보")
    
    st.write("- Email: dmdals1012@gmail.com")
    st.write("- GitHub: https://github.com/dmdals1012/customer-app.git")
    
    st.write("---")
    st.write("이 프로젝트에 대해 더 자세히 알고 싶으시다면, 사이드바에서 각 기능을 선택해 보세요.")
    st.write("데이터는 kaggle 사이트에서 가져와 학습하였습니다. (https://www.kaggle.com/datasets/bhadramohit/customer-shopping-latest-trends-dataset)")