import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
    try:
        data = pd.read_csv('data/customer_data.csv', index_col=0, engine='python', on_bad_lines='skip', sep=',', quotechar='"', escapechar='\\')
        data['Previous Purchases'] = pd.to_numeric(data['Previous Purchases'], errors='coerce')
        # 컬럼명 'Cluster' → '고객유형'으로 변경
        if 'Cluster' in data.columns:
            data = data.rename(columns={'Cluster': '고객유형'})
        return data
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
        return None

# 고객유형 매핑 정보
customer_type_names = {
    0: "고액 소비 VIP 고객",
    1: "젊은 신규 고객",
    2: "중간 소비 젊은 고객",
    3: "중년층 충성 고객",
    4: "보수적인 중장년층 고객",
    5: "가격에 민감한 중년층 고객"
}

def get_customer_type_name(idx):
    return customer_type_names.get(idx, f"유형 {idx}")

def analyze_gender_counts(data):
    st.subheader("성별에 따른 구매 건수 분석")
    gender_counts = data['Gender'].value_counts()
    fig_gender = px.bar(x=gender_counts.index, y=gender_counts.values,
                         labels={'x': '성별', 'y': '구매 건수'},
                         title='성별별 구매 건수')
    st.plotly_chart(fig_gender)
    
    total = gender_counts.sum()
    male_per = (gender_counts.get('Male', 0)/total)*100
    female_per = (gender_counts.get('Female', 0)/total)*100
    st.markdown(f"- 남성 **{male_per:.1f}%** / 여성 **{female_per:.1f}%**")

def analyze_payment_counts(data):
    st.subheader("선호 결제 방식별 구매 건수 분석")
    payment_counts = data['Preferred Payment Method'].value_counts()
    fig = px.bar(payment_counts)
    st.plotly_chart(fig)

def analyze_age_counts(data):
    st.subheader("연령대별 구매 건수 분석")
    data['Age Group'] = pd.cut(data['Age'], bins=[0,20,30,40,50,60,100], 
                             labels=['0-20','21-30','31-40','41-50','51-60','60+'])
    age_counts = data['Age Group'].value_counts()
    fig = px.bar(age_counts)
    st.plotly_chart(fig)

def analyze_category_amounts(data):
    st.subheader("카테고리별 총 구매 금액 분석")
    amounts = data.groupby('Category')['Purchase Amount (USD)'].sum()
    fig = px.bar(amounts)
    st.plotly_chart(fig)

def analyze_location_amounts(data):
    st.subheader("위치별 총 구매 금액 분석")
    amounts = data.groupby('Location')['Purchase Amount (USD)'].sum()
    fig = px.bar(amounts)
    st.plotly_chart(fig)

def analyze_season_amounts(data):
    st.subheader("시즌별 총 구매 금액 분석")
    amounts = data.groupby('Season')['Purchase Amount (USD)'].sum()
    fig = px.bar(amounts)
    st.plotly_chart(fig)

def analyze_item_amounts(data):
    st.subheader("상품별 총 구매 금액 분석")
    amounts = data.groupby('Item Purchased')['Purchase Amount (USD)'].sum().nlargest(10)
    fig = px.bar(amounts)
    st.plotly_chart(fig)

def analyze_season_category(data):
    st.subheader("계절별 카테고리 구매 패턴")
    filtered = data[data['Season'].isin(['Spring','Summer','Fall','Winter'])]
    ct = pd.crosstab(filtered['Season'], filtered['Category'])
    fig = px.bar(ct, barmode='group')
    st.plotly_chart(fig)

def analyze_age_avg(data):
    st.subheader("연령대별 평균 구매 금액")
    data['Age Group'] = pd.cut(data['Age'], bins=[0,20,30,40,50,60,100],
                             labels=['0-20','21-30','31-40','41-50','51-60','60+'])
    avg = data.groupby('Age Group')['Purchase Amount (USD)'].mean()
    fig = px.bar(avg)
    st.plotly_chart(fig)

# 클러스터 → 고객유형으로 변경된 함수들
def analyze_customer_type_purchase(data):
    st.subheader("고객유형별 평균 구매 금액")
    avg = data.groupby('고객유형')['Purchase Amount (USD)'].mean()
    avg.index = [get_customer_type_name(i) for i in avg.index]  # 숫자 → 이름 변환
    fig = px.bar(avg)
    st.plotly_chart(fig)

def analyze_customer_type_rating(data):
    st.subheader("고객유형별 평균 리뷰 평점")
    avg = data.groupby('고객유형')['Review Rating'].mean()
    avg.index = [get_customer_type_name(i) for i in avg.index]
    fig = px.bar(avg)
    st.plotly_chart(fig)

def analyze_customer_type_sales(data):
    st.subheader("고객유형별 총 매출액")
    sales = data.groupby('고객유형')['Purchase Amount (USD)'].sum()
    sales.index = [get_customer_type_name(i) for i in sales.index]
    fig = px.bar(sales)
    st.plotly_chart(fig)

def analyze_customer_type_age_distribution(data):
    st.subheader("고객유형별 연령 분포")
    data['Age Group'] = pd.cut(data['Age'], bins=[0,20,30,40,50,60,100],
                             labels=['0-20','21-30','31-40','41-50','51-60','60+'])
    ct = data.groupby(['고객유형', 'Age Group']).size().unstack()
    ct.index = [get_customer_type_name(i) for i in ct.index]  # 인덱스 이름 변환
    fig = px.bar(ct, barmode='stack')
    st.plotly_chart(fig)
