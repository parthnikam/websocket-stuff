# Texting App

A small Streamlit texting app backed by a FastAPI websocket server and SQLite message storage.

## Features

1. FastAPI server with websocket support.
2. Streamlit UI for adding people and sending messages.
3. SQLite database for storing message history.
4. Broadcast updates to connected clients.

## Architecture

```text
+------------------+      websocket       +------------------+
|  Streamlit UI    | -------------------> |  FastAPI Server  |
| streamlit_app.py |                      |     main.py      |
+--------+---------+                      +--------+---------+
         |                                         |
         | imports                                 | uses
         |                                         |
+--------v---------+                      +--------v---------+
| WebSocket Client |                      | ConnectionManager|
|    client.py     |                      |  connections.py  |
+------------------+                      +--------+---------+
                                                   |
                                                   | stores / reads
                                                   |
                                         +---------v---------+
                                         | SQLite Database   |
                                         |   messages.db     |
                                         | via database.py   |
                                         +-------------------+
```

## Files

- `main.py`: FastAPI app, websocket endpoint, and message API.
- `streamlit_app.py`: Texting UI.
- `client.py`: WebSocket client used by Streamlit.
- `connections.py`: Active websocket connection manager.
- `database.py`: SQLite setup and message queries.
- `messages.db`: Local SQLite database created when the app runs.

## Setup

```bash
pip install -r requirements.txt
```

## Run the server

```bash
uvicorn main:app --reload --port 8000
```

## Run the UI

```bash
streamlit run streamlit_app.py
```
