const express = require("express");
const bodyParser = require("body-parser");
const http = require("http");
const socketIo = require("socket.io");
const app = express();
const server = http.createServer(app);
const io = socketIo(server);
const port = 5000;
let TextTransfer = "";

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/model.html");
});


io.on("connect", (socket) => {
  socket.on("Prediction", (data) => {
   let pre = data.message
   io.emit("Token", { message: pre });

  });
});


server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
  console.log("Server is listening");
});