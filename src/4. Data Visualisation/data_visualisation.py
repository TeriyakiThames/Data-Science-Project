import ast

import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_data
# The main dataset is obtained from combining the Scorpus dataset and web scraping dataset
# After combining both datasets, we then remove duplicated titles.
def load_dataset(file_path):
    try:
        data = pd.read_csv(file_path, on_bad_lines="warn")
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()


@st.cache_data
# Cluster data is obtained from training the models in model.ipynb
def load_cluster_data(file_path):
    try:
        data = pd.read_csv(file_path, on_bad_lines="warn")
        return data
    except Exception as e:
        st.error(f"Failed to load cluster data: {e}")
        return pd.DataFrame()


@st.cache_data
# Map data is calculated from calculate_map.py
def load_map_data(file_path):
    try:
        data = pd.read_csv(file_path, on_bad_lines="warn")
        return data
    except Exception as e:
        st.error(f"Failed to load map data: {e}")
        return pd.DataFrame()


def show_title():
    st.title(
        "How do the affiliations of researchers influence the diversity of engineering research topics?"
    )


def show_overview(data):
    st.header("• Exploring Our Data set")
    # if st.checkbox("Data Preview"):
    st.subheader("Examples of the Data Set")
    st.write(data.head())
    st.subheader("Data Set Statistics")
    st.write(data.describe().head(2))


def show_map(df_dataset, df_map):
    df = df_dataset
    country_freq = df_map
    st.header("• Where Does Our Data Come From?")
    st.map(country_freq)


def show_institute_cluster(df_cluster):
    st.header("• Institution Subject Area Analysis")
    country_list = df_cluster["Country"].unique()
    selected_country = st.selectbox("Select a Country", country_list)
    filtered_by_country = df_cluster[df_cluster["Country"] == selected_country]
    institution_list = filtered_by_country["Institution"].unique()
    selected_institution = st.selectbox("Select an Institution", institution_list)
    filtered_df = filtered_by_country[
        filtered_by_country["Institution"] == selected_institution
    ]
    st.write(f"Largest Subject Areas for {selected_institution}:")
    subject_areas = filtered_df["Subject Area"].unique()
    subject_areas_text = ", ".join(subject_areas)
    st.markdown(
        f"""
        <div style="color: #FFFFFF; padding: 10px; background-color: #262730; font-size: 16px; border-radius: 7.5px;">
            {subject_areas_text}
        </div>
        """,
        unsafe_allow_html=True,
    )
    subject_columns = [
        "Power Systems",
        "Environmental Engineering",
        "Public Health",
        "Social Sciences",
        "Machine Learning",
        "Cancer Research",
        "Materials Science",
        "Food Biotechnology",
        "Nanotechnology",
        "Health Studies",
    ]
    pie_data = filtered_df[subject_columns].iloc[0]
    pie_df = pd.DataFrame({"Subject Area": pie_data.index, "Value": pie_data.values})
    fig = px.pie(
        pie_df,
        names="Subject Area",
        values="Value",
        title=f"Distribution of Subject Areas for {selected_institution}",
        color_discrete_sequence=px.colors.sequential.RdBu,
    )
    st.plotly_chart(fig)


def show_date(dataset):
    st.header("• Published Date Distributions")
    dataset["Date"] = pd.to_datetime(dataset["Date"], errors="coerce")
    dataset = dataset.dropna(subset=["Date"])
    dataset["Year-Month"] = dataset["Date"].dt.to_period("M").astype(str)
    date_data = dataset.groupby("Year-Month")["Title"].count()
    st.bar_chart(date_data)


def run():
    dataset = load_dataset("main_data.csv")
    df_dataset = pd.DataFrame(dataset)

    cluster_data = load_cluster_data("cluster_data.csv")
    df_cluster = pd.DataFrame(cluster_data)

    map_data = load_map_data("calculated_map_data.csv")
    df_map = map_data

    show_title()
    show_overview(dataset)
    show_date(dataset)
    show_map(df_dataset, df_map)
    show_institute_cluster(df_cluster)


run()
