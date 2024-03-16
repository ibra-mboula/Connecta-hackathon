const express = require('express');
const { MongoClient, ServerApiVersion } = require('mongodb');

const app = express();
const port = 3000;

const uri = "mongodb+srv://52676:yNHdKFyn3tPVtptZ@cluster0.kswno1o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

const client = new MongoClient(uri, {
  serverApi: ServerApiVersion.v1 
});

app.use(express.static('public'));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/views/home.html');
});

app.get('/forum', (req, res) => {
  res.sendFile(__dirname + '/views/forum.html');
});

app.get('/carte', (req, res) => {
  res.sendFile(__dirname + '/views/carte.html');
});

async function run() {
  try {
    await client.connect();
    console.log("Connected successfully to MongoDB");

    const database = client.db('hack_data');
    const collection = database.collection('data');

    await collection.insertOne({ message: "Initialization document.." });

    app.listen(port, () => {
      console.log(`Server is running on http://localhost:${port}`);
    });

  } catch (e) {
    console.error(e);
  } finally {
    // Uncomment the following line if you want to close the database connection after the server stops
    // await client.close();
  }
}

run().catch(console.dir);
