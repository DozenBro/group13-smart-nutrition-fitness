import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

async function request(path, options) {
  const response = await fetch(path, options);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    if (Array.isArray(body.detail)) {
      const field = body.detail[0]?.loc?.at(-1);
      throw new Error(field === 'weight_kg'
        ? 'Weight must be greater than 0 and no more than 500 kg, with up to 2 decimal places.'
        : 'Height must be between 50 and 250 cm, with up to 2 decimal places.');
    }
    throw new Error(body.detail || 'The request failed. Please try again.');
  }
  return response.json();
}

function App() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [weight, setWeight] = useState('');
  const [height, setHeight] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  async function loadHistory() {
    setLoading(true);
    setError('');
    try {
      setRows(await request('/api/measurements'));
    } catch (e) {
      setError(e.message || 'Unable to connect to the server.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { loadHistory(); }, []);

  async function save(event) {
    event.preventDefault();
    if (saving) return;
    setMessage('');
    setError('');
    if (weight.trim() === '' || height.trim() === '') {
      setError('Enter both weight and height.');
      return;
    }
    setSaving(true);
    try {
      const row = await request('/api/measurements', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ weight_kg: Number(weight), height_cm: Number(height) }),
      });
      setRows(previous => [row, ...previous].slice(0, 30));
      setMessage('Measurement saved. You can refresh the page to check it.');
      setWeight('');
    } catch (e) {
      setError(e.message || 'Unable to save the measurement.');
    } finally {
      setSaving(false);
    }
  }

  const latest = rows[0];
  return (
    <main>
      <header>
        <p className="eyebrow">GROUP 13 · SMART NUTRITION & FITNESS</p>
        <h1>Body measurements</h1>
        <p>Record your weight and height, and review your history.</p>
      </header>
      <p className="notice">Practice demo with fictional data. Account features are in development.</p>
      <div className="layout">
        <section className="entry" aria-labelledby="entry-title">
          <h2 id="entry-title">New measurement</h2>
          <form onSubmit={save} noValidate>
            <label htmlFor="weight">Weight <span>kg</span></label>
            <input id="weight" type="number" inputMode="decimal" step="0.01" placeholder="For example, 70" value={weight} onChange={e => setWeight(e.target.value)} disabled={saving} />
            <label htmlFor="height">Height <span>cm</span></label>
            <input id="height" type="number" inputMode="decimal" step="0.01" placeholder="For example, 175" value={height} onChange={e => setHeight(e.target.value)} disabled={saving} />
            <button type="submit" disabled={saving || loading}>{saving ? 'Saving…' : 'Save measurement'}</button>
          </form>
          {error && <p role="alert" className="error">{error}</p>}
          {message && <p role="status" className="success">{message}</p>}
        </section>
        <section aria-labelledby="history-title">
          <div className="section-heading">
            <h2 id="history-title">Recent history</h2>
            <button className="secondary" onClick={loadHistory} disabled={loading || saving}>Reload</button>
          </div>
          {latest && <p className="latest">Latest BMI <strong>{latest.bmi.toFixed(2)}</strong><span>BMI = weight in kg / (height in metres)²</span></p>}
          {loading ? <p role="status">Loading history…</p> : rows.length === 0 ? <p className="empty">No measurements yet. Add your first record.</p> :
            <div className="table-scroll"><table>
              <caption>The 30 most recent records, newest first.</caption>
              <thead><tr><th>Recorded at</th><th>kg</th><th>cm</th><th>BMI</th></tr></thead>
              <tbody>{rows.map(row => <tr key={row.id}>
                <td>{new Date(row.created_at).toLocaleString('en-GB')}</td>
                <td>{row.weight_kg}</td><td>{row.height_cm}</td><td>{row.bmi.toFixed(2)}</td>
              </tr>)}</tbody>
            </table></div>}
        </section>
      </div>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);

