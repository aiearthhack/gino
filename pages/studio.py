import streamlit as st

st.set_page_config(layout="wide")

st.title("Studio")

st.markdown('<style>a[data-testid="stPageLink-NavLink"]{border-style: solid; border-width: 2px; border-color: grey;}</style>', unsafe_allow_html=True)

if 'captures' not in st.session_state:
    st.write("No captures yet")

if 'captures' in st.session_state:
    with st.container(height=500):
        for capture in st.session_state.captures:
            col1, col2, col3 = st.columns([0.2, 0.2, 0.6])
            col1.image(capture['metadata']['image'])
            col2.write(capture['metadata']['title'])
            col3.write(capture['metadata']['description'])

    col1, col2 = st.columns(2)
    col1.page_link('pages/summary.py', label='Create Summary', icon='📝')
    col1.write("Grab the essence in seconds - get a quick & easy summary")
    col2.page_link('pages/podcast.py', label='Generate Podcast', icon='📝')
    col2.write("Transform your content into audio - listen on the go")