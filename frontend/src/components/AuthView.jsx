import React, { useState } from 'react';
import { authApi, setToken } from '../api';

export default function AuthView({ onLoginSuccess }) {
  const [mode, setMode] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  function switchMode(nextMode) {
    setMode(nextMode);
    setError('');
    setMessage('');
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (submitting) return;
    setError('');
    setMessage('');

    const cleanEmail = email.trim();
    if (!cleanEmail || !password) {
      setError('Please enter both email and password.');
      return;
    }
    if (mode === 'register' && (password.length < 8 || password.length > 128)) {
      setError('Password must be between 8 and 128 characters.');
      return;
    }

    setSubmitting(true);
    try {
      if (mode === 'register') {
        await authApi.register(cleanEmail, password);
        setMode('login');
        setPassword('');
        setMessage('Account created. Please log in with your credentials.');
      } else {
        const data = await authApi.login(cleanEmail, password);
        setToken(data.token);
        onLoginSuccess(data.user);
      }
    } catch (e) {
      setError(e.message || 'Authentication failed.');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="auth-card" aria-labelledby="auth-title">
      <div className="tabs">
        <button
          type="button"
          className={mode === 'login' ? 'tab active' : 'tab'}
          onClick={() => switchMode('login')}
          disabled={submitting}
        >
          Log in
        </button>
        <button
          type="button"
          className={mode === 'register' ? 'tab active' : 'tab'}
          onClick={() => switchMode('register')}
          disabled={submitting}
        >
          Register
        </button>
      </div>

      <h2 id="auth-title">{mode === 'login' ? 'Sign in to your account' : 'Create a member account'}</h2>

      <form onSubmit={handleSubmit} noValidate>
        <label htmlFor="auth-email">Email</label>
        <input
          id="auth-email"
          type="email"
          autoComplete="email"
          placeholder="alice@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={submitting}
        />

        <label htmlFor="auth-password">Password</label>
        <input
          id="auth-password"
          type="password"
          autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
          placeholder={mode === 'register' ? '8–128 characters' : 'Enter your password'}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={submitting}
        />

        <button type="submit" disabled={submitting}>
          {submitting
            ? mode === 'login' ? 'Signing in…' : 'Creating account…'
            : mode === 'login' ? 'Log in' : 'Register'}
        </button>
      </form>

      {error && <p role="alert" className="error">{error}</p>}
      {message && <p role="status" className="success">{message}</p>}
    </section>
  );
}