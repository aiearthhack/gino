import streamlit as st
from rag import chat
import uuid

import streamlit as st
from rag import chat
import uuid

st.title("Ask Me")

# Initializing global variables
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.messages = []
    st.session_state.chat_started = False


def initialize_session_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    if "greeting_displayed" not in st.session_state:
        st.session_state.greeting_displayed = False


def display_chat_history():
    displayed_conversations = set()
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])
        else:
            st.chat_message("user").write(message["content"])


def handle_chat():
    if not st.session_state.chat_started:
        greeting()
    if prompt := st.chat_input("Seeking anything?"):
        st.session_state.chat_started = True
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner("Thinking..."):
            response = chat(
                prompt, st.session_state.session_id, st.session_state.user_id
            )["output"]
        st.session_state.messages.append({"role": "assistant", "content": response})
        # with st.chat_message("assistant"):
        #     st.markdown(response)


def greeting():
    if not st.session_state.greeting_displayed:
        greeting_msg = "Hi! GinoChat here, ready to embark on a knowledge journey?"
        st.session_state.messages.append({"role": "assistant", "content": greeting_msg})


def show_askme():
    initialize_session_state()
    handle_chat()
    display_chat_history()


if __name__ == "__main__":
    show_askme()
