const http = require('http');

let app = http.createServer((req, res) => {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('hello world');
});

app.listen(3000, '127.0.0.1');
console.log('Node server running on port 3000');
