import express from 'express';
import { createServer } from 'http';
import { setupWebSocket } from './websocket.ts';

const app = express();
const server = createServer(app);

app.use(express.static('public'));

const PORT = process.env.PORT || 8080;

setupWebSocket(server);

server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
