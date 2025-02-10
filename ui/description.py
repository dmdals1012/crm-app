import streamlit as st
import pandas as pd
from PIL import Image

from ui.eda import analyze_gender_counts  # Pillow 라이브러리에서 Image 클래스 import

@st.cache_data
def load_data():
    try:
        data = pd.read_csv('data/customer_data.csv', index_col=0, engine='python', on_bad_lines='skip', sep=',', quotechar='"', escapechar='\\')
        data['Previous Purchases'] = pd.to_numeric(data['Previous Purchases'], errors='coerce')
        return data
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
        return None

def app_description():
    st.title("👔 의류 쇼핑몰 CRM 📊")
    
    st.markdown("---")
    
    st.markdown("## 이 앱은 무엇을 하나요? 🤔")
    st.markdown("**스타일 인사이트 CRM**은 **온라인 의류 쇼핑몰**의 고객 데이터를 분석하고, 머신러닝을 활용하여 고객 관계 관리(CRM)를 최적화하는 시스템입니다.")
    st.markdown("### **추천 대상:**")
    st.markdown("   - 온라인 의류 쇼핑몰 운영자")
    st.markdown("   - CRM 전략 담당자")
    st.markdown("   - 데이터 분석 및 마케팅 전문가")
    
    st.markdown("---")
    
    st.markdown("## 주요 기능 🚀")

    st.markdown("### 1. 고객 유형 예측 🎯")
    
    st.markdown("#### 예측 모델 구축")
    st.markdown("- **모델 선택**: LogisticRegression 모델을 사용하여 고객 유형을 예측합니다.")
    st.markdown("  - 다양한 모델(RandomForestClassifier, XGBClassifier 등)을 실험한 결과, LogisticRegression이 97%의 정확도로 가장 우수한 성능을 보여 채택되었습니다.")
    st.markdown("- **모델 학습**: 세분화된 고객 데이터를 사용하여 모델을 학습시킵니다.")
    st.markdown("- **모델 평가 및 최적화**: 학습된 모델의 성능을 평가하고 필요시 하이퍼파라미터 튜닝 등을 통해 최적화합니다.")

    st.markdown("#### 데이터 준비 및 고객 세분화")
    st.markdown("- **데이터 수집**: 고객의 구매 이력, 행동 패턴 등 다양한 데이터를 수집합니다.")
    
    # 데이터 프레임 표시
    data = load_data()  # 데이터 로드
    if data is not None:
        st.markdown("#### 클러스터링에 사용된 데이터 샘플")
        
        # 'Cluster' 컬럼이 있다면 제외
         # 'Cluster' 컬럼이 있다면 제외
        if 'Cluster' in data.columns:
            sample_data = data.drop('Cluster', axis=1).head()
        else:
            sample_data = data.head()
        
        st.dataframe(sample_data)  # 데이터 프레임의 처음 5행 표시 (Cluster 컬럼 제외)
        st.markdown("이 데이터는 고객의 구매 이력, 결제 방식, 사용 금액 등을 포함한 온라인 의류 쇼핑몰의 고객 정보를 나타냅니다.")
        st.markdown("위 **데이터 샘플**의 출처는 아래 **개발 과정 🛠️** 을 참고해주세요.")
    else:
        st.error("데이터를 불러오는 데 실패했습니다.")

    st.markdown("- **데이터 전처리**: 결측치 처리, 이상치 제거, 특성 스케일링 등을 수행합니다.")
    st.markdown("- **고객 세분화**: K-means 클러스터링 알고리즘을 사용하여 고객을 유사한 특성을 가진 그룹으로 세분화합니다.")
    
    # 엘보우 메소드 이미지 표시
    try:
        elbow_image = Image.open("image/elbow.png")  # 이미지 파일 경로를 여기에 입력하세요
        st.image(elbow_image, caption="엘보우 메소드", use_container_width=True)
        st.markdown("엘보우 메소드를 통해 최적의 클러스터 갯수를 분석한 결과, **6개의 클러스터**로 고객을 세분화하는 것이 가장 적합하다고 판단하였습니다.")
    except FileNotFoundError:
        st.error("엘보우 메소드 이미지를 찾을 수 없습니다. 'image/elbow.png' 경로를 확인하세요.")


    st.markdown("#### 실시간 예측 및 활용")
    st.markdown("- 새로운 고객 데이터가 입력되면, 학습된 LogisticRegression 모델을 사용하여 즉시 고객 유형을 예측합니다.")
    st.markdown("- 예측된 고객 유형에 따라 맞춤형 마케팅 전략을 수립하고 개인화된 서비스를 제공합니다.")

    st.markdown("### 2. 데이터 분석 📊")
    st.markdown("다양한 시각화 기법을 통해 고객 데이터에서 유용한 인사이트를 도출합니다.")
    st.markdown("- 다음은 데이터 분석 탭에서 보여드리는 차트 예시입니다.")

    if data is not None:
        analyze_gender_counts(data)
    else:
        st.error("데이터를 불러오는 데 실패했습니다.")

    st.markdown("#### 더 많은 분석 내용")
    st.markdown("   - 고객 그룹별 특징 및 구매 패턴 분석")
    st.markdown("   - **CRM 최적화를 위한 주요 인사이트 도출**")
    st.markdown("   - 매출 트렌드 및 주요 요인 분석")

    st.markdown("---")
    
    st.markdown("## 개발 과정 🛠️")
    st.markdown("- 사용된 데이터셋(고객 쇼핑 데이터): [Kaggle Customer Shopping Dataset](https://www.kaggle.com/datasets/bhadramohit/customer-shopping-latest-trends-dataset)")
    st.markdown("- 데이터 분석 및 모델링: K-means 클러스터링, LogisticRegression, RandomForestClassifier , XGBClassifier 등")
    st.markdown("- 개발 과정에 대한 더 자세한 내용은 [GitHub 저장소](https://github.com/dmdals1012/customer-app)를 참고해주세요.")
    st.markdown("- 여러 모델을 비교 분석 후, 정확도가 가장 높은 LogisticRegression 모델을 최종 선택")

    st.markdown("---")
    
    st.markdown("## 시작하기 🧭")
    st.markdown("왼쪽 메뉴에서 원하는 기능을 선택하세요.")

    st.markdown("---")
    
    st.markdown("## 문의 📞")
    st.markdown("- 이메일: dmdals1012@gmail.com")
    st.markdown("- GitHub: [https://github.com/dmdals1012/customer-app](https://github.com/dmdals1012/customer-app.git)")

    st.success("의류 쇼핑몰 CRM으로 고객 관계 관리를 혁신하세요! 🚀")
