import streamlit as st
import google.generativeai as genai

# --- Fancy CSS for Glowing Effect ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .stButton>button { 
        border: 2px solid #00f2ff; 
        box-shadow: 0 0 15px #00f2ff; 
        color: white; 
        background: transparent; 
    }
    .stTextInput>div>div>input { 
        border: 1px solid #7000ff; 
        box-shadow: 0 0 5px #7000ff; 
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ Neon AI Portal")

# Session State Management
if "api_key" not in st.session_state:
    provider = st.selectbox("Select AI Provider", ["Gemini", "ChatGPT", "Deepseek"])
    api_key = st.text_input("Enter API Key", type="password")
    
    if st.button("Connect"):
        if provider == "Gemini" and api_key.startswith("AIza"):
            st.session_state.api_key = api_key
            st.session_state.provider = provider
            st.rerun()
        else:
            st.error("Invalid Key or Provider Mismatch")

elif "system_prompt" not in st.session_state:
    st.subheader("Configure your AI")
    st.session_state.system_prompt = st.text_area("Give special instructions to the AI:")
    if st.button("Start Chatting"):
        st.rerun()

else:
    # --- Main Chat Interface ---
    st.sidebar.button("Reset Session", on_click=lambda: st.session_state.clear())
    uploaded_file = st.file_uploader("Upload a file")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("What is on your mind?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Basic logic for Gemini integration
        genai.configure(api_key=st.session_state.api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"{st.session_state.system_prompt}\n\n{prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
