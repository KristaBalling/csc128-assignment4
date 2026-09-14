"""
CSC-128 Assignment 4: Streamlit interface
Krista Balling
"""

import streamlit as st
from booking import handle

st.title("Study Room Reservation Bot")

if "slots" not in st.session_state:
    st.session_state.slots = {
        "day": None,
        "time": None,
        "party_size": None,
        "room": None
    }

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I can help you book a study room. What day do you need it?"
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_text = st.chat_input("Type your message")

if user_text:
    st.session_state.messages.append({
        "role": "user",
        "content": user_text
    })

    response, st.session_state.slots = handle(
        user_text,
        st.session_state.slots
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()