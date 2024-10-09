import pandas as pd
import streamlit as st
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_ollama import ChatOllama


# st.set_page_config(
#     page_title="DF Chat",
#     page_icon="💬",
#     layout="centered"
# )

def show_page():
    def read_data(file):
        if file.name.endswith(".csv"):
            return pd.read_csv(file,encoding='ISO-8859-1')
        else:
            return pd.read_excel(file)


    st.title("🤖 DataFrame ChatBot - Ollama")

    # initialize chat history in streamlit session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "df" not in st.session_state:
        st.session_state.df = None


    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

    if uploaded_file:
        st.session_state.df = read_data(uploaded_file)
        st.write("DataFrame Preview:")
        st.dataframe(st.session_state.df.head())


    # display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    user_prompt = st.chat_input("Ask LLM...")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append({"role":"user","content": user_prompt})

        llm = ChatOllama(model="qwen2.5:7b-instruct-q8_0", temperature=0, base_url="https://6743-34-125-128-90.ngrok-free.app/")

        pandas_df_agent = create_pandas_dataframe_agent(
            llm,
            st.session_state.df,
            verbose=True,
            agent_type="tool-calling",
            allow_dangerous_code=True,
            engine="pandas",
        )

        messages = [
            {"role":"system", "content": "You are a knowledgeable assistant specialized in analyzing and answering questions about CSV files and their data. Provide clear and concise responses based on the contents of the uploaded CSV file."},
            *st.session_state.chat_history
        ]

        response = pandas_df_agent.invoke(messages)

        assistant_response = response["output"]

        st.session_state.chat_history.append({"role":"assistant", "content": assistant_response})

        with st.chat_message("assistant"):
            st.markdown(assistant_response)
