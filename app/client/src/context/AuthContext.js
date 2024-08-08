import React, { createContext, useReducer } from 'react';
import axios from 'axios';

const AuthContext = createContext();

const authReducer = (state, action) => {
  switch (action.type) {
    case 'LOGIN_SUCCESS':
      localStorage.setItem('token', action.payload.token);
      return { ...state, ...action.payload, isAuthenticated: true };
    case 'LOGOUT':
      localStorage.removeItem('token');
      return { ...state, token: null, isAuthenticated: false };
    default:
      return state;
  }
};

const AuthProvider = ({ children }) => {
  const initialState = { token: localStorage.getItem('token'), isAuthenticated: null };
  const [state, dispatch] = useReducer(authReducer, initialState);

  const login = async (formData) => {
    const res = await axios.post('/api/auth', formData);
    dispatch({ type: 'LOGIN_SUCCESS', payload: res.data });
  };

  const logout = () => {
    dispatch({ type: 'LOGOUT' });
  };

  return (
    <AuthContext.Provider value={{ ...state, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthProvider, AuthContext };
