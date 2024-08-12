const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();

// CORS configuration
const corsOptions = {
  origin: process.env.NODE_ENV === 'production' ? false : 'http://localhost:3000',
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));
app.use(express.json());

const INFERENCE_URL = process.env.INFERENCE_URL || 'https://lexcelerate-inference-rn3lkigvjq-as.a.run.app';

app.post('/api/query', async (req, res) => {
  const { query } = req.body;
  try {
    console.log('INFERENCE_URL:', INFERENCE_URL);
    console.log('Sending request to Python server...');
    const response = await axios.post(`${INFERENCE_URL}/api/query`, { query });
    console.log('Received response from Python server:', response.data);
    res.json(response.data);
  } catch (error) {
    console.error('Error details:', error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
    } else if (error.request) {
      console.error('No response received');
    }
    res.status(500).json({ error: 'An error occurred while processing the query' });
  }
});

const PORT = process.env.PORT || 5000;

const path = require('path');

// Serve static files from the React app
app.use(express.static(path.join(__dirname, '../client/build')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
});
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
