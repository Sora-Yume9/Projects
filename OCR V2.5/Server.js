const express = require("express");
const bodyParser = require("body-parser");
const http = require("http");
const socketIo = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

const port = 3000;
let TextTransfer = "";

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/Speak.html");
});


io.on("connect", (socket) => {
  socket.on("transferControl", (data) => {
    let postData = data.message;
    TextTransfer = postData;
    if (TextTransfer != "") {
      console.log(TextTransfer);
      io.emit("eventHorizon", { message: TextTransfer });
      TextTransfer = "";
    }
  });
});

server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
  console.log("Server is listening");
});
