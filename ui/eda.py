import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

@st.cache_data
def load_data():
    try:
        data = pd.read_csv('data/customer_data.csv', index_col=0, engine='python', on_bad_lines='skip', sep=',', quotechar='"', escapechar='\\')
        data['Previous Purchases'] = pd.to_numeric(data['Previous Purchases'], errors='coerce')
        return data
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
        return None

def analyze_gender_counts(data):
    st.subheader("성별별 구매 건수 분석")
    gender_counts = data['Gender'].value_counts()
    fig_gender = px.bar(x=gender_counts.index, y=gender_counts.values,
                         labels={'x': '성별', 'y': '구매 건수'},
                         title='성별별 구매 건수')
    st.plotly_chart(fig_gender, key='gender_chart')
    
    # 분석 결과 설명 추가 (개선)
    total_purchases = gender_counts.sum()
    male_percentage = (gender_counts['Male'] / total_purchases) * 100
    female_percentage = (gender_counts['Female'] / total_purchases) * 100
    
    st.markdown(f"- 남성 구매자는 전체 구매의 **{male_percentage:.1f}%** 를 차지하며, 여성 구매자는 **{female_percentage:.1f}%** 를 차지합니다. 📊")
    st.markdown(f"- 남성 구매자의 비중이 약간 더 높은 것으로 보아, 남성 고객을 위한 마케팅 전략을 강화하는 것이 효과적일 수 있습니다. 🎯")


def analyze_payment_counts(data):
    st.subheader("선호 결제 방식별 구매 건수 분석")
    payment_counts = data['Preferred Payment Method'].value_counts()
    fig_payment = px.bar(x=payment_counts.index, y=payment_counts.values,
                          labels={'x': '결제 방식', 'y': '구매 건수'},
                          title='선호 결제 방식별 구매 건수')
    st.plotly_chart(fig_payment, key='payment_chart')
    
    # 분석 결과 설명 추가 (개선)
    most_preferred = payment_counts.index[0]
    count = payment_counts.values[0]
    percentage = (count / payment_counts.sum()) * 100
    
    st.markdown(f"- 가장 선호하는 결제 방식은 **{most_preferred}** 이며, 전체 결제의 **{percentage:.1f}%** 를 차지합니다. 💳")
    st.markdown(f"- {most_preferred} 결제 방식에 대한 프로모션을 강화하여 고객 만족도를 높이고, 추가적인 매출 증대를 기대할 수 있습니다. ✨")

def analyze_age_counts(data):
    st.subheader("연령대별 구매 건수 분석")
    data['Age Group'] = pd.cut(data['Age'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])
    age_counts = data['Age Group'].value_counts()  # sort_index() 제거
    fig_age = px.bar(x=age_counts.index, y=age_counts.values,
                         labels={'x': '연령대', 'y': '구매 건수'},
                         title='연령대별 구매 건수')
    st.plotly_chart(fig_age, key='age_chart')
    
    # 분석 결과 설명 추가 (개선)
    most_active_age = age_counts.index[0]
    count = age_counts.values[0]
    percentage = (count / age_counts.sum()) * 100

    st.markdown(f"- 가장 활발한 구매를 보이는 연령대는 **{most_active_age}**이며, 전체 구매의 **{percentage:.1f}%** 를 차지합니다. 🎉")
    st.markdown(f"- **{most_active_age}** 연령대에 맞는 상품 및 프로모션을 집중적으로 제공하여 구매 전환율을 높일 수 있습니다. 🎁")


def analyze_category_amounts(data):
    st.subheader("카테고리별 총 구매 금액 분석")
    category_amounts = data.groupby('Category')['Purchase Amount (USD)'].sum().sort_values(ascending=False)
    fig_category = px.bar(x=category_amounts.index, y=category_amounts.values,
                           labels={'x': '카테고리', 'y': '총 구매 금액 (USD)'},
                           title='카테고리별 총 구매 금액')
    st.plotly_chart(fig_category, key='category_chart')
    
    # 분석 결과 설명 추가 (개선)
    top_category = category_amounts.index[0]
    amount = category_amounts.values[0]
    percentage = (amount / category_amounts.sum()) * 100

    st.markdown(f"- 가장 높은 총 구매 금액을 기록한 카테고리는 **{top_category}**이며, 전체 매출의 **{percentage:.1f}%** 인 **{amount:,.2f} USD** 를 차지합니다. 💰")
    st.markdown(f"- {top_category} 카테고리에 대한 상품 구색을 강화하고, 관련 상품을 추천하는 전략을 통해 추가 매출을 확보할 수 있습니다. 🛍️")


