# ==========================================================
# 🟣 NEWS TOPIC DISCOVERY DASHBOARD
# Hierarchical Clustering with Euclidean Distance
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
import seaborn as sns
import plotly.express as px

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_similarity
import chardet

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------

st.set_page_config(layout="wide")
st.title("🟣 News Topic Discovery Dashboard")
st.markdown(
    "This system uses **Hierarchical Clustering** to automatically group similar news articles based on textual similarity."
)

# ----------------------------------------------------------
# SIDEBAR – DATASET UPLOAD (FIXED)
# ----------------------------------------------------------

st.sidebar.header("📂 Dataset Upload")

def detect_encoding(file):
    raw_data = file.read(100000)
    result = chardet.detect(raw_data)
    file.seek(0)
    return result["encoding"]

def load_csv(file):
    try:
        encoding = detect_encoding(file)
        file.seek(0)
        df = pd.read_csv(file, encoding=encoding)
        return df, encoding
    except Exception:
        # fallback encodings
        for enc in ["utf-8", "utf-8-sig", "latin1", "ISO-8859-1", "cp1252"]:
            try:
                file.seek(0)
                df = pd.read_csv(file, encoding=enc)
                return df, enc
            except:
                continue
    return None, None


uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is None:
    st.warning("Please upload a CSV file.")
    st.stop()

df, detected_encoding = load_csv(uploaded_file)

if df is None:
    st.error("Unable to read CSV file. Unsupported encoding.")
    st.stop()

st.sidebar.success(f"Detected Encoding: {detected_encoding}")

# ----------------------------------------------------------
# TEXT COLUMN SELECTION
# ----------------------------------------------------------

st.sidebar.header("📝 Text Configuration")

text_columns = st.sidebar.multiselect(
    "Select Text Columns",
    options=df.columns,
    default=[df.columns[0]]
)

if len(text_columns) == 0:
    st.error("Select at least one text column.")
    st.stop()

df["combined_text"] = df[text_columns].astype(str).agg(" ".join, axis=1)

category_column = st.sidebar.selectbox(
    "Optional Category Column (For Comparison)",
    ["None"] + list(df.columns)
)

# ----------------------------------------------------------
# TF-IDF SETTINGS
# ----------------------------------------------------------

max_features = st.sidebar.slider("Maximum TF-IDF Features", 100, 2000, 1000)
remove_stopwords = st.sidebar.checkbox("Remove English Stopwords", value=True)

ngram_option = st.sidebar.selectbox(
    "N-gram Range",
    ["Unigrams", "Bigrams", "Unigrams + Bigrams"]
)

if ngram_option == "Unigrams":
    ngram_range = (1, 1)
elif ngram_option == "Bigrams":
    ngram_range = (2, 2)
else:
    ngram_range = (1, 2)

min_df = st.sidebar.slider("Minimum Document Frequency", 1, 10, 2)
max_df = st.sidebar.slider("Maximum Document Frequency", 0.5, 1.0, 0.95)

vectorizer = TfidfVectorizer(
    max_features=max_features,
    stop_words="english" if remove_stopwords else None,
    ngram_range=ngram_range,
    min_df=min_df,
    max_df=max_df
)

X = vectorizer.fit_transform(df["combined_text"])

# ----------------------------------------------------------
# HIERARCHICAL SETTINGS
# ----------------------------------------------------------
subset_size = st.sidebar.slider(
    "Articles for Dendrogram",
    min_value=20,
    max_value=min(200, len(df)),
    value=min(50, len(df))
)

num_clusters = st.sidebar.slider(
    "Number of Clusters",
    min_value=2,
    max_value=15,
    value=4
)

st.sidebar.header("🌳 Clustering Controls")

linkage_method = st.sidebar.selectbox(
    "Linkage Method",
    ["ward", "complete", "average", "single"]
)

# Force Euclidean for Ward
if linkage_method == "ward":
    distance_metric = "euclidean"
    st.sidebar.info("Ward linkage requires Euclidean distance.")
