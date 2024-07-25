import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/Login.css';
import Banner from '../Home/Banner';
import Footer from '../Home/Footer';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5001/api/auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (response.ok) {
        // Store token in localStorage or a cookie
        localStorage.setItem('token', data.token);
        navigate('/');
      } else {
        setError(data.msg || 'Login failed');
      }
    } catch (error) {
      setError('Server error');
    }
  };

  return (
    <div className='Login'>
      <Banner />
      <h2>Login</h2>
      <div className='form-container'>
        <form onSubmit={handleLogin} className='smaller-container'>
          <input
            type="email"
            placeholder="Email"
            value={email}
            className='form-input'
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            className='form-input'
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit" className='button'>Login</button>
        </form>
        {error && <p className='error-message'>{error}</p>}
        <p className='App-link'>Not registered yet? <span onClick={() => navigate('/signup')}>Sign up</span></p>
      </div>
      <Footer />
    </div>
  );
};

export default Login;
