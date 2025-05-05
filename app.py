import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("Streamlit Data Explorer")

st.markdown(
    "Upload a CSV file to explore your data. "
    "If no file is uploaded, a default Netflix dataset will be used."
)

uploaded_file = st.file_uploader("Upload CSV file", type="csv")

# Load data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    default_path = "data/netflix_titles.csv"
    if os.path.exists(default_path):
        df = pd.read_csv(default_path)
        st.info("Default dataset loaded.")
    else:
        st.error("No file uploaded and default file not found.")
        st.stop()

# Filters
st.subheader("Column Filters")
filtered_df = df.copy()

for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        min_val, max_val = int(df[col].min()), int(df[col].max())
        selected_range = st.slider(f"Range for '{col}'", min_val, max_val, (min_val, max_val), step=1)
        filtered_df = filtered_df[(df[col] >= selected_range[0]) & (df[col] <= selected_range[1])]
    elif df[col].dtype == "object" and df[col].nunique() <= 50:
        options = df[col].dropna().unique().tolist()
        selected = st.multiselect(f"Filter '{col}'", options=options)
        if selected:
            filtered_df = filtered_df[filtered_df[col].isin(selected)]

# Show filtered preview
st.subheader("Filtered Dataset Preview")
n_rows = st.slider("Number of rows to view", 5, min(100, len(filtered_df)), 10)
st.dataframe(filtered_df.head(n_rows))

# Visualization
st.subheader("Data Visualization")

numeric_cols = filtered_df.select_dtypes(include=["float64", "int64"]).columns.tolist()
categorical_cols = filtered_df.select_dtypes(include=["object", "category"]).columns.tolist()

plot_type = st.selectbox("Select plot type", ["Histogram", "Scatter", "Bar (value counts)"])

if plot_type == "Histogram" and numeric_cols:
    col = st.selectbox("Select numeric column", numeric_cols)
    fig = px.histogram(filtered_df, x=col)
    st.plotly_chart(fig)

elif plot_type == "Scatter" and len(numeric_cols) >= 2:
    x_axis = st.selectbox("X-axis", numeric_cols)
    y_axis = st.selectbox("Y-axis", numeric_cols, index=1)
    fig = px.scatter(filtered_df, x=x_axis, y=y_axis)
    st.plotly_chart(fig)

elif plot_type == "Bar (value counts)" and categorical_cols:
    col = st.selectbox("Select categorical column", categorical_cols)
    counts = filtered_df[col].value_counts().reset_index()
    counts.columns = [col, "count"]
    fig = px.bar(counts, x=col, y="count")
    st.plotly_chart(fig)

else:
    st.warning("Not enough data or columns to generate the selected plot.")
