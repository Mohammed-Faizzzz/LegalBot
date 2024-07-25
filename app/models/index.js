const { Sequelize } = require('sequelize');
const UserModel = require('./User');
require('dotenv').config();

const sequelize = new Sequelize(process.env.POSTGRES_URI, {
  dialect: 'postgres',
  ssl: {
    rejectUnauthorized: false,
  },
});

const User = UserModel(sequelize, Sequelize);

const initDB = async () => {
  try {
    await sequelize.authenticate();
    console.log('Connection to the database has been established successfully.');

    await sequelize.sync({ force: true });
    console.log('All models were synchronized successfully.');
  } catch (error) {
    console.error('Unable to connect to the database:', error);
  }
};

module.exports = { User, initDB, sequelize };
