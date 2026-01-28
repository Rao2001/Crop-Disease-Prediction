import streamlit as st
from PIL import Image
import numpy as np
import os

# Import local modules
from prediction import load_model, predict_image
from utils import get_disease_info, custom_css
from gemini_service import configure_gemini, get_ai_treatment_plan, get_chat_response

# --- Page Configuration ---
st.set_page_config(
    page_title="Crop Doctor AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Apply Custom CSS ---
st.markdown(custom_css(), unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("🌿 Crop Doctor AI")
    st.markdown("---")
    
    # API Key Configuration
    st.subheader("🔑 AI Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API Key to enable the AI Agronomist.")
    
    if api_key:
        if configure_gemini(api_key):
            st.success("AI Connected!")
        else:
            st.error("Invalid API Key")
    else:
        st.warning("Enter API Key to unlock AI features.")
        
    st.markdown("---")
    st.subheader("About")
    st.write(
        "This tool uses deep learning to identify crop diseases from leaf images. "
        "Simply upload a photo to get a diagnosis and treatment recommendations."
    )
    st.markdown("---")
    st.info("Supported Crops: Apple, Corn, Grape, Potato, Tomato, and more.")

# --- Main Content ---
st.title("🌱 Crop Disease Prediction & Analysis")
st.markdown("### Detect diseases accurately and get instant remedies.")

# --- Model Loading ---
# --- Model Loading ---
MODEL_PATH = './models/crop_disease_model.h5'
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = './crop_disease_model.h5' # Fallback to root

model = load_model(MODEL_PATH)

if model is None:
    st.warning("⚠️ Model file not found at `./models/crop_disease_model.h5`. Please run the training notebook to generate the model first.")
    # Option to use a 'demo mode' could go here, but for now we'll just wait for the model.
else:
    st.success("✅ AI Model Loaded Successfully")

# --- File Uploader ---
st.markdown("---")
uploaded_file = st.file_uploader("📸 Upload a leaf image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display Image
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Captured Image")
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True, caption="Uploaded Leaf")

    with col2:
        st.subheader("Analysis Results")
        
        if model is not None:
            if st.button("🔍 Analyze Image", type="primary"):
                with st.spinner("Analyzing leaf patterns..."):
                    predicted_class, confidence = predict_image(image, model)
                
                # Store prediction in session state for Chat context
                st.session_state['last_prediction'] = predicted_class
                
                # Display Result
                st.markdown(f"""
                <div class="prediction-card">
                    <div class="metric-container">
                        <h3>Prediction</h3>
                        <p style="font-size: 1.5em; color: #2c3e50;">{predicted_class.replace('_', ' ')}</p>
                        <h3>Confidence</h3>
                        <p class="confidence-score">{confidence}%</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Dynamic Logic: We no longer have a static database for *every possible* crop in the world.
                # We prioritize Gemini for details.
                
                # Check if we have basic info in utils (for backward compatibility or common crops)
                # But for a truly "Universal" app, we rely on the AI Agronomist mainly.
                info = get_disease_info(predicted_class)
                
                # Only show static info if it's not the "Default/Unknown" response or if we want to show a placeholder
                if info['severity'] != "Unknown":
                     if info['severity'] != "None":
                         st.error(f"**Severity:** {info['severity']}")
                     else:
                        st.success("**Status:** Healthy")
                     
                     with st.expander("ℹ️ Quick Reference (Static DB)", expanded=False):
                        st.write(info['description'])
                        st.write(f"**Treatment:** {info['treatment']}")
                else:
                    st.info("ℹ️ No static record found for this specific class. Use the AI Agronomist below for a custom report.")

# --- AI Agronomist Section ---
if uploaded_file is not None and 'last_prediction' in st.session_state and api_key:
    st.markdown("---")
    st.subheader("👨‍🌾 Ask the AI Agronomist (Powered by Gemini)")
    st.caption(f"Analyzing: {st.session_state['last_prediction']}")
    
    # ... (Rest of UI remains similar but ensures context is passed)
    tab1, tab2 = st.tabs(["📑 Detailed Report", "💬 Chat with Expert"])
    
    with tab1:
        if st.button("✨ Generate Comprehensive Report"):
            with st.spinner("Consulting the AI Agronomist..."):
                # We pass the predicted class name directly to Gemini
                # It doesn't matter if it's "Apple_Scab" or "Rare_Exotic_Fruit_Disease"
                # Gemini will understand the text.
                report = get_ai_treatment_plan(st.session_state['last_prediction'], "High") 
                st.markdown(report)
                
    with tab2:
        st.info(f"Chat context: **{st.session_state['last_prediction'].replace('_', ' ')}**")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("Ask a follow-up question..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = get_chat_response(st.session_state.messages, prompt, st.session_state['last_prediction'])
                message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Built with ❤️ using TensorFlow & Streamlit</div>", 
    unsafe_allow_html=True
)
