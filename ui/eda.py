import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
        data = pd.read_csv('data/customer_data3.csv', index_col=0)
        data['Previous Purchases'] = pd.to_numeric(data['Previous Purchases'], errors='coerce')
        return data

def analyze_customers():
    st.title("고객 데이터 분석")

    st.info('고객을 분류별로 분석합니다.')
    
    data = load_data()
    
    st.markdown("---")  # 마크다운 선 추가
    
    # 1. 연령대별 구매 금액 분포 상자 그림 (정렬된)
    st.subheader("연령대별 구매 금액 분포")
    st.write("이 차트는 각 연령대별 구매 금액의 분포를 보여줍니다. 상자 그림을 통해 중앙값, 사분위수, 이상치 등을 한눈에 파악할 수 있습니다.")
    data['Age Group'] = pd.cut(data['Age'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])
    age_order = ['0-20', '21-30', '31-40', '41-50', '51-60', '60+']
    fig = px.box(data, x='Age Group', y='Purchase Amount (USD)', color='Age Group', category_orders={'Age Group': age_order})
    fig.update_layout(xaxis_title='연령대', yaxis_title='구매 금액 (USD)')
    st.plotly_chart(fig)

    st.markdown("---")  # 마크다운 선 추가

    # 2. 클러스터별 평균 구매 금액과 리뷰 평점
    st.subheader("클러스터별 평균 구매 금액과 리뷰 평점")
    st.write("이 산점도는 각 고객 클러스터의 평균 구매 금액과 리뷰 평점을 보여줍니다. 점의 크기는 평균 구매 금액을 나타냅니다. 이를 통해 클러스터별 특성을 파악할 수 있습니다.")
    cluster_stats = data.groupby('Cluster')[['Purchase Amount (USD)', 'Review Rating']].mean().reset_index()
    fig = px.scatter(cluster_stats, x='Purchase Amount (USD)', y='Review Rating', color='Cluster', size='Purchase Amount (USD)',
                     hover_data=['Cluster'])
    fig.update_layout(xaxis_title='평균 구매 금액 (USD)', yaxis_title='평균 리뷰 평점')
    st.plotly_chart(fig)

    st.markdown("---")  # 마크다운 선 추가

    valid_categories = ['Clothing', 'Accessories', 'Footwear', 'Outerwear']
    valid_seasons = ['Spring', 'Summer', 'Fall', 'Winter']

    # 3. 카테고리별 평균 구매 금액 막대 그래프
    st.subheader("카테고리별 평균 구매 금액")
    st.write("이 막대 그래프는 각 제품 카테고리별 평균 구매 금액을 보여줍니다. 이를 통해 어떤 카테고리의 제품이 가장 높은 매출을 올리는지 파악할 수 있습니다.")
    category_avg = data[data['Category'].isin(valid_categories)].groupby('Category')['Purchase Amount (USD)'].mean().sort_values(ascending=False)
    fig = px.bar(category_avg, x=category_avg.index, y=category_avg.values)
    fig.update_layout(xaxis_title='카테고리', yaxis_title='평균 구매 금액 (USD)')
    st.plotly_chart(fig)

    st.markdown("---")  # 마크다운 선 추가

    # 4. 계절별 구매 패턴 막대 그래프
    st.subheader("계절별 구매 패턴")
    st.write("이 누적 막대 그래프는 각 계절별로 카테고리 구매 패턴을 보여줍니다. 각 색상은 다른 제품 카테고리를 나타내며, 이를 통해 계절에 따른 제품 선호도 변화를 파악할 수 있습니다.")
    filtered_data = data[data['Season'].isin(valid_seasons) & data['Category'].isin(valid_categories)]
    season_category = pd.crosstab(filtered_data['Season'], filtered_data['Category'])
    fig = go.Figure()
    for category in valid_categories:
        if category in season_category.columns:
            fig.add_trace(go.Bar(x=valid_seasons, y=[season_category.loc[season, category] if season in season_category.index else 0 for season in valid_seasons], name=category))
    fig.update_layout(barmode='stack', xaxis_title='계절', yaxis_title='구매 횟수')
    st.plotly_chart(fig)
