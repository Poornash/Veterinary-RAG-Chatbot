import streamlit as st
from backend.rag import load_chat_history
from backend.db import get_db_connection

# ---------------------------------------------------------
# PAGE PROTECTION
# ---------------------------------------------------------
if "is_authenticated" not in st.session_state or st.session_state["is_authenticated"] is False:
    st.error("You must log in to access your chat history.")
    st.stop()

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="History - Vet RAG Bot", page_icon="🐾")

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
    <h2 style="text-align:center; color:#4A4A4A;">📜 Your Chat History</h2>
    <p style="text-align:center; color:#777;">Review your past Q/A sessions with VetBot.</p>
    <br>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LOAD USER HISTORY
# ---------------------------------------------------------
rows = load_chat_history(st.session_state["user_id"])

if len(rows) == 0:
    st.info("No chat history yet.")
else:
    # ---------------------------------------------------------
    # TIMELINE STYLE UI
    # ---------------------------------------------------------
    st.markdown("""
        <style>
            .timeline {
                border-left: 3px solid #4A90E2;
                margin-left: 20px;
                padding-left: 20px;
            }
            .timeline-item {
                margin-bottom: 30px;
                position: relative;
            }
            .timeline-item:before {
                content: '';
                position: absolute;
                left: -11px;
                top: 4px;
                width: 15px;
                height: 15px;
                background-color: #4A90E2;
                border-radius: 50%;
            }
            .card {
                background-color: #F7F9FC;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
            }
            .timestamp {
                color: #888;
                font-size: 12px;
                margin-bottom: 6px;
            }
            .question {
                font-weight: bold;
                color: #333;
            }
            .answer {
                color: #444;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='timeline'>", unsafe_allow_html=True)

    for chat in rows:
        question = chat["question"]
        answer = chat["answer"]
        timestamp = chat["timestamp"]

        st.markdown(
            f"""
            <div class="timeline-item">
                <div class="card">
                    <div class="timestamp">🕒 {timestamp}</div>
                    <div class="question">❓ {question}</div>
                    <br>
                    <div class="answer">💬 {answer}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# CLEAR HISTORY OPTION
# ---------------------------------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("Delete All History", use_container_width=True):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM history WHERE user_id = ?", (st.session_state["user_id"],))
    conn.commit()
    conn.close()

    if "messages" in st.session_state:
        st.session_state.messages = []

    st.success("All history deleted!")
    st.rerun()



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
