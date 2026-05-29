import streamlit as st

from langchain_core.messages import HumanMessage, AIMessage

import database



def render_sidebar():

    """Renders a clean, modern Chat History navigator with individual row deletion."""

    with st.sidebar:

        st.markdown("<h3 style='margin-bottom:0px;'>⚡ MindPal</h3>", unsafe_allow_html=True)

        st.caption("Gemini 3.1 Flash-Lite Engine Powered")

        st.markdown("<br>", unsafe_allow_html=True)

       

        # Action button to spawn a new clean session

        if st.button("➕ New Chat", use_container_width=True, type="primary"):

            new_id = f"Chat {len(st.session_state.sessions) + 1}"

            initial_greeting = "Started a new conversation thread. What's on your mind?"

           

            # Save base chat setup directly onto disk

            database.save_message(new_id, "assistant", initial_greeting)

           

            st.session_state.sessions[new_id] = [AIMessage(content=initial_greeting)]

            st.session_state.current_session = new_id

            st.rerun()

           

        st.markdown("<br><p style='font-size:0.85rem; color:#8a8f98; font-weight:600; margin-bottom:5px;'>RECENT CHATS</p>", unsafe_allow_html=True)

       

        # Render a layout row for each active session

        for session_id in list(st.session_state.sessions.keys()):

            is_active = session_id == st.session_state.current_session

            label = f"💬  {session_id}" if not is_active else f"👉  {session_id}"

           

            # Split layout: 85% width for switching chat, 15% for the delete icon

            col_chat, col_del = st.columns([0.85, 0.15])

           

            with col_chat:

                if st.button(label, key=f"switch_{session_id}", use_container_width=True):

                    st.session_state.current_session = session_id

                    st.rerun()

           

            with col_del:

                if st.button("🗑️", key=f"del_{session_id}", help=f"Delete '{session_id}'"):

                    # 1. Remove the chat history list from SQLite database and session state

                    database.delete_session_from_db(session_id)

                    del st.session_state.sessions[session_id]

                   

                    # 2. Safety viewport fallback transitions

                    if st.session_state.current_session == session_id:

                        remaining_sessions = list(st.session_state.sessions.keys())

                        if remaining_sessions:

                            st.session_state.current_session = remaining_sessions[0]

                        else:

                            st.session_state.pop("current_session", None)

                            st.session_state.pop("sessions", None)

                           

                    st.rerun()

               

        # Sticky bottom utilities section inside the sidebar

        st.markdown("<div style='position: fixed; bottom: 20px; width: 14%;'>", unsafe_allow_html=True)

        st.markdown("---")

        if st.button("🚨 Wipe All History", use_container_width=True):

            database.clear_all_db()

            st.session_state.pop("current_session", None)

            st.session_state.pop("sessions", None)

            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)



def render_chat_stream(chat_history):

    """Optimized block to display standard text and composite attachment logs cleanly."""

    chat_container = st.container()

    with chat_container:

        for message in chat_history:

            if isinstance(message, AIMessage):

                with st.chat_message("assistant", avatar="✨"):

                    st.markdown(message.content)

            elif isinstance(message, HumanMessage):

                with st.chat_message("user", avatar="💻"):

                    # Safe validation check if raw data array format is found

                    if isinstance(message.content, list):

                        text_part = message.content[0].get("text", "")

                        st.markdown(text_part)

                        st.info("📎 *Sent an attached image payload*")

                    else:

                        st.markdown(message.content)