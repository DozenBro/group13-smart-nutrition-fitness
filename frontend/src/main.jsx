import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { authApi, clearToken, getToken } from './api';
import AuthView from './components/AuthView';
import ProfileView from './components/ProfileView';
import MeasurementsView from './components/MeasurementsView';
import './style.css';

function App() {
  const [user, setUser] = useState(null);
  const [checkingAuth, setCheckingAuth] = useState(true);
  const [activeTab, setActiveTab] = useState('measurements');
  const [loggingOut, setLoggingOut] = useState(false);

  useEffect(() => {
    async function checkSession() {
      if (!getToken()) {
        setCheckingAuth(false);
        return;
      }
      try {
        const me = await authApi.me();
        setUser(me);
      } catch {
        clearToken();
        setUser(null);
      } finally {
        setCheckingAuth(false);
      }
    }
    checkSession();
  }, []);

  function handleSessionExpired() {
    clearToken();
    setUser(null);
  }

  async function handleLogout() {
    if (loggingOut) return;
    setLoggingOut(true);
    try {
      await authApi.logout();
    } catch {
      // Token may already be expired or revoked
    } finally {
      clearToken();
      setUser(null);
      setLoggingOut(false);
    }
  }

  return (
    <main>
      <header className="top-header">
        <div>
          <p className="eyebrow">GROUP 13 · SMART NUTRITION & FITNESS</p>
          <h1>Smart Nutrition & Fitness</h1>
        </div>
        {user && (
          <div className="user-bar">
            <span className="user-email">{user.email}</span>
            <button type="button" className="secondary" onClick={handleLogout} disabled={loggingOut}>
              {loggingOut ? 'Logging out…' : 'Log out'}
            </button>
          </div>
        )}
      </header>

      {checkingAuth ? (
        <p role="status">Checking session…</p>
      ) : !user ? (
        <AuthView onLoginSuccess={(u) => { setUser(u); setActiveTab('profile'); }} />
      ) : (
        <>
          <nav className="nav-tabs" aria-label="Main navigation">
            <button
              type="button"
              className={activeTab === 'measurements' ? 'tab active' : 'tab'}
              onClick={() => setActiveTab('measurements')}
            >
              Body measurements
            </button>
            <button
              type="button"
              className={activeTab === 'profile' ? 'tab active' : 'tab'}
              onClick={() => setActiveTab('profile')}
            >
              Health profile
            </button>
          </nav>

          {activeTab === 'measurements' ? (
            <MeasurementsView onSessionExpired={handleSessionExpired} />
          ) : (
            <ProfileView onSessionExpired={handleSessionExpired} />
          )}
        </>
      )}
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);