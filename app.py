import uuid
import streamlit as st
import html2text
import requests
from bs4 import BeautifulSoup
import st_pages

import auth

st.set_page_config(page_title="Gino", page_icon="🌎")

if not auth.login():
    st.stop()

st.markdown('<style>a[data-testid="stPageLink-NavLink"]{border-style: solid; border-width: 2px; border-color: grey;}</style>', unsafe_allow_html=True)

st_pages.show_pages([
    st_pages.Page('app.py', 'Capture Anything', '🏠'),
    st_pages.Page('pages/studio.py', 'Studio', '📝'),
    st_pages.Page('pages/summary.py', 'Summary', '📝'),
    st_pages.Page('pages/podcast.py', 'Podcast', '📝'),
    st_pages.Page('pages/askme.py', 'Askme', '📝'),
    # st_pages.Page('pages/askme.py', 'Ask Me', '📝'),
    # st_pages.Page('pages/mindbase.py', 'Mind Base', '📝'),
    #st_pages.Section('Interview')
])

#st_pages.hide_pages(["Studio"])


if 'url' not in st.session_state:
    st.session_state.url = ''

if 'captures' not in st.session_state:
    st.session_state.captures = []

def on_click():
    st.session_state.url = st.session_state.widget
    st.session_state.widget = ''



st.header("Capture Anything")

notification = st.empty()

st.text_input("Paste link", key="widget", on_change=on_click)
#resume = st.file_uploader('Pictures')
if st.button("Capture"):
    data = {}
    data['id'] = uuid.uuid4()
    data['metadata'] = {}
    data['content'] = ''

    url = st.session_state.url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data['metadata']['title'] = soup.select('head meta[property="og:title"]')[0]['content']
    data['metadata']['description'] = soup.select('head meta[property="og:description"]')[0]['content']
    data['metadata']['image'] = soup.select('head meta[property="og:image"]')[0]['content']
    data['content'] = html2text.html2text(response.text)

    st.session_state.captures.append(data)

    st.write(data)
    col1, col2 = notification.columns([0.8, 0.2])
    col1.success('This is a success message!', icon="✅")
    col2.page_link('pages/studio.py', label='Go to Studio', icon='📝')
