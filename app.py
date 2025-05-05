import streamlit as st
import pandas as pd
import os

st.title("Streamlit Data Explorer")

st.markdown(
    """
    You can upload a CSV file to explore your own data.  
    If you don't upload anything, the default Netflix dataset will be used instead.
    """
)

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully.")
else:
    default_path = "data/netflix_titles.csv"
    if os.path.exists(default_path):
        df = pd.read_csv(default_path)
        st.info("No file uploaded. Default dataset loaded.")
    else:
        st.error("'netflix_titles.csv' not found. Please upload a CSV file.")
        st.stop()

st.write("### Preview of the dataset:")
st.dataframe(df.head())
