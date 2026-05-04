import streamlit as st
import requests
import json

# --- CONFIGURATION ---
# Apni Raw Gist URL yahan dalo (Wahi jo update.py mein thi)
GIST_RAW_URL = "https://gist.github.com/Dragoboy14/0b338953c699b52709dc1174f96e0b77"

st.set_page_config(page_title="Darsh AI", page_icon="🤖")
st.title("🤖 Code Master AI")

# --- FUNCTION: FETCH URL FROM GIST ---
def get_ollama_url():
    try:
        response = requests.get(GIST_RAW_URL)
        if response.status_code == 200:
            return response.text.strip()
        else:
            st.error("Gist se URL fetch nahi ho paya!")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- SESSION STATE: MEMORY (Last 10 Messages) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CHAT UI ---
# Purane messages display karo
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Bhai, kya poochna hai?"):
    # 1. User message dikhao aur save karo
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Ollama URL lao
    base_url = get_ollama_url()
    
    if base_url:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Memory Management: Sirf last 10 messages bhejna
            # (System prompt + last 10 messages)
            context = st.session_state.messages[-10:]
            
            try:
                # Ollama API Call
                response = requests.post(
                    f"{base_url}/api/chat",
                    json={
                        "model": "darshai", # Tera register kiya hua model
                        "messages": context,
                        "stream": True
                    },
                    stream=True
                )
                
                # Streaming Response handle karo
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if "message" in chunk:
                            content = chunk["message"].get("content", "")
                            full_response += content
                            message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                # 3. Assistant response save karo
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Ollama se baat nahi ho payi: {e}")

# Memory Cleanup: Agar 20 se zyada messages ho jayein (User+AI), toh purane delete karo
if len(st.session_state.messages) > 20:
    st.session_state.messages = st.session_state.messages[-20:]
