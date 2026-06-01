# app.py
import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
import re

st.set_page_config(page_title="Sentiment Analyzer", layout="wide")

st.title("🎬 Movie Review Sentiment Analysis System")
st.subheader("Deep Learning Based Sentiment Classification")
st.write("---")

# 1. Mock tokenizer preparation matching training environment parameters
# In production, save/load your actual tokenizer object via pickle
@st.cache_resource
def load_models_and_assets():
    # Attempting to load pre-saved native H5 tracking formats
    try:
        simplernn = tf.keras.models.load_model('simplernn_model.h5')
        lstm = tf.keras.models.load_model('lstm_model.h5')
        gru = tf.keras.models.load_model('gru_model.h5')
    except:
        # Fallback initialization stub if models are missing
        st.error("Pre-trained model files (.h5) not found! Run training pipeline first.")
        st.stop()
    return simplernn, lstm, gru

simplernn, lstm, gru = load_models_and_assets()

# Clean Utility Text
def clean_input(text):
    text = text.lower().replace('<br />', '')
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Input Interface
review_input = st.text_area("Enter your movie review here...", height=150, 
                            placeholder="Type a review to see how different architectures interpret it...")

selected_model_name = st.selectbox("Select Target Benchmark Model:", ["LSTM", "GRU", "SimpleRNN"])

if st.button("Analyze Review", type="primary"):
    if review_input.strip() == "":
        st.warning("Please type a valid review first.")
    else:
        # Mapping model instances
        model_map = {"SimpleRNN": simplernn, "LSTM": lstm, "GRU": gru}
        
        # Simple standalone parsing emulation matching IMDB index
        # (For deployment robustness, use actual saved tokenizer.pickle)
        from tensorflow.keras.datasets import imdb
        word_idx = imdb.get_word_index()
        words = clean_input(review_input).split()
        seq = [word_idx.get(w, 2) + 3 for w in words] # Offset to align with standard mapping
        padded_seq = pad_sequences([seq], maxlen=200, padding='post')
        
        # Active Model Inference
        active_model = model_map[selected_model_name]
        raw_score = float(active_model.predict(padded_seq)[0][0])
        
        sentiment = "Positive" if raw_score >= 0.5 else "Negative"
        confidence = raw_score if raw_score >= 0.5 else (1.0 - raw_score)
        
        # UI Outputs layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Selection Prediction Result")
            metric_color = "green" if sentiment == "Positive" else "red"
            st.markdown(f"**Selected Model:** `{selected_model_name}`")
            st.markdown(f"<h4>Sentiment: <span style='color:{metric_color}'>{sentiment}</span></h4>", unsafe_allow_html=True)
            st.metric(label="Confidence Rating", value=f"{confidence * 100:.1f}%")
            
        with col2:
            st.markdown("### Cross-Architecture Comparison Metric")
            # Pull metrics for all 3 for the comparison dashboard
            all_scores = {}
            for name, model_inst in model_map.items():
                all_scores[name] = float(model_inst.predict(padded_seq)[0][0])
            
            # Render Comparative Probabilities
            for name, score in all_scores.items():
                st.write(f"**{name}**")
                st.progress(score)
                st.caption(f"Positivity Probability Score: {score*100:.1f}%")