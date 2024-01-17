const WebSocket = require('ws');

const server = new WebSocket.Server({ port: 3000 });

server.on('connection', ws => {
    console.log('Client connected');

    ws.on('message', message => {
        console.log(`Received: ${message}`);

        // Broadcast the message to all connected clients
        server.clients.forEach(client => {
            if (client !== ws && client.readyState === WebSocket.OPEN) {
                client.send(message);
            }
        });
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

console.log('Server started on ws:http://172.232.21.168:3000');
