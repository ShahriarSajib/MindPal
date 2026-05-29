import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
import io

import config
import database
from chat_engine import ChatbotEngine
import ui_components

# 1. Base Streamlit Page Setups
st.set_page_config(page_title="MindPal", page_icon="⚡", layout="centered")
config.inject_custom_css()

# 2. Key Provision & Backend Initialization
api_key = config.get_api_key()

if not api_key:
    st.error("🔒 Missing API Credential. Please configure your GOOGLE_API_KEY in your environment.")
    st.stop()

if "bot_engine" not in st.session_state:
    st.session_state.bot_engine = ChatbotEngine(api_key=api_key)

# --- RESILIENT DATABASE SYNCHRONIZER HUB ---
if "sessions" not in st.session_state or not st.session_state.sessions:
    db_backup_records = database.load_all_sessions()
    if db_backup_records:
        st.session_state.sessions = db_backup_records
    else:
        # Ground zero baseline save if database file is fresh/blank
        init_greet = "Hello! I'm your Pal. How can I help you today?"
        database.save_message("Chat 1", "assistant", init_greet)
        st.session_state.sessions = {"Chat 1": [AIMessage(content=init_greet)]}

if "current_session" not in st.session_state or st.session_state.current_session not in st.session_state.sessions:
    st.session_state.current_session = list(st.session_state.sessions.keys())[0]

# Reference shortcuts for readability
current_session_id = st.session_state.current_session
active_chat_history = st.session_state.sessions[current_session_id]

# 3. Sidebar Components (Handles session creation and switching)
ui_components.render_sidebar()

# 4. Main Chat Interface Execution
st.title("⚡ MindPal")
st.caption("Engineered Core Pipeline: Permanent Storage & Context Streaming Enabled")

# Render active dialog stack
ui_components.render_chat_stream(active_chat_history)

# ==========================================
# FILE PROCESSING & FILE UPLOADER COMPONENT
# ==========================================
uploaded_asset = st.file_uploader("📎 Analyze file attachments or system documents contextually", type=["png", "jpg", "jpeg", "txt"])
st_file_payload = None

if uploaded_asset is not None:
    asset_ext = uploaded_asset.name.split(".")[-1].lower()
    
    if asset_ext in ["png", "jpg", "jpeg"]:
        st.image(uploaded_asset, caption="Visual Attachment Input Matrix", width=240)
        st_file_payload = {"bytes": uploaded_asset.getvalue(), "mime": uploaded_asset.type, "mode": "vision"}
        
    elif asset_ext == "txt":
        extracted_text_block = io.StringIO(uploaded_asset.getvalue().decode("utf-8")).read()
        st.success(f"📄 Text Matrix '{uploaded_asset.name}' Loaded! ({len(extracted_text_block)} characters compiled.)")
        st_file_payload = {"text": extracted_text_block, "name": uploaded_asset.name, "mode": "document"}

# ==========================================
# 5. USER INPUT HANDLING & STREAMING PIPELINE
# ==========================================
if user_input := st.chat_input("Message Pal..."):
    
    # Context Augmentation Execution Block
    if st_file_payload and st_file_payload["mode"] == "vision":
        # Formulate a structured multimodal message
        composed_msg = st.session_state.bot_engine.format_multimodal_message(
            user_input, st_file_payload["bytes"], st_file_payload["mime"]
        )
        with st.chat_message("user", avatar="💻"):
            st.markdown(user_input)
            st.info("📎 *Sent an attached image payload*")
            
        active_chat_history.append(composed_msg)
        database.save_message(current_session_id, "user", f"[Image Attached File] {user_input}")
        
    elif st_file_payload and st_file_payload["mode"] == "document":
        # Augment document contents into prompt context window payload
        prompt_with_document = f"--- ATTACHED DOCUMENT: {st_file_payload['name']} ---\n{st_file_payload['text']}\n--------------------\n\nUser Message: {user_input}"
        composed_msg = HumanMessage(content=prompt_with_document)
        
        with st.chat_message("user", avatar="💻"):
            st.markdown(user_input)
            
        active_chat_history.append(composed_msg)
        database.save_message(current_session_id, "user", user_input)
        
    else:
        # Standard pure text message pipeline execution
        composed_msg = HumanMessage(content=user_input)
        with st.chat_message("user", avatar="💻"):
            st.markdown(user_input)
            
        active_chat_history.append(composed_msg)
        database.save_message(current_session_id, "user", user_input)

    # Stream out the assistant response via st.write_stream
    with st.chat_message("assistant", avatar="✨"):
        ai_output = st.write_stream(st.session_state.bot_engine.stream_response(active_chat_history))
            
    # Commit final output string safely back to transient memory state and database logs
    active_chat_history.append(AIMessage(content=ai_output))
    database.save_message(current_session_id, "assistant", ai_output)
    
    # Auto-rename the chat title if it's still generic based on the first question
    if current_session_id.startswith("Chat ") and len(active_chat_history) <= 3:
        new_name = user_input[:20] + "..." if len(user_input) > 20 else user_input
        
        st.session_state.sessions[new_name] = st.session_state.sessions.pop(current_session_id)
        st.session_state.current_session = new_name
        
        # Rewrite matching transaction pointers in database index
        database.delete_session_from_db(current_session_id)
        for msg in st.session_state.sessions[new_name]:
            role_tag = "assistant" if isinstance(msg, AIMessage) else "user"
            clean_str = msg.content[0].get("text", "") if isinstance(msg.content, list) else msg.content
            database.save_message(new_name, role_tag, clean_str)
            
        st.rerun()