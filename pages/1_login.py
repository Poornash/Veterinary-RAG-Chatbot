import streamlit as st
from backend.auth import login_user

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Login - Vet RAG Bot", page_icon="🐾")
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


# If already logged in, redirect
if "is_authenticated" in st.session_state and st.session_state["is_authenticated"]:
    st.switch_page("pages/4_Chat.py")




# ---------------------------------------------------------
# LOGIN UI
# ---------------------------------------------------------
st.markdown("""
    <h2 style="text-align:center; color:#4A4A4A;">🐾 Vet RAG Bot – Login</h2>
    <p style="text-align:center; color:#777;">Welcome back! Please log in to continue.</p>
""", unsafe_allow_html=True)

# Centered container
with st.container():
    st.write("")
    st.write("")

    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    login_btn = st.button("Login", use_container_width=True)

# ---------------------------------------------------------
# LOGIN LOGIC
# ---------------------------------------------------------
if login_btn:
    if email.strip() == "" or password.strip() == "":
        st.error("Please fill all fields.")
    else:
        success, result = login_user(email, password)

        if success:
            user = result

            # Save session details
            st.session_state["is_authenticated"] = True
            st.session_state["user_id"] = user["id"]
            st.session_state["user_name"] = user["name"]
            st.session_state["user_email"] = user["email"]

            st.success("Login successful! Redirecting...")
            st.rerun()

        else:
            st.error(result)


# ---------------------------------------------------------
# SIGNUP LINK
# ---------------------------------------------------------
st.markdown("""
    <p style="text-align:center; margin-top:20px;">
        Don't have an account?
        <a href='/2_Signup' target='_self'>Sign up</a>
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
