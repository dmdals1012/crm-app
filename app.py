import streamlit as st

from ui.eda import analyze_customers
from ui.home import home_page
from ui.ml import predict_new_customer

def main():

    st.sidebar.title("메뉴")


    menu = ['홈', '고객 관리', '고객 분석']
    choice = st.sidebar.selectbox('메뉴', menu)

    if choice == menu[0] :
        home_page()
    elif choice == menu[1] :
        analyze_customers()
    elif choice == menu[2] :
        predict_new_customer()

if __name__ == '__main__':
    main()
