

import streamlit as st
import pandas as pd
import joblib

# 저장된 모델 불러오기
model = joblib.load('model/pipeline.pkl')

cluster_descriptions = {
    0: "중장년층 단골 고객",
    1: "젊은 신규 고객(리뷰 평점 낮음)",
    2: "저가 제품 선호 고객",
    3: "고액 소비 VIP 고객",
    4: "보수적인 중장년층 고객"
}


def predict_new_customer():
    st.title("고객 관리")

    st.info('고객 정보를 입력하세요.')
    
    age = st.number_input("나이", min_value=0, max_value=120)
    purchase_amount = st.number_input("구매 금액 (USD)", min_value=0)
    review_rating = st.slider("리뷰 평점", 1, 5)
    previous_purchases = st.number_input("이전 구매 횟수", min_value=0)
    category = st.selectbox("카테고리", ['Clothing', 'Footwear', 'Outerwear', 'Accessories'])
    color = st.selectbox("색상", ['Gray', 'Maroon', 'Turquoise', 'White', 'Charcoal', 'Silver',
       'Pink', 'Purple', 'Olive', 'Gold', 'Violet', 'Teal', 'Lavender',
       'Black', 'Green', 'Peach', 'Red', 'Cyan', 'Brown', 'Beige',
       'Orange', 'Indigo', 'Yellow', 'Magenta', 'Blue'])
    season = st.selectbox("계절", ["Spring", "Summer", "Autumn", "Winter"])
    frequency = st.selectbox("구매 빈도", ["Weekly", "Monthly", "Quarterly", "Yearly"])
    
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
            st.write("이 고객은 중장년층으로, 회사에 대한 높은 충성도를 보입니다.")
            st.write("마케팅 전략 : 장기 고객 관리, 맞춤형 혜택 제공")
        elif cluster == 1:
            st.write("이 고객은 젊은 층으로, 아직 브랜드 경험이 적어 리뷰 평점이 낮습니다.")
            st.write("마케팅 전략 : 만족도 개선, 리뷰 관리, 조기 할인 유도")
        elif cluster == 2:
            st.write("이 고객은 가격에 민감하며, 주로 저가 제품을 선호합니다.")
            st.write("마케팅 전략 : 가성비 상품 추천, 프로모션 활용")
        elif cluster == 3:
            st.write("이 고객은 고가의 제품을 자주 구매하는 VIP 고객입니다.")
            st.write("마케팅 전략 : 프리미엄 제품 추천, VIP 혜택 강화")
        elif cluster == 4:
            st.write("이 고객은 중장년층으로, 새로운 제품보다는 익숙한 제품을 선호합니다.")
            st.write("마케팅 전략 : 신뢰 기반 마케팅, 기존 제품 중심 전략")

        # 새로운 고객 데이터를 CSV 파일에 저장
        input_data['Cluster'] = cluster
        input_data.to_csv('data/customer_data3.csv', mode='a', header=False, index=False)
        st.success("고객 데이터가 성공적으로 저장되었습니다.")

        