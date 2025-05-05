import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Public Data Explorer")
st.markdown("Load a CSV file and explore interactively its data")

uploaded_file = st.file_uploader("Select CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Data preview")
    st.dataframe(df.head())

    st.subheader("Statistical summary")
    st.write(df.describe())

    st.subheader("Visualization")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if len(numeric_cols) >= 2:
        x_axis = st.selectbox("X var", numeric_cols)
        y_axis = st.selectbox("Y var", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
        fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
        st.plotly_chart(fig)
    else:
        st.info("At least two columns are needed to plot.")
