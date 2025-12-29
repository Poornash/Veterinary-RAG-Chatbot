import streamlit as st
from backend.auth import get_user_by_id, update_user_name, change_password

# ---------------------------------------------------------
# PAGE PROTECTION
# ---------------------------------------------------------
if "is_authenticated" not in st.session_state or st.session_state["is_authenticated"] is False:
    st.error("You must log in to view this page.")
    st.stop()

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Profile - Vet RAG Bot", page_icon="🐾")
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


st.markdown("""
    <h2 style="text-align:center; color:#4A4A4A;">🐾 Your Profile</h2>
    <p style="text-align:center; color:#777;">Manage your account and security settings.</p>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# FETCH USER DETAILS
# ---------------------------------------------------------
user = get_user_by_id(st.session_state["user_id"])

if not user:
    st.error("User not found.")
    st.stop()

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["👤 Profile Information", "🔒 Change Password"])


# ---------------------------------------------------------
# TAB 1 — PROFILE INFORMATION
# ---------------------------------------------------------
with tab1:
    st.subheader("Your Account Details")

    st.write(f"**Name:** {user['name']}")
    st.write(f"**Email:** {user['email']}")
    st.write(f"**Joined On:** {user['created_at']}")

    st.divider()

    st.subheader("Update Name")

    new_name = st.text_input("Enter new name", value=user["name"])
    
    if st.button("Update Name", use_container_width=True):
        if new_name.strip() == "":
            st.error("Name cannot be empty.")
        else:
            success, msg = update_user_name(user["id"], new_name)
            st.session_state["user_name"] = new_name
            st.success(msg)
            st.rerun()


# ---------------------------------------------------------
# TAB 2 — CHANGE PASSWORD
# ---------------------------------------------------------
with tab2:
    st.subheader("Change Your Password")

    old_password = st.text_input("Old Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_new_password = st.text_input("Confirm New Password", type="password")

    if st.button("Update Password", use_container_width=True):
        if new_password != confirm_new_password:
            st.error("New passwords do not match!")
        elif old_password.strip() == "" or new_password.strip() == "":
            st.error("Please fill all fields.")
        else:
            success, message = change_password(user["id"], old_password, new_password)

            if success:
                st.success(message)
            else:
                st.error(message)


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
