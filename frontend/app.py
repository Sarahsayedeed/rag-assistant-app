import streamlit as st
from api_client import ask, check_health

st.set_page_config(page_title="RAG Document Assistant", page_icon="📚")

st.title("RAG Document Assistant")

# Sidebar for health status
st.sidebar.title("System Status")
health = check_health()
if health.get("status") == "healthy":
    st.sidebar.success("Backend API is Online")
else:
    st.sidebar.error("Backend API is Offline")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.write(f"- {source}")

# React to user input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask(prompt)
            
            if "error" in response:
                st.error(response["error"])
                st.session_state.messages.append({"role": "assistant", "content": response["error"]})
            else:
                answer = response.get("answer", "No answer found.")
                sources = response.get("sources", [])
                
                st.markdown(answer)
                if sources:
                    with st.expander("Sources"):
                        for source in sources:
                            st.write(f"- {source}")
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "sources": sources
                })
