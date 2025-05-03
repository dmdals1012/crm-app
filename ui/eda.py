import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    try:
        data = pd.read_csv('data/customer_data.csv', index_col=0, engine='python', on_bad_lines='skip', sep=',', quotechar='"', escapechar='\\')
        data['Previous Purchases'] = pd.to_numeric(data['Previous Purchases'], errors='coerce')
        return data
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
        return None

# 고객 유형 번호별 이름
customer_type_names = {
    0: "고액 소비 VIP 고객",
    1: "젊은 신규 고객",
    2: "중간 소비 젊은 고객",
    3: "중년층 충성 고객",
    4: "보수적인 중장년층 고객",
    5: "가격에 민감한 중년층 고객"
}

def show_customer_types(data):
    if "고객유형" in data.columns:
        st.markdown("### 🏷️ 고객 유형 분류")
        for k, v in customer_type_names.items():
            st.markdown(f"- 고객 유형 {k} : {v}")
        st.markdown("---")

def get_customer_type_name(idx):
    return customer_type_names.get(idx, f"유형 {idx}")

def analyze_gender_counts(data):
    st.subheader("성별에 따른 구매 건수 분석")
    gender_counts = data['Gender'].value_counts()
    fig_gender = px.bar(x=gender_counts.index, y=gender_counts.values,
                         labels={'x': '성별', 'y': '구매 건수'},
                         title='성별별 구매 건수')
    st.plotly_chart(fig_gender, key='gender_chart')
    total_purchases = gender_counts.sum()
    male_percentage = (gender_counts.get('Male', 0) / total_purchases) * 100
    female_percentage = (gender_counts.get('Female', 0) / total_purchases) * 100
    st.markdown(f"- 남성 구매자는 전체 구매의 **{male_percentage:.1f}%** 를 차지하며, 여성 구매자는 **{female_percentage:.1f}%** 를 차지합니다. 📊")

def analyze_payment_counts(data):
    st.subheader("선호 결제 방식별 구매 건수 분석")
    payment_counts = data['Preferred Payment Method'].value_counts()
    fig_payment = px.bar(x=payment_counts.index, y=payment_counts.values,
                          labels={'x': '결제 방식', 'y': '구매 건수'},
                          title='선호 결제 방식별 구매 건수')
    st.plotly_chart(fig_payment, key='payment_chart')

def analyze_age_counts(data):
    st.subheader("연령대별 구매 건수 분석")
    data['Age Group'] = pd.cut(data['Age'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])
    age_counts = data['Age Group'].value_counts()
    fig_age = px.bar(x=age_counts.index, y=age_counts.values,
                         labels={'x': '연령대', 'y': '구매 건수'},
                         title='연령대별 구매 건수')
    st.plotly_chart(fig_age, key='age_chart')

def analyze_category_amounts(data):
    st.subheader("카테고리별 총 구매 금액 분석")
    category_amounts = data.groupby('Category')['Purchase Amount (USD)'].sum().sort_values(ascending=False)
    fig_category = px.bar(x=category_amounts.index, y=category_amounts.values,
                           labels={'x': '카테고리', 'y': '총 구매 금액 (USD)'},
                           title='카테고리별 총 구매 금액')
    st.plotly_chart(fig_category, key='category_chart')

def analyze_location_amounts(data):
    st.subheader("위치별 총 구매 금액 분석")
    location_amounts = data.groupby('Location')['Purchase Amount (USD)'].sum().sort_values(ascending=False)
    fig_location = px.bar(x=location_amounts.index, y=location_amounts.values,
                           labels={'x': '위치', 'y': '총 구매 금액 (USD)'},
                           title='위치별 총 구매 금액')
    st.plotly_chart(fig_location, key='location_chart')

def analyze_season_amounts(data):
    st.subheader("시즌별 총 구매 금액 분석")
    season_amounts = data.groupby('Season')['Purchase Amount (USD)'].sum().sort_values(ascending=False)
    fig_season = px.bar(x=season_amounts.index, y=season_amounts.values,
                           labels={'x': '시즌', 'y': '총 구매 금액 (USD)'},
                           title='시즌별 총 구매 금액')
    st.plotly_chart(fig_season, key='season_chart')

