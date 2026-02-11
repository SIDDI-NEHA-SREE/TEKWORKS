import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import euclidean_distances


# ---------------------------------------------------------
# Page Config
# ---------------------------------------------------------
st.set_page_config(page_title="NYC Taxi Hotspot Detection", layout="wide")

st.title("🚕 NYC Taxi Pickup Hotspot Analysis")
st.write("Discover natural pickup hotspots using DBSCAN clustering")


# ---------------------------------------------------------
# File Upload
# ---------------------------------------------------------
uploaded_file = st.file_uploader("Upload NYC Taxi CSV File", type=["csv"])


def load_csv_with_encoding(file):
    encodings = ["utf-8", "latin1", "ISO-8859-1"]
    for enc in encodings:
        try:
            file.seek(0)
            return pd.read_csv(file, encoding=enc)
        except Exception:
            continue
    return None


if uploaded_file:

    df = load_csv_with_encoding(uploaded_file)

    if df is None:
        st.error("Could not read file. Please check encoding.")
        st.stop()

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # ---------------------------------------------------------
    # Validate Required Columns
    # ---------------------------------------------------------
    required_cols = ["pickup_latitude", "pickup_longitude"]

    if not all(col in df.columns for col in required_cols):
        st.error("Required columns not found.")
        st.stop()

    # ---------------------------------------------------------
    # Feature Selection
    # ---------------------------------------------------------
    X = df[required_cols].dropna().copy()

    # ---------------------------------------------------------
    # Remove obvious out-of-NYC noise
    # NYC approx bounding box
    # ---------------------------------------------------------
    X = X[
        (X["pickup_latitude"].between(40.5, 41.0)) &
        (X["pickup_longitude"].between(-74.3, -73.6))
    ]

    st.write("Valid Pickup Points:", len(X))

    # ---------------------------------------------------------
    # Sampling (important for large dataset)
    # ---------------------------------------------------------
    max_points = st.sidebar.slider("Max Points to Use", 1000, 50000, 10000)

    if len(X) > max_points:
        X = X.sample(max_points, random_state=42)
        st.info(f"Using random sample of {max_points} points for performance.")

    # ---------------------------------------------------------
    # Scaling
    # ---------------------------------------------------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ---------------------------------------------------------
    # Sidebar Parameters
    # ---------------------------------------------------------
    st.sidebar.header("DBSCAN Parameters")

    eps = st.sidebar.slider("Epsilon (Neighborhood Radius)", 0.1, 3.0, 0.3)
    min_samples = st.sidebar.slider("Min Samples", 3, 20, 5)

    # ---------------------------------------------------------
    # DBSCAN Clustering
    # ---------------------------------------------------------
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric="euclidean")
    clusters = dbscan.fit_predict(X_scaled)

    X["Cluster"] = clusters

    # ---------------------------------------------------------
    # Cluster Summary
    # ---------------------------------------------------------
    n_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
    n_noise = list(clusters).count(-1)

    st.subheader("📊 Cluster Summary")
    col1, col2 = st.columns(2)
    col1.metric("Clusters Found", n_clusters)
    col2.metric("Noise Points Ignored", n_noise)

    # ---------------------------------------------------------
    # Cluster Centers (Hotspot Centers)
    # ---------------------------------------------------------
    if n_clusters > 0:
        centers = (
            X[X["Cluster"] != -1]
            .groupby("Cluster")[["pickup_latitude", "pickup_longitude"]]
            .mean()
        )

        st.subheader("📍 Cluster Centers (Hotspots)")
        st.dataframe(centers)

    # ---------------------------------------------------------
    # Visualization
    # ---------------------------------------------------------
    st.subheader("🗺 Pickup Hotspot Map")

    fig, ax = plt.subplots(figsize=(10, 8))

    unique_clusters = set(clusters)

    for cluster in unique_clusters:
        if cluster == -1:
            color = "black"
            label = "Noise"
            size = 3
        else:
            color = None
            label = f"Cluster {cluster}"
            size = 5

        cluster_points = X[X["Cluster"] == cluster]

        ax.scatter(
            cluster_points["pickup_longitude"],
            cluster_points["pickup_latitude"],
            s=size,
            label=label
        )

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("DBSCAN Identified Pickup Hotspots")
    ax.legend(markerscale=3, fontsize=8)

    st.pyplot(fig)

    # ---------------------------------------------------------
    # Euclidean Distance Example
    # ---------------------------------------------------------
    st.subheader("📐 Sample Euclidean Distance")

    if len(X_scaled) >= 2:
        dist = euclidean_distances(
            [X_scaled[0]],
            [X_scaled[1]]
        )[0][0]

        st.write(
            "Distance between first two scaled pickup points:",
            round(dist, 4)
        )

else:
    st.info("Upload the NYC Taxi dataset CSV file to begin.")
