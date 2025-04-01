import streamlit as st

def show_message(msg, success=True):
    if success:
        st.success(msg)
    else:
        st.error(msg)
