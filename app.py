import streamlit as st
import cv2
import face_recognition

from database import init_db, get_all_users
from auth import register, login
from face_utils import (
    extract_face_descriptor,
    serialize_descriptor,
    deserialize_descriptor
)
from auth_social import social_login  



# --------------------------
# DASHBOARD après connexion
# --------------------------
def dashboard(user=None):
    st.title("👋 Bienvenue dans Projet de Zahia")

    if user:
        st.write(f"Utilisateur connecté : {user[1]} ({user[2]})")
    else:
        st.write("Vous êtes connecté.")

    if st.button("🔓 Se déconnecter"):
        st.session_state["user"] = None
        st.session_state["page"] = "Menu"
        st.rerun()

# --------------------------
# INSCRIPTION
# --------------------------
def inscription_page():
    st.header("👤 Inscription avec reconnaissance faciale")

    username = st.text_input("Nom d'utilisateur")
    email = st.text_input("Adresse email")
    password = st.text_input("Mot de passe", type="password")

    if st.button("📸 Capturer visage & S’inscrire"):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            st.error("❌ Erreur lors de la capture de l'image.")
            return

        st.image(frame, caption="📸 Image capturée", channels="BGR", use_column_width=True)

        descriptor = extract_face_descriptor(frame)

        if descriptor is None:
            st.warning("Aucun visage détecté. Veuillez réessayer.")
            return

        blob = serialize_descriptor(descriptor)

        try:
            register(username, email, password, blob)
            st.success("✅ Inscription réussie !")

            st.session_state["user"] = (None, username, email)
            st.session_state["page"] = "Dashboard"
            st.rerun()

        except Exception as e:
            st.error(f"Erreur : {e}")

# --------------------------
# CONNEXION CLASSIQUE
# --------------------------
def connexion_classique():
    st.header("🔑 Connexion classique")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        ok, user = login(email, password)
        if ok:
            st.success(f"✅ Bienvenue {user[1]}")
            st.session_state["user"] = user
            st.session_state["page"] = "Dashboard"
            st.rerun()
        else:
            st.error("❌ Email ou mot de passe incorrect.")

# --------------------------
# CONNEXION PAR VISAGE
# --------------------------
def connexion_par_visage():
    st.header("🔐 Connexion par reconnaissance faciale")

    if st.button("📷 Capturer & se connecter"):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            st.error("❌ Erreur de caméra.")
            return

        descriptor = extract_face_descriptor(frame)

        if descriptor is None:
            st.warning("Aucun visage détecté.")
            return

        users = get_all_users()
        if not users:
            st.warning("Aucun utilisateur enregistré.")
            return

        known_descriptors = []
        identities = []

        for user in users:
            blob = user[4]
            if blob:
                known = deserialize_descriptor(blob)
                known_descriptors.append(known)
                identities.append(user)

        if not known_descriptors:
            st.warning("Aucun encodage facial trouvé.")
            return

        distances = face_recognition.face_distance(known_descriptors, descriptor)
        min_distance = min(distances)
        min_index = distances.tolist().index(min_distance)

        if min_distance < 0.65:
            matched_user = identities[min_index]
            st.success(f"✅ Bienvenue {matched_user[1]}")
            st.session_state["user"] = matched_user
            st.session_state["page"] = "Dashboard"
            st.rerun()
        else:
            st.error("❌ Visage non reconnu.")

# --------------------------
# CONNEXION RÉSEAUX SOCIAUX (simulation)
# --------------------------
def social_login():
    st.header("🔓 Connexion via Google/Facebook")
    st.info("⚠️ Fonctionnalité en cours d'intégration. Connexion simulée.")

    if st.button("Se connecter avec Google ou Facebook"):
        st.success("✅ Connexion simulée réussie !")
        st.session_state["user"] = ("social_id", "Utilisateur Réseaux", "social@reseaux.com")
        st.session_state["page"] = "Dashboard"
        st.rerun()

# --------------------------
# MAIN STREAMLIT
# --------------------------
def main():
    st.set_page_config(page_title="ProjetZahia", page_icon="🤖", layout="centered")
    init_db()

    if "page" not in st.session_state:
        st.session_state["page"] = "Menu"
    if "user" not in st.session_state:
        st.session_state["user"] = None

    if st.session_state["page"] == "Menu":
        page = st.sidebar.selectbox("📋 Menu", [
            "Inscription",
            "Connexion classique",
            "Connexion par visage",
            "Connexion Google/Facebook"
        ])

        if page == "Inscription":
            inscription_page()
        elif page == "Connexion classique":
            connexion_classique()
        elif page == "Connexion par visage":
            connexion_par_visage()
        elif page == "Connexion Google/Facebook":
            social_login()

    elif st.session_state["page"] == "Dashboard":
        dashboard(st.session_state["user"])

if __name__ == "__main__":
    main()
