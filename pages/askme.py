import streamlit as st
from rag import chat
import uuid

st.set_page_config(page_title="Ask Me", page_icon="💬")
st.title("Ask Me")

# Initializing global variables
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.messages = []
    st.session_state.chat_started = False

def initialize_session_state():
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())

def display_chat_history():
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])
        else:
            st.chat_message("user").write(message["content"])

def handle_chat():
    conversation_messages = []

    if not st.session_state.chat_started:
        greeting_msg = "Hi! GinoChat here, ready to embark on a knowledge journey?"
        conversation_messages.append({"role": "assistant", "content": greeting_msg})
        st.session_state.chat_started = True

    if prompt := st.chat_input("Seeking anything?"):
        conversation_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            response = chat(prompt, st.session_state.session_id, st.session_state.user_id)['output']
            conversation_messages.append({"role": "assistant", "content": response})

    st.session_state.messages = conversation_messages

def show_askme():
    initialize_session_state()
    handle_chat()
    display_chat_history()

if __name__ == "__main__":
    show_askme()