def analyze_location_amounts(data):
    st.subheader("위치별 총 구매 금액 분석")
    location_amounts = data.groupby('Location')['Purchase Amount (USD)'].sum().sort_values(ascending=False)
    fig_location = px.bar(x=location_amounts.index, y=location_amounts.values,
                           labels={'x': '위치', 'y': '총 구매 금액 (USD)'},
                           title='위치별 총 구매 금액')
    st.plotly_chart(fig_location, key='location_chart')
    
     # 분석 결과 설명 추가 (개선)
    top_location = location_amounts.index[0]
    amount = location_amounts.values[0]
    percentage = (amount / location_amounts.sum()) * 100

    st.markdown(f"- 가장 높은 총 구매 금액을 기록한 위치는 **{top_location}**이며, 전체 매출의 **{percentage:.1f}%** 인 **{amount:,.2f} USD** 입니다. 🌍")
    st.markdown(f"- {top_location} 지역 고객을 대상으로 한 맞춤형 프로모션을 통해 충성도를 높이고, 신규 고객 유치를 위한 전략을 수립할 수 있습니다. 🚩")

def analyze_season_amounts(data):
    st.subheader("시즌별 총 구매 금액 분석")
    season_amounts = data.groupby('Season')['Purchase Amount (USD)'].sum().sort_values(ascending=False)
    fig_season = px.bar(x=season_amounts.index, y=season_amounts.values,
                           labels={'x': '시즌', 'y': '총 구매 금액 (USD)'},
                           title='시즌별 총 구매 금액')
    st.plotly_chart(fig_season, key='season_chart')
    
    # 분석 결과 설명 추가 (개선)
    top_season = season_amounts.index[0]
    amount = season_amounts.values[0]
    percentage = (amount / season_amounts.sum()) * 100
    
    st.markdown(f"- 가장 높은 총 구매 금액을 기록한 시즌은 **{top_season}**이며, 전체 매출의 **{percentage:.1f}%** 인 **{amount:,.2f} USD** 입니다. ☀️")
    st.markdown(f"- {top_season} 시즌에 맞는 상품 라인업을 강화하고, 특별 할인 이벤트를 진행하여 매출을 극대화할 수 있습니다. 🌸")

def analyze_item_amounts(data):
    st.subheader("상품별 총 구매 금액 분석 (상위 10개)")
    item_amounts = data.groupby('Item Purchased')['Purchase Amount (USD)'].sum().sort_values(ascending=False).head(10)
    fig_item = px.bar(x=item_amounts.index, y=item_amounts.values,
                           labels={'x': '상품', 'y': '총 구매 금액 (USD)'},
                           title='상품별 총 구매 금액 (상위 10개)')
    st.plotly_chart(fig_item, key='item_chart')
    
    # 분석 결과 설명 추가 (개선)
    top_item = item_amounts.index[0]
    amount = item_amounts.values[0]
    percentage = (amount / item_amounts.sum()) * 100

    st.markdown(f"- 가장 높은 총 구매 금액을 기록한 상품은 **{top_item}**이며, 전체 매출의 **{percentage:.1f}%** 인 **{amount:,.2f} USD** 입니다. 👑")
    st.markdown(f"- {top_item} 상품의 재고를 충분히 확보하고, 관련 상품을 함께 추천하여 구매 만족도를 높일 수 있습니다. 🎁")


def analyze_season_category(data):
    st.subheader("계절별 카테고리 구매 패턴 분석")
    filtered_data = data[data['Season'].isin(['Spring', 'Summer', 'Fall', 'Winter']) & data['Category'].isin(['Clothing', 'Accessories', 'Footwear', 'Outerwear'])]
    season_category = pd.crosstab(filtered_data['Season'], filtered_data['Category'])
    
    # 계절 순서 변경
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_category = season_category.reindex(season_order)
    
    fig_season_category = px.bar(season_category, x=season_category.index, y=season_category.columns, labels={'value': '구매 횟수', 'index': '계절', 'columns': '카테고리'})
    fig_season_category.update_layout(barmode='stack', xaxis_title='계절', yaxis_title='구매 횟수')
    st.plotly_chart(fig_season_category, key='season_category_chart')
    
    # 분석 결과 설명 추가 (개선)
    for season in season_order:
        if season in season_category.index:
            top_category = season_category.loc[season].idxmax()
            top_count = season_category.loc[season, top_category]
            percentage = (top_count / season_category.loc[season].sum()) * 100
            st.markdown(f"- **{season}**: 가장 인기 있는 카테고리는 **{top_category}**이며, 해당 계절 구매의 **{percentage:.1f}%** 를 차지하는 **{top_count:,}**건의 구매가 있었습니다. 🌸")
        else:
            st.markdown(f"- **{season}**: 해당 계절에 대한 데이터가 없습니다.")


