import streamlit as st
from backend.rag import get_rag_response, save_chat_history, load_chat_history

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


# -----------------------------
# Session Setup
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_authenticated" not in st.session_state or not st.session_state.is_authenticated:
    st.error("Please login first.")
    st.stop()

user_id = st.session_state["user_id"]

if "history_loaded" not in st.session_state:
    st.session_state.history_loaded = False

# -----------------------------
# QUICK EXIT WORDS
# -----------------------------
goodbye_triggers = [
    "ok", "okay", "okay done", "done", "thank you",
    "thanks", "bye", "ok bye", "okay thank you"
]

# -----------------------------
# Non-Pet Topic Blocker (FAST)
# -----------------------------
non_pet_keywords = [
    "capital", "president", "math", "country", "physics",
    "chemistry", "france", "india", "history",
    "human anatomy", "human brain", "computer", "machine"
]


def is_non_pet_question(q):
    q = q.lower()
    return any(word in q for word in non_pet_keywords)


# -----------------------------
# ChatGPT-style Bubble UI
# -----------------------------
def user_bubble(msg):
    st.markdown(
        f"""
        <div style='text-align: right; margin: 10px;'>
            <div style="
                display: inline-block;
                background: #4F8BF9;
                color: white;
                padding: 10px 15px;
                border-radius: 14px;
                max-width: 70%;
                font-size: 15px;">
                {msg}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def bot_bubble(msg):
    st.markdown(
        f"""
        <div style='text-align: left; margin: 10px;'>
            <div style="
                display: inline-block;
                background: #EDEDED;
                color: black;
                padding: 10px 15px;
                border-radius: 14px;
                max-width: 70%;
                font-size: 15px;">
                {msg}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Build Conversational Context
# -----------------------------
def build_chat_context(messages, limit=4):
    """
    Builds recent conversation context for follow-up questions
    """
    history = []
    for role, msg in messages[-limit*2:]:
        prefix = "User" if role == "user" else "Assistant"
        history.append(f"{prefix}: {msg}")
    return "\n".join(history)

# -----------------------------
# Load Previous History
# -----------------------------
if not st.session_state.history_loaded:
    past_messages = load_chat_history(user_id)

    for q, a, t in past_messages:
        st.session_state.messages.append(("user", q))
        st.session_state.messages.append(("bot", a))

    st.session_state.history_loaded = True


# -----------------------------
# Header
# -----------------------------
st.title("🐾 VetBot — Chat with the Veterinary Assistant")


# -----------------------------
# Render stored messages
# -----------------------------
for sender, msg in st.session_state.messages:
    if sender == "user":
        user_bubble(msg)
    else:
        bot_bubble(msg)

# -----------------------------
# User Input
# -----------------------------
user_input = st.chat_input("Ask something about your pet...")

if user_input:
    # Show user's message
    st.session_state.messages.append(("user", user_input))
    user_bubble(user_input)

    lower = user_input.lower().strip()

    # FAST greeting response (no LLM, instant)
    # FAST greeting response (flexible)
    greeting_triggers = ["hi", "hello", "hey", "hai"]

    if any(lower.startswith(greet) for greet in greeting_triggers):
        reply = "Hi! How can I help with your pet today? 🐾"
        bot_bubble(reply)
        st.session_state.messages.append(("bot", reply))
        save_chat_history(user_id, user_input, reply)
        st.stop()

    # FAST help / confusion handling
    help_triggers = ["help", "help please", "please help", "i need help"]

    if any(trigger in lower for trigger in help_triggers):
        reply = (
            "I'm here to help 🐾\n\n"
            "Please tell me what’s happening with your pet — "
            "for example symptoms, behavior changes, or concerns."
        )
        bot_bubble(reply)
        st.session_state.messages.append(("bot", reply))
        save_chat_history(user_id, user_input, reply)
        st.stop()


    # FAST Goodbye logic
    if any(trigger in lower for trigger in goodbye_triggers):
        goodbye_reply = "I'm glad I could help. Take good care of your pet — feel free to ask anytime! 🐾"
        bot_bubble(goodbye_reply)
        st.session_state.messages.append(("bot", goodbye_reply))
        save_chat_history(user_id, user_input, goodbye_reply)
        st.stop()

    # FAST non-pet rejection
    if is_non_pet_question(lower):
        reply = "This question is not related to pets or veterinary topics, so I cannot answer it."
        bot_bubble(reply)
        st.session_state.messages.append(("bot", reply))
        save_chat_history(user_id, user_input, reply)
        st.stop()

    # NORMAL RAG + Phi-3 response WITH CONTEXT
    chat_context = build_chat_context(st.session_state.messages)
    combined_query = f"""
    Previous conversation:
    {chat_context}

    Current question:
    {user_input}
    """

    with st.spinner("🐾 VetBot is thinking..."):
        bot_reply, _ = get_rag_response(combined_query)

    bot_bubble(bot_reply)


    # Save message + history
    st.session_state.messages.append(("bot", bot_reply))
    save_chat_history(user_id, user_input, bot_reply)


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
