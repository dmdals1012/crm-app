import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def analyze_customers():
    st.title("고객 데이터 분석")
    
    uploaded_file = st.file_uploader("고객 데이터 CSV 파일을 업로드하세요", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, index_col=0)
        st.write(data)
        
        # 기술 통계
        st.subheader("기술 통계")
        st.write(data.describe())
        
        # 범주형 데이터 빈도 분석
        st.subheader("범주형 데이터 빈도 분석")
        categorical_cols = data.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            st.write(f"{col}의 빈도:")
            st.write(data[col].value_counts())
            
        # 데이터 분포 시각화
        st.subheader("데이터 분포 시각화")
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
            sns.histplot(data[col], kde=True, ax=ax1)
            ax1.set_title(f'{col} 분포')
            sns.boxplot(x=data[col], ax=ax2)
            ax2.set_title(f'{col} 박스플롯')
            st.pyplot(fig)
        
        
        
        # 클러스터별 특성 분석
        if 'Cluster' in data.columns:
            st.subheader("클러스터별 특성 분석(평균)")
            cluster_means = data.groupby('Cluster')[numeric_cols].mean()
            st.write(cluster_means)
            
       
