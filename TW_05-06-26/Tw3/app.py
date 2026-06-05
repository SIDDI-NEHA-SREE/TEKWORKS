import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Medical Report Understanding System",
    layout="wide"
)

st.title("🏥 Intelligent Medical Report Understanding System")

# ======================================================
# POSITIONAL ENCODING
# ======================================================

def positional_encoding(max_position, d_model):

    pe = np.zeros((max_position, d_model))

    for pos in range(max_position):

        for i in range(0, d_model, 2):

            pe[pos, i] = np.sin(
                pos / (10000 ** (i / d_model))
            )

            if i + 1 < d_model:

                pe[pos, i + 1] = np.cos(
                    pos / (10000 ** (i / d_model))
                )

    return pe

# ======================================================
# DEMO PREDICTION FUNCTION
# Replace with trained model prediction
# ======================================================

def predict_specialty(text):

    text = text.lower()

    if any(word in text for word in
           ["stroke", "brain", "seizure", "neurologic"]):
        return "Neurology", 0.95

    elif any(word in text for word in
             ["fracture", "bone", "spine"]):
        return "Orthopedics", 0.93

    elif any(word in text for word in
             ["heart", "cardiac", "artery", "chest pain"]):
        return "Cardiology", 0.94

    elif any(word in text for word in
             ["skin", "rash", "dermatology"]):
        return "Dermatology", 0.92

    elif any(word in text for word in
             ["xray", "ct", "mri", "scan"]):
        return "Radiology", 0.91

    else:
        return "Unknown", 0.70

# ======================================================
# IMPORTANT TERMS
# ======================================================

important_terms = [
    "stroke",
    "fracture",
    "tumor",
    "infection",
    "brain",
    "cardiac",
    "spine",
    "pain",
    "lesion",
    "seizure"
]

# ======================================================
# FILE UPLOAD
# ======================================================

uploaded_file = st.file_uploader(
    "Upload Medical Report (.txt)",
    type=["txt"]
)

if uploaded_file is not None:

    report_text = uploaded_file.read().decode("utf-8")

    st.subheader("Uploaded Medical Report")

    st.text_area(
        "Report Content",
        report_text,
        height=250
    )

    # ==================================================
    # PREDICTION
    # ==================================================

    specialty, confidence = predict_specialty(
        report_text
    )

    st.subheader("Prediction")

    st.success(
        f"Predicted Specialty: {specialty}"
    )

    st.metric(
        "Confidence Score",
        f"{confidence*100:.2f}%"
    )

    # ==================================================
    # IMPORTANT TERMS
    # ==================================================

    st.subheader(
        "Important Medical Terms"
    )

    detected_terms = []

    report_lower = report_text.lower()

    for term in important_terms:

        if term in report_lower:

            detected_terms.append(term)

    if detected_terms:

        st.write(detected_terms)

    else:

        st.write(
            "No important medical terms detected."
        )

    # ==================================================
    # ATTENTION MAP
    # ==================================================

    st.subheader("Attention Map")

    attention_scores = np.random.rand(
        10,
        10
    )

    fig, ax = plt.subplots(
        figsize=(6,4)
    )

    sns.heatmap(
        attention_scores,
        cmap="viridis",
        ax=ax
    )

    ax.set_title(
        "Attention Heatmap"
    )

    st.pyplot(fig)

    # ==================================================
    # POSITIONAL ENCODING HEATMAP
    # ==================================================

    st.subheader(
        "Positional Encoding Heatmap"
    )

    pe = positional_encoding(
        50,
        32
    )

    fig2, ax2 = plt.subplots(
        figsize=(10,5)
    )

    sns.heatmap(
        pe,
        cmap="viridis",
        ax=ax2
    )

    ax2.set_title(
        "Positional Encoding"
    )

    st.pyplot(fig2)

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.write(
    "Healthcare NLP Project | Medical Report Understanding System"
)