def analyze_item_amounts(data):
    st.subheader("상품별 총 구매 금액 분석 (상위 10개)")
    item_amounts = data.groupby('Item Purchased')['Purchase Amount (USD)'].sum().sort_values(ascending=False).head(10)
    fig_item = px.bar(x=item_amounts.index, y=item_amounts.values,
                           labels={'x': '상품', 'y': '총 구매 금액 (USD)'},
                           title='상품별 총 구매 금액 (상위 10개)')
    st.plotly_chart(fig_item, key='item_chart')

def analyze_season_category(data):
    st.subheader("계절별 카테고리 구매 패턴 분석")
    filtered_data = data[data['Season'].isin(['Spring', 'Summer', 'Fall', 'Winter']) & data['Category'].isin(['Clothing', 'Accessories', 'Footwear', 'Outerwear'])]
    season_category = pd.crosstab(filtered_data['Season'], filtered_data['Category'])
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_category = season_category.reindex(season_order)
    fig_season_category = px.bar(season_category, x=season_category.index, y=season_category.columns, labels={'value': '구매 횟수', 'index': '계절', 'columns': '카테고리'})
    fig_season_category.update_layout(barmode='stack', xaxis_title='계절', yaxis_title='구매 횟수')
    st.plotly_chart(fig_season_category, key='season_category_chart')

def analyze_age_avg(data):
    st.subheader("연령대별 평균 구매 금액 분석")
    data['Age Group'] = pd.cut(data['Age'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])
    age_avg = data.groupby('Age Group')['Purchase Amount (USD)'].mean().sort_index()
    fig_age = px.bar(x=age_avg.index, y=age_avg.values,
                         labels={'x': '연령대', 'y': '평균 구매 금액 (USD)'},
                         title='연령대별 평균 구매 금액')
    st.plotly_chart(fig_age, key='age_avg_chart')

def analyze_cluster_purchase(data):
    st.subheader("고객 유형별 평균 구매 금액 분석")
    if "고객유형" in data.columns:
        show_customer_types(data)
        avg_purchase = data.groupby('고객유형')['Purchase Amount (USD)'].mean().sort_index()
        x_labels = [f"{i} ({get_customer_type_name(i)})" for i in avg_purchase.index]
        fig = px.bar(x=x_labels, y=avg_purchase.values,
                     labels={'x': '고객 유형', 'y': '평균 구매 금액 (USD)'},
                     title='고객 유형별 평균 구매 금액')
        st.plotly_chart(fig, key='customer_type_purchase_chart')

def analyze_cluster_rating(data):
    st.subheader("고객 유형별 평균 리뷰 평점 분석")
    if "고객유형" in data.columns:
        avg_rating = data.groupby('고객유형')['Review Rating'].mean().sort_index()
        x_labels = [f"{i} ({get_customer_type_name(i)})" for i in avg_rating.index]
        fig = px.bar(x=x_labels, y=avg_rating.values,
                     labels={'x': '고객 유형', 'y': '평균 리뷰 평점'},
                     title='고객 유형별 평균 리뷰 평점')
        st.plotly_chart(fig, key='customer_type_rating_chart')

def analyze_cluster_sales(data):
    st.subheader("고객 유형별 총 매출액")
    if "고객유형" in data.columns:
        sales = data.groupby('고객유형')['Purchase Amount (USD)'].sum().sort_index()
        x_labels = [f"{i} ({get_customer_type_name(i)})" for i in sales.index]
        fig = px.bar(x=x_labels, y=sales.values,
                     labels={'x': '고객 유형', 'y': '총 구매 금액 (USD)'},
                     title='고객 유형별 총 매출액')
        st.plotly_chart(fig, key='customer_type_sales_chart')

def analyze_cluster_age_distribution(data):
    st.subheader("고객 유형별 연령 분포")
    if "고객유형" in data.columns:
        age_groups = [0, 20, 30, 40, 50, 60, 100]
        age_labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '60+']
        data['Age Group'] = pd.cut(data['Age'], bins=age_groups, labels=age_labels, right=False)
        type_age = data.groupby(['고객유형', 'Age Group']).size().unstack(fill_value=0)
        type_age.index = [f"{i} ({get_customer_type_name(i)})" for i in type_age.index]
        fig = px.bar(type_age, x=type_age.index, y=type_age.columns,
                     labels={'value': '고객 수', 'x': '고객 유형', 'columns': '연령대'},
                     title='고객 유형별 연령 분포')
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig, key='customer_type_age_chart')
