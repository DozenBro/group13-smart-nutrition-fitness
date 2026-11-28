import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { authApi, clearToken, getToken } from './api';
import AuthView from './components/AuthView';
import ProfileView from './components/ProfileView';
import MeasurementsView from './components/MeasurementsView';
import WorkoutsView from './components/WorkoutsView';
import FoodsView from './components/FoodsView';
import AdminView from './components/AdminView';
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
      setActiveTab('measurements');
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
            <span className="user-email">{user.email} ({user.role})</span>
            <button type="button" className="secondary" onClick={handleLogout} disabled={loggingOut}>
              {loggingOut ? 'Logging out…' : 'Log out'}
            </button>
          </div>
        )}
      </header>

      {checkingAuth ? (
        <p role="status">Checking session…</p>
      ) : !user ? (
        <AuthView onLoginSuccess={(u) => { setUser(u); setActiveTab('measurements'); }} />
      ) : (
        <>
          <nav className="nav-tabs" aria-label="Main navigation">
            <button
              type="button"
              className={activeTab === 'measurements' ? 'tab active' : 'tab'}
              onClick={() => setActiveTab('measurements')}
            >
              Dashboard & history
            </button>
            <button
              type="button"
              className={activeTab === 'profile' ? 'tab active' : 'tab'}
              onClick={() => setActiveTab('profile')}
            >
              Health profile
            </button>
            <button
              type="button"
              className={activeTab === 'workouts' ? 'tab active' : 'tab'}
              onClick={() => setActiveTab('workouts')}
            >
              Workout planner
            </button>
            <button
              type="button"
              className={activeTab === 'foods' ? 'tab active' : 'tab'}
              onClick={() => setActiveTab('foods')}
            >
              Foods
            </button>
            {user.role === 'admin' && (
              <button
                type="button"
                className={activeTab === 'admin' ? 'tab active' : 'tab'}
                onClick={() => setActiveTab('admin')}
              >
                Admin
              </button>
            )}
          </nav>

          {activeTab === 'measurements' && (
            <MeasurementsView
              onSessionExpired={handleSessionExpired}
              onGoToProfile={() => setActiveTab('profile')}
            />
          )}
          {activeTab === 'profile' && (
            <ProfileView onSessionExpired={handleSessionExpired} />
          )}
          {activeTab === 'workouts' && (
            <WorkoutsView user={user} />
          )}
          {activeTab === 'foods' && (
            <FoodsView />
          )}
          {activeTab === 'admin' && user.role === 'admin' && (
            <AdminView currentUser={user} onSessionExpired={handleSessionExpired} />
          )}
        </>
      )}
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);