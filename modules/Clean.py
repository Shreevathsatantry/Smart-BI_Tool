import streamlit as st
import pandas as pd
from AutoClean import AutoClean  # Ensure you have AutoClean installed

def show_page():
    st.title("Data Cleaning Tool")  # No need to set page config here again

    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

    if uploaded_file:
        original_data = pd.read_csv(uploaded_file,encoding='ISO-8859-1')
        st.write("Filename:", uploaded_file.name)
        st.write("Original Data Preview:", original_data.head())

        # Define the options for different cleaning tasks
        # Rest of the code stays the same...

        # Define the options for different cleaning tasks
        mode = {
            "Choose option": "None",
            "Automated processing": "auto",
            "Manual processing": "manual"
        }

        duplicates = {
            "False": False,
            "Auto": "auto",
            "True": True
        }

        missing_num = {
            "False": False,
            "Auto": "auto",
            "linear regression": "linreg",
            "K-Nearest Neighbors": "knn",
            "Mean": "mean",
            "Median": "median",
            "Mode": "most_frequent",
            "Delete": "delete"
        }

        missing_categ = {
            "False": False,
            "Auto": "auto",
            "Logistic Regression": "logreg",
            "K-Nearest Neighbors": "knn",
            "Mode": "most_frequent",
            "Delete": "delete"
        }

        encode_categ = {
            "False": False,
            "Auto": "auto",
            "One Hot Encoding": ["onehot"],
            "Label Encoding": ["label"]
        }

        extract_datetime = {
            "False": False,
            "Auto": "auto",
            "Day": "D",
            "Month": "M",
            "Year": "Y",
            "Hour": "h",
            "Minute": "m",
            "Second": "s"
        }

        outliers = {
            "False": False,
            "Auto": "auto",
            "Winsorize": "winz",
            "Delete": "delete"
        }

        outlier_param = {
            "Default (1.5)": 1.5,
            "Custom value": "custom"
        }

        logfile = {
            "True": True,
            "False": False
        }

        verbose = {
            "False": False,
            "True": True
        }

        initial_option = st.sidebar.selectbox('Choose mode for AutoClean:', list(mode.keys()))
        selected_mode = mode[initial_option]

        if initial_option == "Manual processing":
            st.sidebar.header("Manual Processing Options")

            dup_option = st.sidebar.selectbox('Handle duplicates:', list(duplicates.keys()))
            selected_duplicates = duplicates[dup_option]

            missing_num_option = st.sidebar.selectbox('Handle missing numerical values:', list(missing_num.keys()))
            selected_missing_num = missing_num[missing_num_option]

            missing_categ_option = st.sidebar.selectbox('Handle missing categorical values:', list(missing_categ.keys()))
            selected_missing_categ = missing_categ[missing_categ_option]

            encode_option = st.sidebar.selectbox('Encoding categorical values:', list(encode_categ.keys()))
            selected_encode_categ = encode_categ[encode_option]

            datetime_option = st.sidebar.selectbox('Extract datetime parts:', list(extract_datetime.keys()))
            selected_extract_datetime = extract_datetime[datetime_option]

            outliers_option = st.sidebar.selectbox('Handle outliers:', list(outliers.keys()))
            selected_outliers = outliers[outliers_option]

            outlier_param_option = st.sidebar.selectbox('Outlier threshold (1.5 by default):', list(outlier_param.keys()))
            if outlier_param_option == "Custom value":
                custom_outlier_value = st.sidebar.number_input("Enter custom outlier threshold", min_value=0.0, step=0.1)
                selected_outlier_param = custom_outlier_value
            else:
                selected_outlier_param = outlier_param[outlier_param_option]

            logfile_option = st.sidebar.selectbox('Generate logfile?', list(logfile.keys()))
            selected_logfile = logfile[logfile_option]

            verbose_option = st.sidebar.selectbox('Verbose mode?', list(verbose.keys()))
            selected_verbose = verbose[verbose_option]

            if st.button('Run AutoClean 🚀'):
                with st.spinner('Cleaning data...'):
                    cleaner = AutoClean(
                        original_data,
                        mode=selected_mode,
                        duplicates=selected_duplicates,
                        missing_num=selected_missing_num,
                        missing_categ=selected_missing_categ,
                        encode_categ=selected_encode_categ,
                        extract_datetime=selected_extract_datetime,
                        outliers=selected_outliers,
                        outlier_param=selected_outlier_param,
                        logfile=selected_logfile,
                        verbose=selected_verbose
                    )
                    cleaned_data = cleaner.output
                    st.success("Data cleaning completed!")

                    st.subheader("Original Data")
                    st.write(original_data.head())
                    st.subheader("Cleaned Data")
                    st.write(cleaned_data.head())

                    st.subheader("Statistics for Original Data")
                    st.write(original_data.describe(include='all'))

                    st.subheader("Statistics for Cleaned Data")
                    st.write(cleaned_data.describe(include='all'))

                    st.download_button('Download Cleaned Data', cleaned_data.to_csv(index=False), file_name='cleaned_data.csv')

        elif initial_option == "Automated processing":
            if st.button('Run AutoClean 🚀'):
                with st.spinner('Cleaning data...'):
                    cleaner = AutoClean(
                        original_data,
                        mode='auto'
                    )
                    cleaned_data = cleaner.output
                    st.success("Data cleaning completed!")

                    st.subheader("Original Data")
                    st.write(original_data.head())
                    st.subheader("Cleaned Data")
                    st.write(cleaned_data.head())

                    st.subheader("Statistics for Original Data")
                    st.write(original_data.describe(include='all'))

                    st.subheader("Statistics for Cleaned Data")
                    st.write(cleaned_data.describe(include='all'))

                    st.download_button('Download Cleaned Data', cleaned_data.to_csv(index=False), file_name='cleaned_data.csv')
