import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    try:
        data = pd.read_csv('data/customer_data.csv', index_col=0, engine='python', on_bad_lines='skip', sep=',', quotechar='"', escapechar='\\')
        data['Previous Purchases'] = pd.to_numeric(data['Previous Purchases'], errors='coerce')
        # 'Cluster' → '고객유형' 컬럼명으로 변경
        if 'Cluster' in data.columns:
            data = data.rename(columns={'Cluster': '고객유형'})
        return data
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
        return None

# 고객유형 번호와 이름만 간단히 표시
customer_type_names = {
    0: "고액 소비 VIP 고객",
    1: "젊은 신규 고객",
    2: "중간 소비 젊은 고객",
    3: "중년층 충성 고객",
    4: "보수적인 중장년층 고객",
    5: "가격에 민감한 중년층 고객"
}

def show_customer_types():
    st.markdown("### 🏷️ 고객유형 분류")
    for k, v in customer_type_names.items():
        st.markdown(f"- 고객유형 {k} : {v}")
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
    st.markdown(f"- 남성 구매자의 비중이 약간 더 높은 것으로 보아, 남성 고객을 위한 마케팅 전략을 강화하는 것이 효과적일 수 있습니다. 🎯")

def analyze_payment_counts(data):
    st.subheader("선호 결제 방식별 구매 건수 분석")
    payment_counts = data['Preferred Payment Method'].value_counts()
    fig_payment = px.bar(x=payment_counts.index, y=payment_counts.values,
                          labels={'x': '결제 방식', 'y': '구매 건수'},
                          title='선호 결제 방식별 구매 건수')
    st.plotly_chart(fig_payment, key='payment_chart')
    most_preferred = payment_counts.index[0]
    count = payment_counts.values[0]
    percentage = (count / payment_counts.sum()) * 100
    st.markdown(f"- 가장 선호하는 결제 방식은 **{most_preferred}** 이며, 전체 결제의 **{percentage:.1f}%** 를 차지합니다. 💳")
    st.markdown(f"- {most_preferred} 결제 방식에 대한 프로모션을 강화하여 고객 만족도를 높이고, 추가적인 매출 증대를 기대할 수 있습니다. ✨")

def analyze_age_counts(data):
    st.subheader("연령대별 구매 건수 분석")
    data['Age Group'] = pd.cut(data['Age'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])
    age_counts = data['Age Group'].value_counts()
    fig_age = px.bar(x=age_counts.index, y=age_counts.values,
                         labels={'x': '연령대', 'y': '구매 건수'},
                         title='연령대별 구매 건수')
    st.plotly_chart(fig_age, key='age_chart')
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
    top_item = item_amounts.index[0]
    amount = item_amounts.values[0]
    percentage = (amount / item_amounts.sum()) * 100
    st.markdown(f"- 가장 높은 총 구매 금액을 기록한 상품은 **{top_item}**이며, 전체 매출의 **{percentage:.1f}%** 인 **{amount:,.2f} USD** 입니다. 👑")
    st.markdown(f"- {top_item} 상품의 재고를 충분히 확보하고, 관련 상품을 함께 추천하여 구매 만족도를 높일 수 있습니다. 🎁")

def analyze_season_category(data):
    st.subheader("계절별 카테고리 구매 패턴 분석")
    filtered_data = data[data['Season'].isin(['Spring', 'Summer', 'Fall', 'Winter']) & data['Category'].isin(['Clothing', 'Accessories', 'Footwear', 'Outerwear'])]
    season_category = pd.crosstab(filtered_data['Season'], filtered_data['Category'])
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_category = season_category.reindex(season_order)
    fig_season_category = px.bar(season_category, x=season_category.index, y=season_category.columns, labels={'value': '구매 횟수', 'index': '계절', 'columns': '카테고리'})
    fig_season_category.update_layout(barmode='stack', xaxis_title='계절', yaxis_title='구매 횟수')
    st.plotly_chart(fig_season_category, key='season_category_chart')
    for season in season_order:
        if season in season_category.index:
            top_category = season_category.loc[season].idxmax()
            top_count = season_category.loc[season, top_category]
            percentage = (top_count / season_category.loc[season].sum()) * 100 if season_category.loc[season].sum() > 0 else 0
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
    highest_avg_age = age_avg.idxmax()
    highest_avg_amount = age_avg.max()
    st.markdown(f"- 평균 구매 금액이 가장 높은 연령대는 **{highest_avg_age}**이며, 평균 구매 금액은 **{highest_avg_amount:,.2f} USD** 입니다. 💰")
    st.markdown(f"- {highest_avg_age} 연령대 고객의 구매 패턴을 분석하여, 비슷한 연령대의 고객층을 발굴하고 맞춤형 상품을 추천하는 전략을 수립할 수 있습니다. 🎁")

