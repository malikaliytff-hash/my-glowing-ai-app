import streamlit as st
import google.generativeai as genai

# --- UI Configuration ---
st.set_page_config(page_title="Neon AI Portal", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    .stApp { background: #050505; color: #00f2ff; }
    h1 { color: #00f2ff; text-shadow: 0 0 10px #00f2ff; text-align: center; }
    .stButton>button { 
        border: 2px solid #00f2ff; border-radius: 12px;
        background: transparent; color: #00f2ff; 
        box-shadow: 0 0 15px #00f2ff; transition: 0.3s;
    }
    .stTextInput>div>div>input { border: 2px solid #7000ff; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ Neon AI Portal")

# --- Initialize Session ---
if "api_key" not in st.session_state:
    st.subheader("Setup")
    key_input = st.text_input("Enter your Google API Key", type="password")
    if st.button("Initialize Portal"):
        if key_input.startswith("AIza"):
            st.session_state.api_key = key_input
            st.rerun()
        else:
            st.error("Invalid API Key format.")
            
elif "system_prompt" not in st.session_state:
    st.session_state.system_prompt = st.text_area("System Instructions:", "You are a helpful and expert AI assistant.")
    if st.button("Launch Chat"):
        genai.configure(api_key=st.session_state.api_key)
        # Using the current industry-standard model
        model = genai.GenerativeModel('gemini-3.5-flash')
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

else:
    # --- Chat Interface ---
    if st.sidebar.button("Reset Session"):
        st.session_state.clear()
        st.rerun()
        
    for message in st.session_state.chat.history:
        with st.chat_message(message.role):
            st.markdown(message.parts[0].text)

    if prompt := st.chat_input("Ask anything..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        full_context = f"Instruction: {st.session_state.system_prompt}\n\nUser: {prompt}"
        response = st.session_state.chat.send_message(full_context)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
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
