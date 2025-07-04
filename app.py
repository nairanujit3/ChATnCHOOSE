import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from chatbot_core import ask_bot

# --- Page configuration ---
st.set_page_config(
    page_title="🛍️ PriceWise Assistant",
    layout="centered",
    page_icon="🛒"
)

# --- Mobile-first responsive styling ---
st.markdown("""
    <style>
    /* Common chat bubble style */
    .stChatMessage {
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        word-wrap: break-word;
        max-width: 100%;
    }
    .stChatMessage.user {
        background-color: #f0f2f6;
        color: #000;
    }
    .stChatMessage.assistant {
        background-color: #e8f5e9;
        color: #2e7d32;
    }

    /* Improve message spacing on mobile */
    @media only screen and (max-width: 600px) {
        .stChatMessage {
            font-size: 1rem;
            padding: 0.8rem;
        }
    }

    /* Make input container mobile-friendly */
    .stChatInputContainer {
        background-color: #fff;
        padding-top: 1rem;
    }

    /* Hide Streamlit's default fullscreen header on mobile */
    header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Header content ---
st.title("🛍️ PriceWise Assistant")
st.caption("Compare. Decide. Save — the smart way 🧠💰")

# --- Initialize chat history ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Show previous chat messages ---
for msg in st.session_state.chat_history:
    with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
        if isinstance(msg, HumanMessage):
            st.markdown(f"🧑‍💻 **You:** {msg.content}", unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
            st.markdown(f"🤖 **PriceWise:** {msg.content}", unsafe_allow_html=True)

# --- Input box ---
prompt = st.chat_input("🔍 What product would you like to compare today?")

if prompt:
    # Display user's prompt
    with st.chat_message("user"):
        st.markdown(f" {prompt}", unsafe_allow_html=True)

    # Call bot and update state
    response, updated_history = ask_bot(prompt, st.session_state.chat_history)
    st.session_state.chat_history = updated_history

    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(f" {response}", unsafe_allow_html=True)