def analyze_age_avg(data):
    st.subheader("연령대별 평균 구매 금액 분석")
    data['Age Group'] = pd.cut(data['Age'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])
    age_avg = data.groupby('Age Group')['Purchase Amount (USD)'].mean().sort_index()
    fig_age = px.bar(x=age_avg.index, y=age_avg.values,
                         labels={'x': '연령대', 'y': '평균 구매 금액 (USD)'},
                         title='연령대별 평균 구매 금액')
    st.plotly_chart(fig_age, key='age_avg_chart')
    
    # 분석 결과 설명 추가 (개선)
    highest_avg_age = age_avg.idxmax()
    highest_avg_amount = age_avg.max()

    st.markdown(f"- 평균 구매 금액이 가장 높은 연령대는 **{highest_avg_age}**이며, 평균 구매 금액은 **{highest_avg_amount:,.2f} USD** 입니다. 💰")
    st.markdown(f"- {highest_avg_age} 연령대 고객의 구매 패턴을 분석하여, 유사한 특성을 가진 고객층을 발굴하고 맞춤형 상품을 추천하는 전략을 수립할 수 있습니다. 🎁")

def analyze_cluster_purchase(data):
    st.subheader("클러스터별 평균 구매 금액 분석")
    cluster_avg_purchase = data.groupby('Cluster')['Purchase Amount (USD)'].mean().sort_index()
    fig_cluster_purchase = px.bar(x=cluster_avg_purchase.index, y=cluster_avg_purchase.values,
                         labels={'x': '클러스터', 'y': '평균 구매 금액 (USD)'},
                         title='클러스터별 평균 구매 금액')
    st.plotly_chart(fig_cluster_purchase, key='cluster_purchase_chart')
    
    # 분석 결과 설명 추가 (개선)
    highest_avg_cluster = cluster_avg_purchase.idxmax()
    highest_avg_amount = cluster_avg_purchase.max()

    st.markdown(f"- 평균 구매 금액이 가장 높은 클러스터는 **{highest_avg_cluster}**이며, 평균 구매 금액은 **{highest_avg_amount:,.2f} USD** 입니다. 👑")
    st.markdown(f"- {highest_avg_cluster} 클러스터 고객의 특성을 파악하여, 해당 클러스터와 유사한 고객을 대상으로 하는 마케팅 캠페인을 진행하여 효율을 높일 수 있습니다. 🚀")

def analyze_cluster_rating(data):
    st.subheader("클러스터별 평균 리뷰 평점 분석")
    cluster_avg_rating = data.groupby('Cluster')['Review Rating'].mean().sort_index()
    fig_cluster_rating = px.bar(x=cluster_avg_rating.index, y=cluster_avg_rating.values,
                         labels={'x': '클러스터', 'y': '평균 리뷰 평점'},
                         title='클러스터별 평균 리뷰 평점')
    st.plotly_chart(fig_cluster_rating, key='cluster_rating_chart')
    
     # 분석 결과 설명 추가 (개선)
    highest_avg_cluster = cluster_avg_rating.idxmax()
    highest_avg_rating = cluster_avg_rating.max()

    st.markdown(f"- 평균 리뷰 평점이 가장 높은 클러스터는 **{highest_avg_cluster}**이며, 평균 평점은 **{highest_avg_rating:.2f}** 입니다. 👍")
    st.markdown(f"- {highest_avg_cluster} 클러스터 고객에게 긍정적인 경험을 제공하는 요인을 분석하고, 다른 클러스터에도 적용하여 전체적인 고객 만족도를 향상시킬 수 있습니다. ✨")

