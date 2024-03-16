const express = require('express');
const app = express();
const port = 3000;

// Serveur les fichiers statiques du dossier public
app.use(express.static('public'));

// Route pour la page Home
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/views/home.html');
});

// Route pour la page Forum
app.get('/forum', (req, res) => {
  res.sendFile(__dirname + '/views/forum.html');
});

// Route pour la page Carte
app.get('/carte', (req, res) => {
  res.sendFile(__dirname + '/views/carte.html');
});

app.listen(port, () => {
  console.log(`Serveur démarré sur http://localhost:${port}`);
});
