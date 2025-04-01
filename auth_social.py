import streamlit as st
from streamlit_auth0 import login_button

def social_login():
    st.header("🔓 Connexion via Google/Facebook")

    result = login_button(
        domain="dev-8n38ass0hnojrwub.us.auth0.com",
        client_id="ZZjKvVPjmE70uRIcQZtfuzwgcX4ZCzvP",
        redirect_uri="http://localhost:8501"
    )

    if result:
        st.success("✅ Connexion réussie via Google/Facebook")
        st.write("Bienvenue", result['userinfo']['name'])
        st.write("Email :", result['userinfo']['email'])

        st.session_state["user"] = (
            result['userinfo'].get("sub"),
            result['userinfo'].get("name"),
            result['userinfo'].get("email")
        )
        st.session_state["page"] = "Dashboard"
        st.rerun()
