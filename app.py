import streamlit as st
from PIL import Image
import os
import time

# Import local modules
from utils import custom_css, set_background
from gemini_service import configure_gemini, analyze_image_with_gemini, get_chat_response

# --- Page Configuration ---
st.set_page_config(
    page_title="Crop Doctor AI - Professional",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Apply Custom CSS ---
st.markdown(custom_css(), unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("🌿 Crop Doctor Pro")
    st.markdown("---")
    
    # API Key Configuration
    st.subheader("🔑 System Configuration")
    
    st.markdown("Get your free key here: [Google AI Studio](https://aistudio.google.com/app/apikey)")
    
    # Check if key is in secrets
    if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("API Key loaded from secrets 🔒")
    else:
        api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API Key to enable the Universal Disease Recognition System.")
        
        # Auto-Save Option
        if api_key:
            if st.button("💾 Save Key for Future"):
                try:
                    secrets_path = os.path.join(".streamlit", "secrets.toml")
                    os.makedirs(".streamlit", exist_ok=True)
                    with open(secrets_path, "w") as f:
                        f.write(f'GEMINI_API_KEY = "{api_key}"\n')
                    st.success("Key saved! It will load automatically next time.")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not save key: {e}")
    
    if api_key:
        with st.spinner("Connecting to Global Knowledge Base..."):
            is_connected, error_msg = configure_gemini(api_key)
            if is_connected:
                st.success("✅ System Online")
            else:
                st.error(f"❌ Connection Failed: {error_msg}")
    else:
        st.warning("⚠️ System Offline. Connect API Key.")
        
    st.markdown("---")
    st.info("Universal Mode Active: Capable of analyzing any crop, fruit, or vegetable disease using advanced Computer Vision.")

# --- Main Content ---
st.title("🌱 Universal Crop Disease Diagnosis")
st.markdown("### Professional Grade AI-Powered Plant Pathology")

# --- File Uploader ---
st.markdown("---")
uploaded_file = st.file_uploader("📸 Upload High-Resolution Specimen", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display Image
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Specimen View")
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True, caption="captured_sample.jpg")

    with col2:
        st.subheader("Diagnostic Report")
        
        if not api_key:
            st.error("🛑 Analysis Halted. Authentication Required.")
            st.write("Please enter your Gemini API Key in the sidebar to proceed with analysis.")
        else:
            if st.button("🔍 Run Full Analysis", type="primary"):
                with st.spinner("Processing biological data... Identifying pathogens..."):
                    # Call Gemini Service
                    result = analyze_image_with_gemini(image, api_key)
                    
                    if "error" in result:
                        st.error(f"Analysis Error: {result['error']}")
                    else:
                        # Store context for chat
                        st.session_state['last_diagnosis'] = f"{result.get('plant_name', 'Plant')} - {result.get('disease_name', 'Issue')}"
                        
                        # Display Results nicely
                        st.markdown(f"""
                        <div class="prediction-card">
                            <div class="metric-container">
                                <h3>Condition Identified</h3>
                                <p style="font-size: 1.8em; color: #e74c3c;">{result.get('disease_name', 'Unknown')}</p>
                                <p><strong>Plant:</strong> {result.get('plant_name', 'Unknown')}</p>
                                <div style="display: flex; justify-content: space-between; width: 100%;">
                                    <span><strong>Status:</strong> {result.get('status', 'Unknown')}</span>
                                    <span><strong>Confidence:</strong> {result.get('confidence', 0)}%</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("📝 Detailed Pathologist Notes", expanded=True):
                            st.markdown(f"**Visual Symptoms:**\n{result.get('description', 'No description available.')}")
                            
                        with st.expander("💊 Treatment & Management Plan", expanded=True):
                            st.markdown(f"**Action Required:**\n{result.get('treatment', 'No treatment plan available.')}")
                            st.markdown(f"**Prevention:**\n{result.get('prevention', 'No prevention data.')}")

# --- AI Consultant Chat ---
if 'last_diagnosis' in st.session_state and api_key:
    st.markdown("---")
    st.subheader("💬 Consult with AI Agronomist")
    st.info(f"Context: Discussing **{st.session_state['last_diagnosis']}**")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a follow-up question about this diagnosis..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = get_chat_response(st.session_state.messages, prompt, st.session_state['last_diagnosis'])
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>Powered by Google Gemini 1.5 Vision Model</div>", 
    unsafe_allow_html=True
)
