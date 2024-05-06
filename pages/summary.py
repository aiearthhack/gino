import streamlit as st


st.set_page_config(layout="wide")

st.title("Smart Summarizer")

def get_summary(data):
    return "lorem ipsum..."

data = {}
data['length'] = st.sidebar.radio("Summary length", ["short", "medium", "long"], horizontal=True)

data['style'] = st.sidebar.radio("Summary style", ["bullet points", "paragraph"], horizontal=True)

data['more_instructions'] = st.sidebar.text_area("More instructions:")

submit = st.sidebar.button("Submit")

if submit:
    st.write(data)
    st.session_state['summary'] = get_summary(data)
    st.write(st.session_state['summary'])
    st.page_link('pages/summary.py', label='Re-Generate Summary', icon='📝')
