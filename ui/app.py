"""
AgentDesk — Streamlit Web UI
Phase 3: Browser chat interface for Maya
"""

import os
import streamlit as st
import anthropic

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Omega Insurance Brokers LLC Support",
    page_icon="☕",
    layout="centered"
)

# ── Load FAQ ──────────────────────────────────────────────────────────────────
def load_faq(filepath):
    with open(filepath, "r") as f:
        return f.read()

# ── System prompt ─────────────────────────────────────────────────────────────
def build_system_prompt(faq_content):
    return f"""
You are Maya, the AI support assistant for Omega Insurance Brokers.

RULES:
- Answer ONLY from the knowledge base below. Never guess.
- Be warm, friendly and concise.
- If you cannot find the answer, say:
  "Let me connect you to our team."
  Then give the escalation contact from the knowledge base.

KNOWLEDGE BASE:
{faq_content}
"""

# ── App header ────────────────────────────────────────────────────────────────
st.title("Omega Insurance")
st.caption("Hi! I'm Maya, your support assistant. Ask me anything!")

# ── Load FAQ and client ───────────────────────────────────────────────────────
faq_content = load_faq("knowledge/test_clients/omega_insurance_faq.txt")
system_prompt = build_system_prompt(faq_content)
client        = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ── Session memory ────────────────────────────────────────────────────────────
# st.session_state persists across reruns — this is Streamlit's memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Display chat history ──────────────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Type your message here..."):

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add to memory
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Get Maya's response
    with st.chat_message("assistant"):
        with st.spinner("Maya is typing..."):
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=500,
                system=system_prompt,
                messages=st.session_state.messages
            )
            reply = response.content[0].text
            st.markdown(reply)

    # Add Maya's reply to memory
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })