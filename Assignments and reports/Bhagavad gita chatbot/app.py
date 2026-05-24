import streamlit as st
from chatbot import Chatbot
from knowledge_base import knowledge_base

st.set_page_config(
    page_title="Bhagavad Gita Guide",
    page_icon="🕉️",
    layout="centered"
)

st.title("🕉️ Bhagavad Gita Guide")
st.markdown(
    "Ask me about the teachings, characters, chapters, "
    "and timeless wisdom of the Bhagavad Gita."
)

with st.sidebar:
    st.header("About")
    st.write("A conversational guide to the wisdom of the Bhagavad Gita.")

    st.subheader("Try asking:")
    sample_questions = [
        "What is the Bhagavad Gita?",
        "Who is Krishna?",
        "What is karma yoga?",
        "What does Krishna say about death?",
        "What is dharma?",
        "How can the Gita help in daily life?",
        "What is the famous verse about action?",
    ]
    for q in sample_questions:
        st.markdown(f"- {q}")

    st.divider()
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = [
            {"role": "assistant",
             "content": "Namaste! I'm here to help you explore the wisdom of the Bhagavad Gita. What would you like to know?"}
        ]
        st.rerun()


@st.cache_resource
def load_chatbot():
    return Chatbot(knowledge_base)


bot = load_chatbot()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "Namaste! I'm here to help you explore the wisdom of the Bhagavad Gita. What would you like to know?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask about the Bhagavad Gita..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = bot.get_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
