# In modules/vizzu.py

import streamlit as st
from modules.src.vizzu_builder import App

def show_page():
    st.title("Vizzu Animation Page")
    # Your Vizzu animation logic or App initialization code goes here
    app = App()  # If App() contains the Streamlit app, you may need to call its specific methods

# If you want to run this module directly for testing
if __name__ == "__main__":
    show_page()  # Optional: run show_page() if this module is executed directly