def analyze_customer_type_purchase(data):
    st.subheader("고객유형별 평균 구매 금액 분석")
    avg_purchase = data.groupby('고객유형')['Purchase Amount (USD)'].mean().sort_index()
    x_labels = [get_customer_type_name(i) for i in avg_purchase.index]
    fig = px.bar(x=x_labels, y=avg_purchase.values,
                 labels={'x': '고객유형', 'y': '평균 구매 금액 (USD)'},
                 title='고객유형별 평균 구매 금액')
    st.plotly_chart(fig, key='customer_type_purchase_chart')
    highest_idx = avg_purchase.idxmax()
    highest_name = get_customer_type_name(highest_idx)
    highest_amount = avg_purchase.max()
    st.markdown(f"- 평균 구매 금액이 가장 높은 고객유형은 **{highest_name}**이며, 평균 구매 금액은 **{highest_amount:,.2f} USD** 입니다. 👑")

def analyze_customer_type_rating(data):
    st.subheader("고객유형별 평균 리뷰 평점 분석")
    avg_rating = data.groupby('고객유형')['Review Rating'].mean().sort_index()
    x_labels = [get_customer_type_name(i) for i in avg_rating.index]
    fig = px.bar(x=x_labels, y=avg_rating.values,
                 labels={'x': '고객유형', 'y': '평균 리뷰 평점'},
                 title='고객유형별 평균 리뷰 평점')
    st.plotly_chart(fig, key='customer_type_rating_chart')
    highest_idx = avg_rating.idxmax()
    highest_name = get_customer_type_name(highest_idx)
    highest_rating = avg_rating.max()
    st.markdown(f"- 평균 리뷰 평점이 가장 높은 고객유형은 **{highest_name}**이며, 평균 평점은 **{highest_rating:.2f}** 입니다. 👍")

def analyze_customer_type_sales(data):
    st.subheader("고객유형별 총 매출액")
    sales = data.groupby('고객유형')['Purchase Amount (USD)'].sum().sort_index()
    x_labels = [get_customer_type_name(i) for i in sales.index]
    fig = px.bar(x=x_labels, y=sales.values,
                 labels={'x': '고객유형', 'y': '총 구매 금액 (USD)'},
                 title='고객유형별 총 매출액')
    st.plotly_chart(fig, key='customer_type_sales_chart')
    highest_idx = sales.idxmax()
    highest_name = get_customer_type_name(highest_idx)
    highest_amount = sales.max()
    st.markdown(f"- 가장 높은 총 매출액을 기록한 고객유형은 **{highest_name}**이며, 총 매출액은 **{highest_amount:,.0f} USD** 입니다. 💰")

def analyze_customer_type_age_distribution(data):
    st.subheader("고객유형별 연령 분포")
    age_groups = [0, 20, 30, 40, 50, 60, 100]
    age_labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '60+']
    data['Age Group'] = pd.cut(data['Age'], bins=age_groups, labels=age_labels, right=False)
    type_age = data.groupby(['고객유형', 'Age Group']).size().unstack(fill_value=0)
    x_labels = [get_customer_type_name(i) for i in type_age.index]
    fig = px.bar(type_age, x=x_labels, y=type_age.columns,
                 labels={'value': '고객 수', 'x': '고객유형', 'columns': '연령대'},
                 title='고객유형별 연령 분포')
    fig.update_layout(barmode='stack')
    st.plotly_chart(fig, key='customer_type_age_chart')
    for idx in type_age.index:
        top_age_group = type_age.loc[idx].idxmax()
        top_age_count = type_age.loc[idx, top_age_group]
        percentage = (top_age_count / type_age.loc[idx].sum()) * 100
        st.markdown(f"- **{get_customer_type_name(idx)}**: 가장 많은 연령대는 **{top_age_group}**이며, 해당 유형의 **{percentage:.1f}%**를 차지합니다.")

def customer_analysis(data):
    st.header("고객 관련 데이터 분석")
    st.write("고객 관련 데이터를 분석하여 인사이트를 도출합니다.")
    analyze_gender_counts(data)
    analyze_payment_counts(data)
    analyze_age_counts(data)

def sales_analysis(data):
    st.header("매출 관련 데이터 분석")
    st.write("매출 관련 데이터를 분석하여 인사이트를 도출합니다.")
    analyze_category_amounts(data)
    analyze_location_amounts(data)
    analyze_season_amounts(data)
    analyze_item_amounts(data)
    analyze_season_category(data)

def analyze_customers(data):
    st.title("고객 데이터 분석")
    show_customer_types()
    st.info('고객유형별로 분석합니다.')
    st.markdown("---")
    customer_analysis(data)
    analyze_age_avg(data)
    analyze_customer_type_purchase(data)
    analyze_customer_type_rating(data)
    analyze_customer_type_sales(data)
    analyze_customer_type_age_distribution(data)
