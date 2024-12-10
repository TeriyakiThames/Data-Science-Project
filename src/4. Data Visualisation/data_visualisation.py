import ast
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import pyLDAvis
import seaborn as sns
import streamlit as st
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer


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


@st.cache_data
def load_document():
    # Load the documents list from the pickle file
    with open("documents.pkl", "rb") as f:
        documents = pickle.load(f)
        return documents


@st.cache_data
def load_doc_term_matrix():
    with open("doc_term_matrix.pkl", "rb") as f:
        doc_term_matrix = pickle.load(f)
        return doc_term_matrix


@st.cache_data
def load_vectorizer():
    with open("vectorizer.pkl", "rb") as f:
        loaded_vectorizer = pickle.load(f)
        return loaded_vectorizer


@st.cache_data
def load_lda_model_fitted():
    with open("lda_model_fitted.pkl", "rb") as f:
        lda_model = pickle.load(f)
        return lda_model


@st.cache_data
def load_kmeans():
    with open("kmeans_model.pkl", "rb") as f:
        kmeans = pickle.load(f)
        return kmeans


def show_title():
    st.title(
        "How do the affiliations of researchers influence the diversity of engineering research topics?"
    )


def show_overview(data):
    st.header("• Exploring Our Data set")
    if st.checkbox("Data Preview"):
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

    # Shows the largest subject areas
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

    # Shows the pie chart
    subject_columns = [
        "Artificial Intelligence",
        "Telecommunication Engineering",
        "Medical Science",
        "Disease Analysis",
        "Biomedical Research",
        "Environmental Science",
        "Pharmaceutical Science",
        "Chemical Science",
        "Energy and Power Systems",
        "Social and Business Studies",
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


def show_cluster(df):
    # List of actual cluster names
    st.header("• K-Means Clustering (PCA)")
    st.markdown(
        """
    - Each dot represents different institutions
    - The colors represents different subject area (cluster)
    - Institution within the same cluster are similar in terms of topic they focus on
    """
    )
    cluster_names_list = [
        "Artificial Intelligence",
        "Telecommunication Engineering",
        "Medical Science",
        "Disease Analysis",
        "Biomedical Research",
        "Environmental Science",
        "Pharmaceutical Science",
        "Chemical Science",
        "Energy and Power Systems",
        "Social and Business Studies",
    ]

    documents = load_document()

    loaded_vectorizer = load_vectorizer()
    doc_term_matrix = loaded_vectorizer.transform(documents)

    lda_model = load_lda_model_fitted()
    doc_topic_matrix = lda_model.transform(doc_term_matrix)

    kmeans = load_kmeans()
    clusters = kmeans.fit_predict(doc_topic_matrix)

    institutions = df["Institution"].tolist()
    institutions = institutions[:-1]

    pca = PCA(n_components=2)
    reduced_matrix = pca.fit_transform(doc_topic_matrix)

    pca_df = pd.DataFrame(reduced_matrix, columns=["PCA1", "PCA2"])
    pca_df["Cluster"] = clusters
    pca_df["Cluster Name"] = pca_df["Cluster"].map(lambda x: cluster_names_list[int(x)])
    pca_df["Institution"] = institutions

    st.write(pca_df[["Institution", "Cluster", "Cluster Name", "PCA1", "PCA2"]])

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x="PCA1",
        y="PCA2",
        hue="Cluster Name",
        palette="Set1",
        data=pca_df,
        s=100,
        marker="o",
    )

    plt.title("PCA of Document-Topic Matrix", fontsize=16)
    plt.xlabel("PCA Component 1", fontsize=14)
    plt.ylabel("PCA Component 2", fontsize=14)

    st.pyplot(plt)
    selected_cluster = st.selectbox("Select Cluster", options=cluster_names_list)
    filtered_df_cluster = pca_df[pca_df["Cluster Name"] == selected_cluster]
    st.write(
        f"Data for selected cluster: {selected_cluster}",
        filtered_df_cluster[["Institution", "Cluster", "Cluster Name"]],
    )


def show_country_insights(data):
    st.header("• Top Contributing Countries")
    if isinstance(data["Country"].iloc[0], str) and data["Country"].iloc[0].startswith(
        "["
    ):
        data["Country"] = data["Country"].apply(ast.literal_eval)
    if isinstance(data["Country"].iloc[0], list):
        data = data.explode("Country")
    country_data = data["Country"].value_counts().head(10)
    st.bar_chart(country_data)


def show_LDA():
    st.header("• LDA: Topic-Intermap (pyLDAvis)")
    st.markdown(
        """
    - The size of the circle indicates the topic’s overall prevalence in the corpus
    - The distance between topics indicates how similar they are
    - For each topic, we can see which keywords are the most prevalent
    """
    )
    data = {
        "Topic": [
            "Topic 1",
            "Topic 2",
            "Topic 3",
            "Topic 4",
            "Topic 5",
            "Topic 6",
            "Topic 7",
            "Topic 8",
            "Topic 9",
            "Topic 10",
        ],
        "Subject Area": [
            "Artificial Intelligence",
            "Disease Analysis",
            "Medical Science",
            "Telecommunication Engineering",
            "Biomedical Research",
            "Environmental Science",
            "Pharmaceutical Science",
            "Chemical Science",
            "Energy and Power Systems",
            "Social and Business Studies",
        ],
    }

    df1 = pd.DataFrame(data).reset_index(drop=True)
    st.table(df1)

    vectorizer = load_vectorizer()
    lda_model = load_lda_model_fitted()
    doc_term_matrix = load_doc_term_matrix()

    vocab = vectorizer.get_feature_names_out()

    # Calculate term frequencies
    term_frequency = np.asarray(doc_term_matrix.sum(axis=0)).flatten()

    # Prepare data for pyLDAvis
    data = pyLDAvis.prepare(
        topic_term_dists=lda_model.components_
        / lda_model.components_.sum(axis=1)[:, np.newaxis],
        doc_topic_dists=lda_model.transform(doc_term_matrix),
        doc_lengths=np.array(doc_term_matrix.sum(axis=1)).flatten(),
        vocab=vocab,
        term_frequency=term_frequency,
        sort_topics=False,  # Set to True if you want topics sorted by relevance
    )

    # Convert to HTML
    html_string = pyLDAvis.prepared_data_to_html(data)

    # Display in Streamlit
    st.components.v1.html(html_string, width=1300, height=800)


def run():
    dataset = load_dataset("main_data.csv")
    df_dataset = pd.DataFrame(dataset)

    cluster_data = load_cluster_data("cluster_data.csv")
    df_cluster = pd.DataFrame(cluster_data)

    map_data = load_map_data("calculated_map_data.csv")
    df_map = map_data

    filter_data = load_cluster_data("filtered_df.csv")
    filtered_df = pd.DataFrame(filter_data)

    show_title()
    show_overview(dataset)
    show_date(dataset)
    show_country_insights(dataset)
    show_map(df_dataset, df_map)
    show_institute_cluster(df_cluster)
    st.title("ML Data Insights Visualisation")
    show_cluster(filtered_df)
    show_LDA()


run()
