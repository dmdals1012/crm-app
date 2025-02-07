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
    st.title("고객 분석 및 관리 시스템에 오신 것을 환영합니다! 👋")
    
    st.markdown("---")
    
    st.write("## 이 앱은 무엇을 하나요?")
    st.write("우리의 고객 분석 시스템은 여러분의 비즈니스 성장을 돕기 위해 설계되었습니다. 고객 데이터를 심층 분석하고, 머신러닝을 활용해 고객을 이해하며, 효과적인 마케팅 전략을 수립하는 데 도움을 줍니다.")
    
    st.markdown("---")
    
    st.write("## 어떤 기능들이 있나요?")

    st.write("### 1. 고객 세그먼테이션 👥")
    st.write("AI 기술을 활용해 고객을 다양한 그룹으로 나눕니다. 각 그룹의 특성을 파악하고 맞춤 전략을 세워보세요.")
    
    st.write("### 2. 데이터 분석 📊")
    st.write("데이터를 시각적으로 표현하여 쉽게 이해할 수 있습니다. 구매 패턴, 선호도 등을 한눈에 파악해보세요!")

    st.write("### 3. 실시간 분석 및 보고 📈")
    st.write("실시간으로 데이터를 분석하고 보고서를 생성합니다. 비즈니스 성과를 즉시 확인하고 대응할 수 있습니다.")

    st.markdown("---")
    
    st.write("## 개발 과정 소개")
    st.write("이 앱은 다음과 같은 과정을 거쳐 개발되었습니다:")
    st.write("1. 데이터 수집 및 전처리: Kaggle의 고객 쇼핑 데이터셋을 활용")
    st.write("2. 데이터 분석 및 모델링:")
    st.write("   - K-means 클러스터링을 통한 고객 세그먼테이션")
    st.write("   - LogisticRegression, RandomForest, XGBoost를 활용한 고객 유형 예측")
    st.write("3. Streamlit을 이용한 웹 애플리케이션 개발")
    
    st.write("고객 유형 예측에는 LogisticRegression이 97%의 정확도로 가장 우수한 성능을 보여 채택되었습니다.")

    st.markdown("---")
    
    st.write("## 어떻게 시작하나요?")
    st.write("왼쪽 사이드바에서 원하는 기능을 선택하세요. 각 기능에 대한 자세한 설명과 사용법을 확인할 수 있습니다.")

    st.markdown("---")
    
    st.write("## 더 궁금한 점이 있나요?")
    st.write("- 이메일: dmdals1012@gmail.com")
    st.write("- GitHub: https://github.com/dmdals1012/customer-app.git")
    
    st.info("이 앱은 Kaggle의 고객 쇼핑 데이터셋을 활용하여 개발되었습니다. 자세한 내용은 [여기](https://www.kaggle.com/datasets/bhadramohit/customer-shopping-latest-trends-dataset)에서 확인하실 수 있습니다.")

    st.success("고객 분석 및 관리 시스템과 함께 여러분의 비즈니스를 한 단계 더 발전시켜보세요! 🚀")
