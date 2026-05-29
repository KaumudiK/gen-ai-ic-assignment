import streamlit as st
from rag_engine import RAGEngine

st.set_page_config(
    page_title="Acme Tech HR Assistant",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Acme Tech HR Assistant")
st.markdown(
    "Ask questions about company policies, leave, work from home, "
    "or employee benefits. I'll find answers from the official documents."
)


@st.cache_resource
def load_rag_engine():
    engine = RAGEngine(documents_path='documents')
    engine.build_index()
    return engine


with st.sidebar:
    st.header("About")
    st.write("This assistant uses 4 company documents:")
    st.markdown("- Company Policies")
    st.markdown("- Leave Policy")
    st.markdown("- Work From Home Policy")
    st.markdown("- Employee Benefits")

    st.divider()
    st.subheader("Try asking:")
    sample_questions = [
        "How many vacation days do I get?",
        "What's the work from home policy?",
        "How much is the wellness allowance?",
        "What's the notice period for resignation?",
        "Can I get reimbursed for online courses?",
        "When are performance reviews?",
    ]
    for q in sample_questions:
        st.markdown(f"- {q}")

    st.divider()
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()


with st.spinner("Loading knowledge base..."):
    engine = load_rag_engine()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "Hi! I'm the Acme Tech HR Assistant. "
                    "Ask me anything about company policies, leave, "
                    "WFH, or benefits."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            response = engine.generate_answer(user_input, top_k=3)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})