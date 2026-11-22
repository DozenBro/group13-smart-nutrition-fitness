import React, { useEffect, useState } from 'react';
import { adminApi } from '../api';

export default function AdminView({ currentUser, onSessionExpired }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState(null);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  async function loadUsers() {
    setLoading(true);
    setError('');
    try {
      setUsers(await adminApi.listUsers());
    } catch (e) {
      if (e.status === 401) {
        onSessionExpired();
        return;
      }
      setError(e.message || 'Unable to load accounts.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadUsers();
  }, []);

  async function toggleLock(target) {
    if (busyId !== null) return;
    setBusyId(target.id);
    setError('');
    setMessage('');
    try {
      const updated = target.is_locked
        ? await adminApi.unlockUser(target.id)
        : await adminApi.lockUser(target.id);
      setUsers((prev) => prev.map((u) => (u.id === updated.id ? updated : u)));
      setMessage(
        updated.is_locked
          ? `Locked account ${updated.email} and revoked active sessions.`
          : `Unlocked account ${updated.email}.`
      );
    } catch (e) {
      if (e.status === 401) {
        onSessionExpired();
        return;
      }
      setError(e.message || 'Unable to update account status.');
    } finally {
      setBusyId(null);
    }
  }

  return (
    <section aria-labelledby="admin-title">
      <div className="section-heading">
        <h2 id="admin-title">Account administration</h2>
        <button type="button" className="secondary" onClick={loadUsers} disabled={loading || busyId !== null}>
          Reload
        </button>
      </div>

      {error && <p role="alert" className="error">{error}</p>}
      {message && <p role="status" className="success">{message}</p>}

      {loading ? (
        <p role="status">Loading accounts…</p>
      ) : users.length === 0 ? (
        <p className="empty">No accounts found.</p>
      ) : (
        <div className="table-scroll">
          <table>
            <caption>Registered accounts ordered by ID.</caption>
            <thead>
              <tr>
                <th>ID</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
                <th>Created at</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => {
                const isSelf = currentUser && u.id === currentUser.id;
                return (
                  <tr key={u.id}>
                    <td>{u.id}</td>
                    <td>{u.email}</td>
                    <td>{u.role}</td>
                    <td>
                      <span className={u.is_locked ? 'badge locked' : 'badge active'}>
                        {u.is_locked ? 'Locked' : 'Active'}
                      </span>
                    </td>
                    <td>{new Date(u.created_at).toLocaleString('en-GB')}</td>
                    <td>
                      <button
                        type="button"
                        className="secondary"
                        disabled={busyId !== null || isSelf}
                        title={isSelf ? 'Cannot lock your own account' : ''}
                        onClick={() => toggleLock(u)}
                      >
                        {busyId === u.id
                          ? 'Updating…'
                          : u.is_locked
                            ? 'Unlock'
                            : 'Lock'}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}