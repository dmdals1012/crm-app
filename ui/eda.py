import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def analyze_customers():
    st.title("고객 데이터 분석")

    st.info('고객을 분류별로 분석합니다.')
    
    @st.cache_data
    def load_data():
        data = pd.read_csv('data/customer_data3.csv', index_col=0)
        data['Previous Purchases'] = pd.to_numeric(data['Previous Purchases'], errors='coerce')
        return data

    data = load_data()
    
    # 1. 연령대별 구매 금액 분포 상자 그림 (정렬된)
    st.subheader("연령대별 구매 금액 분포")
    data['Age Group'] = pd.cut(data['Age'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])
    age_order = ['0-20', '21-30', '31-40', '41-50', '51-60', '60+']
    fig = px.box(data, x='Age Group', y='Purchase Amount (USD)', color='Age Group', category_orders={'Age Group': age_order})
    fig.update_layout(xaxis_title='연령대', yaxis_title='구매 금액 (USD)')
    st.plotly_chart(fig)

    # 2. 클러스터별 평균 구매 금액과 리뷰 평점
    st.subheader("클러스터별 평균 구매 금액과 리뷰 평점")
    cluster_stats = data.groupby('Cluster')[['Purchase Amount (USD)', 'Review Rating']].mean().reset_index()
    fig = px.scatter(cluster_stats, x='Purchase Amount (USD)', y='Review Rating', color='Cluster', size='Purchase Amount (USD)',
                     hover_data=['Cluster'])
    fig.update_layout(xaxis_title='평균 구매 금액 (USD)', yaxis_title='평균 리뷰 평점')
    st.plotly_chart(fig)

    # 3. 카테고리별 평균 구매 금액 막대 그래프
    st.subheader("카테고리별 평균 구매 금액")
    category_avg = data.groupby('Category')['Purchase Amount (USD)'].mean().sort_values(ascending=False)
    fig = px.bar(category_avg, x=category_avg.index, y=category_avg.values)
    fig.update_layout(xaxis_title='카테고리', yaxis_title='평균 구매 금액 (USD)')
    st.plotly_chart(fig)

    # 4. 계절별 구매 패턴 막대 그래프
    st.subheader("계절별 구매 패턴")
    season_category = pd.crosstab(data['Season'], data['Category'])
    fig = go.Figure()
    for category in season_category.columns:
        fig.add_trace(go.Bar(x=season_category.index, y=season_category[category], name=category))
    fig.update_layout(barmode='stack', xaxis_title='계절', yaxis_title='구매 횟수')
    st.plotly_chart(fig)

if __name__ == "__main__":
    analyze_customers()