else:
    distance_metric = st.sidebar.selectbox(
        "Distance Metric",
        ["euclidean"]
    )

# ----------------------------------------------------------
# DENDROGRAM
# ----------------------------------------------------------

if st.button("🟦 Generate Dendrogram"):

    st.subheader("Dendrogram")

    X_subset = X[:subset_size].toarray()

    linkage_matrix = sch.linkage(
        X_subset,
        method=linkage_method,
        metric=distance_metric
    )

    fig = plt.figure(figsize=(10, 6))
    sch.dendrogram(linkage_matrix)
    plt.xlabel("Article Index")
    plt.ylabel("Distance")
    st.pyplot(fig)


# ----------------------------------------------------------
# APPLY CLUSTERING
# ----------------------------------------------------------

if st.button("🟩 Apply Clustering"):

    X_dense = X.toarray()

    model = AgglomerativeClustering(
        n_clusters=num_clusters,
        linkage=linkage_method,
        metric=distance_metric
    )

    clusters = model.fit_predict(X_dense)
    df["Cluster"] = clusters

    # ✅ Correct silhouette calculation (dense matrix only)
    score = silhouette_score(X_dense, clusters, metric="euclidean")

    # ------------------------------------------------------
    # SILHOUETTE SCORE
    # ------------------------------------------------------

    st.subheader("📊 Silhouette Score")
    st.write(round(score, 4))

    if score > 0.5:
        st.success("Clusters are well separated.")
    elif score > 0.2:
        st.info("Clusters moderately separated.")
    else:
        st.warning("Clusters may overlap.")

    # ------------------------------------------------------
    # PCA VISUALIZATION
    # ------------------------------------------------------

    st.subheader("📍 PCA Cluster Visualization")

    pca = PCA(n_components=2)
    X_reduced = pca.fit_transform(X_dense)

    fig = px.scatter(
        x=X_reduced[:, 0],
        y=X_reduced[:, 1],
        color=df["Cluster"].astype(str),
        hover_data={"Snippet": df["combined_text"].str[:150]},
        title="Cluster Projection (PCA 2D)"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------
    # CLUSTER SUMMARY
    # ------------------------------------------------------

    st.subheader("📋 Cluster Summary")

    terms = vectorizer.get_feature_names_out()
    cluster_summary = []

    for i in range(num_clusters):

        cluster_indices = np.where(clusters == i)[0]
        cluster_size = len(cluster_indices)

        if cluster_size == 0:
            continue

        cluster_tfidf_mean = np.asarray(
            X[cluster_indices].mean(axis=0)
        ).flatten()

        top_indices = cluster_tfidf_mean.argsort()[-10:][::-1]
        top_terms = [terms[idx] for idx in top_indices]

        cluster_summary.append({
            "Cluster ID": i,
            "Number of Articles": cluster_size,
            "Top Keywords": ", ".join(top_terms[:5])
        })

    summary_df = pd.DataFrame(cluster_summary)
    st.dataframe(summary_df)

    # ------------------------------------------------------
    # CATEGORY VS CLUSTER
    # ------------------------------------------------------

    if category_column != "None":

        st.subheader("📊 Cluster vs Category Comparison")

        contingency = pd.crosstab(df["Cluster"], df[category_column])
        st.dataframe(contingency)

        fig = plt.figure(figsize=(8, 6))
        sns.heatmap(contingency, annot=True, fmt="d")
        st.pyplot(fig)

    # ------------------------------------------------------
    # DOWNLOAD
    # ------------------------------------------------------

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Clustered Dataset",
        csv,
        "clustered_news.csv",
        "text/csv"
    )

    # ------------------------------------------------------
    # BUSINESS INTERPRETATION
    # ------------------------------------------------------

    st.subheader("🧠 Business Interpretation")

    for row in cluster_summary:
        st.markdown(
            f"**Cluster {row['Cluster ID']}** focuses on themes such as: {row['Top Keywords']}."
        )

