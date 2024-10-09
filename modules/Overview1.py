import pandas as pd
import sweetviz as sv
import streamlit as st


def show_page():
    def read_data(file):
        if file.name.endswith(".csv"):
            return pd.read_csv(file,encoding='ISO-8859-1')
        else:
            return pd.read_excel(file,encoding='ISO-8859-1')

    st.title("🤖 DataFrame Overview")

    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        df = read_data(uploaded_file)

        with st.expander("CSV preview:"):
            st.write(df)

        report = sv.analyze(df)
        report.show_html("report.html")
        st.components.v1.html(open("report.html").read(), height=600, width=800)
    else:
        st.info("Please upload a CSV or Excel file to view the DataFrame.")
