import streamlit as st

from client import NodeClient
from database import create_message, init_db, list_messages


DEFAULT_WS_URL = "ws://localhost:8000/ws"


st.set_page_config(page_title="Texting App", layout="wide")
st.title("Texting App")
init_db()

if "nodes" not in st.session_state:
    st.session_state.nodes = {}

if "logs" not in st.session_state:
    st.session_state.logs = []


def add_node(name: str, url: str) -> None:
    node = NodeClient(name=name, url=url)
    node.connect()
    st.session_state.nodes[name] = node
    st.session_state.logs.append(f"created {name}")


with st.sidebar:
    st.header("Server")
    ws_url = st.text_input("WebSocket URL", value=DEFAULT_WS_URL)

    st.header("People")
    with st.form("add-node", clear_on_submit=True):
        node_name = st.text_input("Name", placeholder="Alex")
        submitted = st.form_submit_button("Add person")

    if submitted:
        cleaned_name = node_name.strip()
        if not cleaned_name:
            st.warning("Enter a name.")
        elif cleaned_name in st.session_state.nodes:
            st.warning("That person already exists.")
        else:
            add_node(cleaned_name, ws_url)
            st.rerun()

    if st.button("Refresh"):
        st.rerun()


for node in st.session_state.nodes.values():
    for message in node.drain_messages():
        st.session_state.logs.append(f"[{node.name}] {message}")
    for error in node.drain_errors():
        st.session_state.logs.append(f"[{node.name}] error: {error}")


left, right = st.columns([2, 1])

with left:
    st.subheader("Conversation")
    messages = list_messages()
    if messages:
        for message in messages:
            with st.chat_message(message["sender"]):
                st.write(message["content"])
                st.caption(message["created_at"])
    else:
        st.info("No messages yet.")

    st.subheader("Send a text")
    people = list(st.session_state.nodes.keys())
    if people:
        sender = st.selectbox("From", people)
    else:
        sender = st.text_input("From", placeholder="Alex")

    with st.form("send-message", clear_on_submit=True):
        content = st.text_area("Message", placeholder="Type a message...")
        sent = st.form_submit_button("Send")

    if sent:
        cleaned_sender = sender.strip()
        cleaned_content = content.strip()
        if not cleaned_sender:
            st.warning("Enter who the message is from.")
        elif not cleaned_content:
            st.warning("Enter a message.")
        else:
            create_message(cleaned_sender, cleaned_content)
            st.session_state.logs.append(f"saved message from {cleaned_sender}")
            st.rerun()

    if st.session_state.nodes:
        st.subheader("Connected people")
        for name, node in list(st.session_state.nodes.items()):
            if st.button("Disconnect", key=f"disconnect-{name}"):
                node.close()
                del st.session_state.nodes[name]
                st.session_state.logs.append(f"removed {name}")
                st.rerun()

with right:
    st.subheader("Event log")
    if st.session_state.logs:
        for entry in reversed(st.session_state.logs[-50:]):
            st.write(entry)
    else:
        st.caption("No events yet.")
