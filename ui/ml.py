import streamlit as st
import pandas as pd
import joblib

# 저장된 모델 불러오기
model = joblib.load('model/pipeline.pkl')

cluster_descriptions = {
    0: "고액 소비 VIP 고객",
    1: "젊은 신규 고객",
    2: "중간 소비 젊은 고객",
    3: "중년층 충성 고객",
    4: "보수적인 중장년층 고객",
    5: "가격에 민감한 중년층 고객"
}

def predict_new_customer():
    st.title("고객 관리")

    st.info('고객 정보를 입력하세요. 정확도도 97%의 인공지능이 고객의 유형과 마케팅 전략을 알려줍니다.')

    st.markdown("---")

    st.markdown("## 머신러닝 과정 ⚙️")
    st.markdown("이 모델은 K-means 클러스터링과 Logistic Regression을 사용하여 고객 유형을 예측합니다. 자세한 내용은 **앱 소개** 탭을 참고해주세요.")
    
    age = st.number_input("나이", min_value=18, max_value=70)
    purchase_amount = st.number_input("구매 금액 (USD)", min_value=20, max_value=100)
    review_rating = st.slider("리뷰 평점", 2.5, 5.0, 3.5)
    previous_purchases = st.number_input("이전 구매 횟수", min_value=0, max_value=50)
    category = st.selectbox("카테고리", ['Clothing', 'Footwear', 'Outerwear', 'Accessories'])
    color = st.selectbox("색상", ['Gray', 'Maroon', 'Turquoise', 'White', 'Charcoal', 'Silver',
       'Pink', 'Purple', 'Olive', 'Gold', 'Violet', 'Teal', 'Lavender',
       'Black', 'Green', 'Peach', 'Red', 'Cyan', 'Brown', 'Beige',
       'Orange', 'Indigo', 'Yellow', 'Magenta', 'Blue'])
    season = st.selectbox("계절", ["Spring", "Summer", "Fall", "Winter"])
    frequency = st.selectbox("구매 빈도", ["Weekly", "Fortnightly", "Monthly", "Quarterly", "Bi-Weekly", "Annually", "Every 3 Months"])
    
    if st.button("예측"):
        input_data = pd.DataFrame({
            'Age': [age],
            'Purchase Amount (USD)': [purchase_amount],
            'Review Rating': [review_rating],
            'Previous Purchases': [previous_purchases],
            'Category': [category],
            'Color': [color],
            'Season': [season],
            'Frequency of Purchases': [frequency]
        })
        
        prediction = model.predict(input_data)
        cluster = prediction[0]
        description = cluster_descriptions.get(cluster, "알 수 없는 그룹")
        
        st.write(f"특징 : {description}")
        
        # 추가적인 그룹별 특성 설명
        if cluster == 0:
            st.write("이 고객은 고액을 자주 소비하는 VIP 고객입니다.")
            st.write("마케팅 전략 : 프리미엄 제품 추천, 개인화된 VIP 서비스 제공")
        elif cluster == 1:
            st.write("이 고객은 젊은 층으로, 다양한 제품을 시도하는 경향이 있습니다.")
            st.write("마케팅 전략 : 트렌디한 제품 추천, 소셜 미디어 마케팅 강화")
        elif cluster == 2:
            st.write("이 고객은 젊은 층이지만 중간 정도의 구매력을 가지고 있습니다.")
            st.write("마케팅 전략 : 가성비 좋은 중급 제품 추천, 로열티 프로그램 참여 유도")
        elif cluster == 3:
            st.write("이 고객은 중년층으로, 브랜드에 대한 높은 충성도를 보입니다.")
            st.write("마케팅 전략 : 장기 고객 혜택 강화, 신제품 우선 체험 기회 제공")
        elif cluster == 4:
            st.write("이 고객은 중장년층으로, 익숙한 제품을 선호하고 변화를 꺼립니다.")
            st.write("마케팅 전략 : 신뢰성 강조, 기존 제품의 개선점 홍보")
        elif cluster == 5:
            st.write("이 고객은 중년층이지만 가격에 민감하며 할인을 선호합니다.")
            st.write("마케팅 전략 : 할인 행사 정보 우선 제공, 가격 대비 품질 강조")

        # 새로운 고객 데이터를 CSV 파일에 저장
        input_data['Cluster'] = cluster
        input_data.to_csv('data/customer_data3.csv', mode='a', header=False, index=False)
        st.success("고객 데이터가 성공적으로 저장되었습니다.")
