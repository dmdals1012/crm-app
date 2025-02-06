import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def analyze_customers():
    st.title("고객 데이터 분석")
    
    uploaded_file = st.file_uploader("고객 데이터 CSV 파일을 업로드하세요", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        
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
        
        # 상관관계 분석
        st.subheader("상관관계 분석")
        corr = data[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
        
        # 산점도 매트릭스
        st.subheader("산점도 매트릭스")
        fig = px.scatter_matrix(data[numeric_cols])
        st.plotly_chart(fig)
        
        # 클러스터별 특성 분석
        if 'Cluster' in data.columns:
            st.subheader("클러스터별 특성 분석")
            cluster_means = data.groupby('Cluster')[numeric_cols].mean()
            st.write(cluster_means)
            
            # 클러스터별 특성 시각화
            for col in numeric_cols:
                fig = px.box(data, x='Cluster', y=col, title=f'클러스터별 {col} 분포')
                st.plotly_chart(fig)
        
        # 인터랙티브 요소
        st.subheader("인터랙티브 분석")
        x_axis = st.selectbox('X축 선택', options=numeric_cols)
        y_axis = st.selectbox('Y축 선택', options=numeric_cols)
        color_option = st.selectbox('색상 구분', options=['None'] + list(categorical_cols))
        
        if color_option == 'None':
            fig = px.scatter(data, x=x_axis, y=y_axis)
        else:
            fig = px.scatter(data, x=x_axis, y=y_axis, color=color_option)
        st.plotly_chart(fig)
        
        # 이상치 탐지
        st.subheader("이상치 탐지")
        for col in numeric_cols:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
            st.write(f"{col}의 이상치 개수: {len(outliers)}")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.boxplot(x=data[col], ax=ax)
            ax.set_title(f'{col} 이상치 박스플롯')
            st.pyplot(fig)
