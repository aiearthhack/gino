import streamlit as st
import extra_streamlit_components as stx

user_database = [
    {
        'username': 'admin',
        'password': 'admin'
    }
]

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

def login():
    value = cookie_manager.get(cookie='username')
    
    if value:
        st.sidebar.write(f"Hello, {value}")
        if st.sidebar.button("Logout"):
            cookie_manager.delete('username')
            value = None
        return True

    if not value:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if any(user['username'] == username and user['password'] == password for user in user_database):
                cookie_manager.set('username', username)
                value = cookie_manager.get(cookie='username')
                st.write(value)
                return True
            else:
                st.error("Invalid credentials")
    return False