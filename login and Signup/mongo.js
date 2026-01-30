const express = require('express');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const port = 3000;
const bodyParser = require('body-parser');
app.use(bodyParser.json());
const { MongoClient } = require('mongodb');

const uri = 'mongodb://localhost:27017';
const client = new MongoClient(uri);

async function connectToMongoDB() {
  try {
    await client.connect();
    console.log('Connected to MongoDB');
  } catch (error) {
    console.error('Error connecting to MongoDB:', error);
  }
}

connectToMongoDB();
app.get('/login', (req, res) => {
  res.sendFile(__dirname + '/login.html');
});
app.get('/Register', (req, res) => {
  res.sendFile(__dirname + '/signup.html');
});

http.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});


io.on('connection', (socket) => {
  console.log('A user connected');

  socket.on('disconnect', () => {
    console.log('User disconnected');
  });


  socket.on('signup', async ({ email, password }) => {
    const query = { password, email };

    const db = client.db("Logins");
    const collection = db.collection("Accounts");
    const existingData = await collection.findOne(query);

    try {
      if (existingData) {
        socket.emit('signupResult', { message: 'Account already exists' });
      } else {
        const result = await collection.insertOne({ password, email });

        
        socket.emit('signupResult', { message: 'Account created' });
      }
    } catch (error) {
      console.error('Error storing or checking data in MongoDB:', error);
      socket.emit('signupResult', { error: 'Internal Server Error' });
    }
  });

 
  socket.on('login', async ({ loginEmail, loginPassword }) => {
    const query = { password: loginPassword, email: loginEmail };

    const db = client.db("Logins");
    const collection = db.collection("Accounts");
    const existingData = await collection.findOne(query);

    try {
      if (existingData) {
       
        socket.emit('loginResult', { message: 'yes' });
      } else {
        socket.emit('loginResult', { message: 'Account does not exist' });
      }
    } catch (error) {
      console.error('Error storing or checking data in MongoDB:', error);
      socket.emit('loginResult', { error: 'Internal Server Error' });
    }
  });
});
