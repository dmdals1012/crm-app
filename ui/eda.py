import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def analyze_customers():
    st.title("고객 데이터 분석")

    st.info('고객을 분류별로 분석합니다.')
    
    @st.cache_data
    def load_data():
        data = pd.read_csv('data/customer_data3.csv', index_col=0)
        data['Previous Purchases'] = pd.to_numeric(data['Previous Purchases'], errors='coerce')
        return data

    data = load_data()
    st.write(data)
    
    # 기술 통계
    st.subheader("기술 통계")
    st.write(data.describe())
    
    # 클러스터별 과거 구매 기록 평균 분석
    st.subheader("클러스터별 과거 구매 기록 평균")
    if 'Cluster' in data.columns and 'Previous Purchases' in data.columns:
        cluster_purchase_means = data.groupby('Cluster')['Previous Purchases'].mean().sort_values(ascending=False)
        fig = px.bar(cluster_purchase_means, 
                     x=cluster_purchase_means.index, 
                     y=cluster_purchase_means.values,
                     labels={'x': '클러스터', 'y': '평균 구매 횟수'},
                     title='클러스터별 평균 과거 구매 횟수')
        fig.update_layout(xaxis_title='클러스터', yaxis_title='평균 구매 횟수')
        st.plotly_chart(fig)
        
        st.write("클러스터별 평균 과거 구매 횟수:")
        st.write(cluster_purchase_means)
    else:
        st.warning("'Cluster' 또는 'Previous Purchases' 열이 데이터에 없습니다.")
        
    # 데이터 분포 시각화
    st.subheader("데이터 분포 시각화")
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        sns.histplot(data[col], kde=True, ax=ax1)
        ax1.set_title(f'{col} 분포')
        ax1.set_xlabel('값')
        ax1.set_ylabel('빈도')
        sns.boxplot(x=data[col], ax=ax2)
        ax2.set_title(f'{col} 박스플롯')
        ax2.set_xlabel('값')
        st.pyplot(fig)
    
    # 클러스터별 특성 분석
    if 'Cluster' in data.columns:
        st.subheader("클러스터별 특성 분석(평균)")
        cluster_means = data.groupby('Cluster')[numeric_cols].mean()
        
        # 히트맵으로 클러스터별 특성 시각화
        fig = px.imshow(cluster_means.T, 
                        labels=dict(x="클러스터", y="특성", color="평균값"),
                        title="클러스터별 특성 평균")
        st.plotly_chart(fig)
        
        st.write("클러스터별 특성 평균값:")
        st.write(cluster_means)

