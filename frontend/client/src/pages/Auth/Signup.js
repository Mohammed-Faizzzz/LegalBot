import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/Signup.css';
import Banner from '../Home/Banner';
import Footer from '../Home/Footer';

const Signup = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
  
    try {
      const response = await fetch('http://localhost:5001/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username,
          email,
          password,
        })
      });
  
      const data = await response.json();
  
      if (response.ok) {
        // Store token in localStorage or a cookie
        localStorage.setItem('token', data.token);
        navigate('/');
      } else {
        setError(data.msg || 'Signup failed');
      }
    } catch (error) {
      console.error('Error during signup:', error);
      setError('Server error');
    }
  };  

  return (
    <div className='Signup'>
      <Banner />
      <h2>Sign Up</h2>
      <div className='form-container'>
        <form onSubmit={handleSignup} className='smaller-container'>
          <input
            type="text"
            placeholder="Username"
            value={username}
            className='form-input'
            onChange={(e) => setUsername(e.target.value)}
          />
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
          <input
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            className='form-input'
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          <button type="submit" className='button'>Sign Up</button>
        </form>
      </div>
      {error && <p className='error-message'>{error}</p>}
      <Footer />
    </div>
  );
};

export default Signup;
