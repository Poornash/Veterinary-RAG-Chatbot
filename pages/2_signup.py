import streamlit as st
from backend.auth import signup_user

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Signup - Vet RAG Bot", page_icon="🐾")

# If already logged in → redirect
if "is_authenticated" in st.session_state and st.session_state["is_authenticated"]:
    st.switch_page("pages/4_Chat.py")

# ---- FIXED APP TITLE (TOP-LEFT) ----
st.markdown("""
    <style>
        .fixed-title {
            position: fixed;
            top: 12px;
            left: 18px;
            font-size: 22px;
            font-weight: 700;
            z-index: 9999;
        }
    </style>

    <div class="fixed-title">🐾 PawMedBot</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIGNUP UI
# ---------------------------------------------------------
st.markdown("""
    <h2 style="text-align:center; color:#4A4A4A;">🐾 Create Your Vet RAG Bot Account</h2>
    <p style="text-align:center; color:#777;">Join us and start chatting with your AI Vet Assistant!</p>
""", unsafe_allow_html=True)

# Centered container
with st.container():
    st.write("")
    st.write("")

    name = st.text_input("Full Name", placeholder="Enter your name")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter a password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")

    signup_btn = st.button("Create Account", use_container_width=True)

# ---------------------------------------------------------
# SIGNUP LOGIC
# ---------------------------------------------------------
if signup_btn:
    if name.strip() == "" or email.strip() == "" or password.strip() == "" or confirm_password.strip() == "":
        st.error("Please fill all fields.")

    elif password != confirm_password:
        st.error("Passwords do not match!")

    else:
        success, message = signup_user(name, email, password)

        if success:
            st.success(message + " Redirecting to login...")
            st.rerun()

        else:
            st.error(message)


# ---------------------------------------------------------
# LOGIN LINK
# ---------------------------------------------------------
st.markdown("""
    <p style="text-align:center; margin-top:20px;">
        Already have an account?
        <a href='/1_Login' target='_self'>Login</a>
    </p>
""", unsafe_allow_html=True)


# ---- FLOATING PROFILE BADGE (BOTTOM-LEFT) ----
profile_name = st.session_state.get("user_name", "Guest")

st.markdown(f"""
    <style>
        .floating-profile {{
            position: fixed;
            bottom: 25px;
            left: 18px;
            background: rgba(255, 255, 255, 0.12);
            padding: 12px 16px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            color: white;
            font-size: 14px;
            box-shadow: 0 0 10px rgba(0,0,0,0.35);
            z-index: 9999;
        }}
    </style>

    <div class="floating-profile">
        <strong>👤 {profile_name}</strong><br>
        <span style="opacity:0.7; font-size:12px;">Logged In</span>
    </div>
""", unsafe_allow_html=True)
