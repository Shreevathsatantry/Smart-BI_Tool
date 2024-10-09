import streamlit as st
from modules import Clean, dashboard_self,Pygwalk,Overview1,Chat ,app

with st.sidebar:
    st.title("Navigation")
    page = st.selectbox("Choose a page", ["Home", "Data Cleaning (AutoClean)", "Dynamic Dashboard","Data Visualization","Data Analysis","Chat with Dataset","Knowledge graph"])

if page == "Home":
    st.title("Welcome to the Multi-Page Streamlit App")
    st.write("""
    This application allows you to perform various tasks like data cleaning, model interaction, and more.
    
    Use the sidebar to navigate to different sections of the app:
    - **Data Cleaning (AutoClean)**: Upload your dataset and clean it using AutoClean.
    - **Dynamic Dashboard**: View dynamic data visualizations.
    """)

elif page == "Data Cleaning (AutoClean)":
    Clean.show_page()  

elif page == "Dynamic Dashboard":
    dashboard_self.show_page()  

elif  page== "Data Visualization":
    Pygwalk.show_page()

elif  page== "Data Analysis":
    Overview1.show_page()

elif  page== "Chat with Dataset":
    Chat.show_page()

elif  page== "Knowledge graph":
    app.show_page()