const WebSocket = require('ws');

const url = 'ws://127.0.0.1:8000/ws';

const ws = new WebSocket(url);

ws.on('open', function open() {
  console.log('WebSocket connection opened');
  ws.send('Hello, server!');
});

ws.on('message', function message(data) {
  console.log(`Received: ${data}`);
});

ws.on('close', function close(code, reason) {
  console.log(`WebSocket connection closed with code: ${code}, reason: ${reason}`);
});

ws.on('error', function error(err) {
  console.error(`WebSocket error: ${err.message}`);
});