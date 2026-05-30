from __future__ import annotations

from dataclasses import dataclass, field
import json
from queue import Queue
from threading import Thread
from typing import Optional

import websocket


@dataclass
class NodeClient:
    name: str
    url: str = "ws://localhost:8000/ws"
    messages: Queue[str] = field(default_factory=Queue)
    errors: Queue[str] = field(default_factory=Queue)
    _socket: Optional[websocket.WebSocketApp] = field(default=None, init=False)
    _thread: Optional[Thread] = field(default=None, init=False)

    def connect(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        self._socket = websocket.WebSocketApp(
            self.url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self._thread = Thread(target=self._socket.run_forever, daemon=True)
        self._thread.start()

    def send(self, message: str) -> None:
        if not self._socket:
            self.errors.put("node is not connected")
            return

        self._socket.send(json.dumps({"sender": self.name, "content": message}))

    def close(self) -> None:
        if self._socket:
            self._socket.close()

    def drain_messages(self) -> list[str]:
        return self._drain(self.messages)

    def drain_errors(self) -> list[str]:
        return self._drain(self.errors)

    def _on_open(self, ws: websocket.WebSocketApp) -> None:
        self.messages.put(f"{self.name} connected")

    def _on_message(self, ws: websocket.WebSocketApp, message: str) -> None:
        self.messages.put(message)

    def _on_error(self, ws: websocket.WebSocketApp, error: Exception) -> None:
        self.errors.put(str(error))

    def _on_close(
        self,
        ws: websocket.WebSocketApp,
        close_status_code: int | None,
        close_msg: str | None,
    ) -> None:
        self.messages.put(f"{self.name} disconnected")

    @staticmethod
    def _drain(queue: Queue[str]) -> list[str]:
        items: list[str] = []
        while not queue.empty():
            items.append(queue.get())
        return items
