const path = require("path");
const http = require("http");
const express = require("express");
const { Server } = require("socket.io");
const WebSocketClient = require("websocket").client;

const app = express();
const server = http.createServer(app);
const io = new Server(server);
const client = new WebSocketClient();

const db = require("./db.js");
const socketModule = require("./sockets");

app.set("db", db);
app.set("currRecording", null);

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));
app.use(require("./routes"));

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/index.html");
});

client.on("connect", (connection) => {
    connection.on("message", (message) => {
        if (message.type === "utf8") {
            const content = JSON.parse(message.utf8Data);
            content.map((e) => {
                const coordRecord = {
                    lat: e.lat,
                    lon: e.lon,
                    heading: e.heading,
                    boatName: e.name,
                    recordId: app.get("currRecording"),
                };
                db.insertCoordinate(coordRecord);
            });
            const isRecording =
                app.get("currRecording") === null ? false : true;
            content.map((e) => {
                e["isRecording"] = isRecording;
            });
            io.emit("newCoord", content);
        }
    });
});
client.connect("ws://127.0.0.1:25000");

const onConnection = (socket) => {
    socketModule.getCurrentRecordings(io, app);
};

io.on("connection", onConnection);

server.listen(process.env.PORT || 3000, () => {
    console.log(`listening on *:${server.address().port}`);
});
