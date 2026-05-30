import { Server as HttpServer } from 'http';
import WebSocket, { WebSocketServer } from 'ws';

const IS_ALIVE = Symbol('isAlive');

export class ConnectionManager {
  private clients = new Set<WebSocket>();

  addClient(ws: WebSocket) {
    this.clients.add(ws);
    console.log(`Client added. Total clients: ${this.clients.size}`);
  }

  removeClient(ws: WebSocket) {
    this.clients.delete(ws);
    console.log(`Client removed. Total clients: ${this.clients.size}`);
  }

  broadcast(message: string, sender: WebSocket | null = null) {
    this.clients.forEach((client) => {
      if (client !== sender && client.readyState === WebSocket.OPEN) {
        try {
          client.send(message);
        } catch (error) {
          console.error('Error broadcasting to client:', error);
          this.removeClient(client);
        }
      }
    });
  }

  getClientCount() {
    return this.clients.size;
  }
}

export function setupWebSocket(server: HttpServer): WebSocketServer {
  const connectionManager = new ConnectionManager();
  const wss = new WebSocketServer({ server, clientTracking: true });

  wss.on('connection', function connection(ws: WebSocket & { [key: symbol]: boolean }, request) {
    const clientIP = request.socket.remoteAddress;
    console.log(`New client connection from ${clientIP}`);

    connectionManager.addClient(ws);
    ws.send(`Welcome! There are ${connectionManager.getClientCount()} clients connected.`);
    connectionManager.broadcast(`A new user joined the chat!`);


    ws.on('message', function message(data) {
      try {
        const messageText = data.toString();
        console.log('Received: ', messageText);
        connectionManager.broadcast(messageText);
      } catch (error) {
        console.error('Error processing message: ', error);
      }
    });


    ws.on('close', function close(code, reason) {
      connectionManager.removeClient(ws);
      connectionManager.broadcast(`A user left the chat`);
      console.log(`Client disconnected - Code: ${code}\nReason: ${reason}`);
    });


    ws.on('error', function error(err) {
      console.error('websocket error: ', err);
    });


    ws[IS_ALIVE] = true;
    ws.on('pong', function heartbeat() {
      ws[IS_ALIVE] = true;
    });
  });


  type WebSocketWithAlive = WebSocket & { [key: symbol]: boolean };
  const interval = setInterval(function ping() {
    wss.clients.forEach(function each(ws: WebSocket) {
      const ext = ws as WebSocketWithAlive;
      if (ext[IS_ALIVE] === false) {
        return ws.terminate();
      }
      ext[IS_ALIVE] = false;
      ws.ping();
    });
  }, 30000);

  wss.on('close', function close() {
    clearInterval(interval);
  });

  return wss;
}
