const express = require('express');
const { MongoClient, ServerApiVersion } = require('mongodb');
const path = require('path'); // Module pour manipuler les chemins de fichiers
const app = express();
const port = 3000;

// Mise à jour de l'URI pour utiliser MongoDB Atlas
//const uri = "mongodb+srv://52676:yNHdKFyn3tPVtptZ@cluster0.kswno1o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&ssl=true&authSource=admin";
const uri = "mongodb://127.0.0.1:27017";
const client = new MongoClient(uri);

app.set('view engine', 'ejs'); // Configuration du moteur de modèle EJS
app.set('views', path.join(__dirname, 'views')); // Spécification du répertoire des vues


app.use(express.json());
app.use(express.static('public'));
//app.use(express.static('views'));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/views/home.html');
});

app.get('/profil', (req, res) => {
  res.sendFile(__dirname + '/views/profil.html');
});

app.get('/forum', (req, res) => {
  res.sendFile(__dirname + '/views/forum.html');
});

app.get('/data', (req, res) => {
  res.sendFile(__dirname + '/views/data.html');
});

app.get('/api/data', async (req, res) => {
  try {
    await client.connect();
    const database = client.db('hack_data');
    const collection = database.collection('data2');
    const data = await collection.find({}).toArray();
    res.json(data);
  } catch (e) {
    res.status(500).send(e.message);
  }
});

app.get('/api/statistics', async (req, res) => {
  try {
    await client.connect();
    const database = client.db('hack_data');
    const collection = database.collection('data2');
    
    // Remplacez ceci par la logique appropriée pour récupérer et formater les données de votre collection
    const statistics = await collection.aggregate([
      { $group: { _id: "$arrondissement", count: { $sum: 1 } } }
    ]).toArray();

    res.json(statistics);
  } catch (e) {
    res.status(500).send(e.message);
  }
});

app.get('/carte', async (req, res) => {

  await client.connect();
  console.log("Connected successfully to MongoDB");

  const database = client.db('hack_data');
  const collection = database.collection('data2');

  data = await collection.find({}).toArray();

  data.forEach(element => {
    element.coord.long = parseFloat(element.coord.long)
    element.coord.lat = parseFloat(element.coord.lat)
  });

  commune_detected = {}

  data.forEach(element=>{
    if (element.commune in commune_detected){
      commune_detected[element.commune] += 1
    }else{
      commune_detected[element.commune] = 1
    }
  });

  data.forEach(item=>{
    if(item.commune in commune_detected){
      item.number = commune_detected[item.commune]
    }
  });

  res.render('carte', { data: data }); // Rendre la page carte.ejs
});

async function run() {
  try {
    await client.connect();
    console.log("Connected successfully to MongoDB");

    const database = client.db('hack_data');
    const collection = database.collection('data2');

    data_coord = await collection.find({}).toArray();
    

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

