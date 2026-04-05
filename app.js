// app.js
const express = require('express');
const bodyParser = require('body-parser');
const db = require('./db'); // we will create this next

const app = express();
const PORT = 3000;

app.use(bodyParser.json());

// Test route
app.get('/', (req, res) => {
  res.send('Server is running!');
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});