def analyze_cluster_sales(data):
    st.subheader("클러스터별 총 매출액")
    try:
        cluster_sales = data.groupby('Cluster')['Purchase Amount (USD)'].sum().sort_index()
        if not cluster_sales.empty:
            fig_cluster_sales = px.bar(x=cluster_sales.index, y=cluster_sales.values,
                                labels={'x': '클러스터', 'y': '총 구매 금액 (USD)'},
                                title='클러스터별 총 매출액')
            st.plotly_chart(fig_cluster_sales, key='cluster_sales_chart')
            
            # 분석 결과 설명 추가 (개선)
            highest_sales_cluster = cluster_sales.idxmax()
            highest_sales_amount = cluster_sales.max()

            st.markdown(f"- 가장 높은 총 매출액을 기록한 클러스터는 **{highest_sales_cluster}**이며, 총 매출액은 **{highest_sales_amount:,.0f} USD** 입니다. 💰")
            st.markdown(f"- {highest_sales_cluster} 클러스터 고객에게 인기 있는 상품이나 프로모션을 분석하여, 다른 클러스터에도 적용하는 것을 고려해볼 수 있습니다. 🚀")
        else:
            st.warning("클러스터별 매출 데이터가 없습니다.")
    except KeyError:
        st.error("DataFrame에 'Cluster' 또는 'Purchase Amount (USD)' 컬럼이 없습니다.")

def analyze_cluster_age_distribution(data):
    st.subheader("클러스터별 연령 분포")
    try:
        age_groups = [0, 20, 30, 40, 50, 60, 100]
        age_labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '60+']
        data['Age Group'] = pd.cut(data['Age'], bins=age_groups, labels=age_labels, right=False)
        cluster_age = data.groupby(['Cluster', 'Age Group']).size().unstack(fill_value=0)
        
        fig_cluster_age = px.bar(cluster_age, x=cluster_age.index, y=cluster_age.columns,
                                labels={'value': '고객 수', 'index': '클러스터', 'columns': '연령대'},
                                title='클러스터별 연령 분포')
        fig_cluster_age.update_layout(barmode='stack')
        st.plotly_chart(fig_cluster_age, key='cluster_age_chart')

         # 분석 결과 설명 추가 (개선)
        for cluster in cluster_age.index:
            top_age_group = cluster_age.loc[cluster].idxmax()
            top_age_count = cluster_age.loc[cluster, top_age_group]
            percentage = (top_age_count / cluster_age.loc[cluster].sum()) * 100

            st.markdown(f"- 클러스터 **{cluster}**: 가장 많은 연령대는 **{top_age_group}**이며, 해당 클러스터의 **{percentage:.1f}%** 를 차지하는 **{top_age_count:,}**명 입니다. 👶")
    except KeyError:
        st.error("DataFrame에 'Cluster' 또는 'Age' 컬럼이 없습니다.")
    except Exception as e:
        st.error(f"오류 발생: {e}")

def customer_analysis(data):
    st.header("고객 관련 데이터 분석")
    st.write("고객 관련 데이터를 분석하여 인사이트를 도출합니다.")
    
    analyze_gender_counts(data) # 성별별 구매 건수 분석
    analyze_payment_counts(data) # 선호 결제 방식별 구매 건수 분석
    analyze_age_counts(data) # 연령대별 구매 건수 분석

def sales_analysis(data):
    st.header("매출 관련 데이터 분석")
    st.write("매출 관련 데이터를 분석하여 인사이트를 도출합니다.")
    
    analyze_category_amounts(data) # 카테고리별 총 구매 금액 분석
    analyze_location_amounts(data) # 위치별 총 구매 금액 분석
    analyze_season_amounts(data) # 시즌별 총 구매 금액 분석
    analyze_item_amounts(data) # 상품별 총 구매 금액 분석
    analyze_season_category(data) # 계절별 카테고리 구매 패턴 분석

def analyze_customers(data):
    st.title("고객 데이터 분석")

    st.info('고객을 분류별로 분석합니다.')

    st.markdown("---")  # 마크다운 선 추가
    
    customer_analysis(data) # 고객 관련 분석
    
    # 1. 연령대별 구매 금액 분포 막대 그래프
    analyze_age_avg(data) # 연령대별 평균 구매 금액 분석

    # 클러스터별 평균 구매 금액 막대 그래프
    analyze_cluster_purchase(data) # 클러스터별 평균 구매 금액 분석

    # 클러스터별 평균 리뷰 평점 막대 그래프
    analyze_cluster_rating(data) # 클러스터별 평균 리뷰 평점 분석

    analyze_cluster_sales(data)
    
    analyze_cluster_age_distribution(data)

def main():
    st.title("👔 의류 온라인 쇼핑몰 CRM 📊")

    # 데이터 로드
    data = load_data()

    if data is not None:
        # 고객 데이터 분석 실행
        analyze_customers(data)
    else:
        st.error("데이터를 불러오는 데 실패했습니다.")

if __name__ == "__main__":
    main()
