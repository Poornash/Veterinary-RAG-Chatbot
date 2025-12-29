import streamlit as st

# ---------------------------------------------------------
# INITIAL SESSION SETUP
# ---------------------------------------------------------
def init_session():
    if "is_authenticated" not in st.session_state:
        st.session_state["is_authenticated"] = False
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    if "user_name" not in st.session_state:
        st.session_state["user_name"] = "Guest"
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = ""

init_session()

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="PawMedBot",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# FIXED APP TITLE (TOP-LEFT, ON ALL PAGES)
# ---------------------------------------------------------
st.markdown("""
    <style>
        .fixed-title {
            position: fixed;
            top: 12px;
            left: 20px;
            font-size: 22px;
            font-weight: 700;
            z-index: 9999;
        }
    </style>

    <div class="fixed-title">🐾 PawMedBot</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# FIXED PROFILE BOX (BOTTOM-LEFT, ON ALL PAGES)
# ---------------------------------------------------------
profile_box_html = f"""
    <style>
        .profile-box {{
            position: fixed;
            bottom: 25px;
            left: 20px;
            width: 180px;
            background: #222;
            padding: 12px 14px;
            border-radius: 12px;
            color: white;
            font-size: 15px;
            z-index: 9999;
            box-shadow: 0px 0px 6px rgba(0,0,0,0.35);
        }}
    </style>

    <div class="profile-box">
        👤 <b>{st.session_state['user_name']}</b>
    </div>
"""

st.markdown(profile_box_html, unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR (COLLAPSIBLE) — NAVIGATION MENU
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 🐾 Navigation")

    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/1_login.py", label="🔐 Login")
    st.page_link("pages/2_signup.py", label="📝 Signup")
    st.page_link("pages/4_chat.py", label="💬 Chat")
    st.page_link("pages/3_profile.py", label="👤 Profile")
    st.page_link("pages/5_histroy.py", label="📜 History")


# ---------------------------------------------------------
# HOME PAGE CONTENT
# ---------------------------------------------------------
st.write("")  
st.write("")  
st.markdown("""
    <h1 style="text-align:center; color:#444;">🐾 Welcome to PawMedBot</h1>
    <p style="text-align:center; font-size:18px; color:#666;">
        Your Offline Veterinary Assistant — Fast, Accurate & Private  
        <br><br>
        Use the menu on the left to Login, Signup, or Start Chatting!
    </p>
""", unsafe_allow_html=True)
