const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const { initDB } = require('./models');
const userRoute = require('./routes/users');
const authRoute = require('./routes/auth');

dotenv.config();

const app = express();

// Connect Database
initDB();

// Enable CORS
app.use(cors());

// Init Middleware
app.use(express.json());

// Define Routes
app.use('/api/users', userRoute);
app.use('/api/auth', authRoute);

const PORT = process.env.PORT || 5001;

app.listen(PORT, () => console.log(`Server started on port ${PORT}`));
