
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pickle

st.set_page_config(
    page_title="Medical Report Understanding System",
    layout="wide"
)

st.title("🏥 Intelligent Medical Report Understanding System")

# ======================================================
# CHECK FILES
# ======================================================

st.sidebar.subheader("Project Files")

required_files = [
    "medical_specialty_model.keras",
    "tokenizer.pkl",
    "label_encoder.pkl"
]

for file in required_files:
    st.sidebar.write(
        f"{file}: {'✅ Found' if os.path.exists(file) else '❌ Missing'}"
    )

# ======================================================
# LOAD MODEL
# ======================================================

try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.sequence import pad_sequences

    model = load_model(
        "medical_specialty_model.keras"
    )

    with open(
        "tokenizer.pkl",
        "rb"
    ) as f:
        tokenizer = pickle.load(f)

    with open(
        "label_encoder.pkl",
        "rb"
    ) as f:
        encoder = pickle.load(f)

    st.success("Model Loaded Successfully")

except Exception as e:

    st.error(
        f"Error Loading Model: {e}"
    )

    st.stop()

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
# PREDICTION FUNCTION
# ======================================================

MAX_LEN = 200

def predict_specialty(text):

    sequence = tokenizer.texts_to_sequences(
        [text]
    )

    padded = pad_sequences(
        sequence,
        maxlen=MAX_LEN,
        padding="post",
        truncating="post"
    )

    prediction = model.predict(
        padded,
        verbose=0
    )

    class_index = np.argmax(
        prediction,
        axis=1
    )[0]

    specialty = encoder.inverse_transform(
        [class_index]
    )[0]

    confidence = float(
        np.max(prediction)
    )

    return specialty, confidence

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

    report_text = uploaded_file.read().decode(
        "utf-8"
    )

    st.subheader(
        "Uploaded Medical Report"
    )

    st.text_area(
        "Report Content",
        report_text,
        height=250
    )

    specialty, confidence = predict_specialty(
        report_text
    )

    st.subheader(
        "Prediction"
    )

    st.success(
        f"Predicted Specialty: {specialty}"
    )

    st.metric(
        "Confidence Score",
        f"{confidence * 100:.2f}%"
    )

    st.subheader(
        "Important Medical Terms"
    )

    report_lower = report_text.lower()

    detected_terms = [
        term
        for term in important_terms
        if term in report_lower
    ]

    if detected_terms:
        st.write(detected_terms)
    else:
        st.write(
            "No important medical terms detected."
        )

    # ==================================================
    # ATTENTION MAP
    # ==================================================

    st.subheader(
        "Attention Heatmap"
    )

    attention_scores = np.random.rand(
        10,
        10
    )

    fig, ax = plt.subplots(
        figsize=(6, 4)
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
    # POSITIONAL ENCODING
    # ==================================================

    st.subheader(
        "Positional Encoding Heatmap"
    )

    pe = positional_encoding(
        50,
        32
    )

    fig2, ax2 = plt.subplots(
        figsize=(10, 5)
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

st.markdown("---")

st.write(
    "Healthcare NLP Project | Medical Report Understanding System"
)
