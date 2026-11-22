import React, { useEffect, useState } from 'react';
import { healthApi, measurementApi } from '../api';
import HistoryChart from './HistoryChart';

const FIELD_LABELS = {
  age_years: 'Age (19–78)',
  sex_for_equation: 'Sex',
  activity_level: 'Activity level',
};

export default function MeasurementsView({ onSessionExpired, onGoToProfile }) {
  const [rows, setRows] = useState([]);
  const [estimate, setEstimate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [weight, setWeight] = useState('');
  const [height, setHeight] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  async function loadDashboard() {
    setLoading(true);
    setError('');
    try {
      const [historyData, estimateData] = await Promise.all([
        measurementApi.list(),
        healthApi.estimate(),
      ]);
      setRows(historyData);
      setEstimate(estimateData);
    } catch (e) {
      if (e.status === 401) {
        onSessionExpired();
        return;
      }
      setError(e.message || 'Unable to connect to the server.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

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
      const row = await measurementApi.create(Number(weight), Number(height));
      setRows((previous) => [row, ...previous].slice(0, 30));
      setMessage('Measurement saved. Dashboard updated.');
      setWeight('');
      const updatedEstimate = await healthApi.estimate();
      setEstimate(updatedEstimate);
    } catch (e) {
      if (e.status === 401) {
        onSessionExpired();
        return;
      }
      setError(e.message || 'Unable to save the measurement.');
    } finally {
      setSaving(false);
    }
  }

  const missingLabels = (estimate?.tdee_missing_fields || []).map(
    (f) => FIELD_LABELS[f] || f
  );

  return (
    <div className="layout">
      <section className="entry" aria-labelledby="entry-title">
        <h2 id="entry-title">New measurement</h2>
        <form onSubmit={save} noValidate>
          <label htmlFor="weight">Weight <span>kg</span></label>
          <input
            id="weight"
            type="number"
            inputMode="decimal"
            step="0.01"
            placeholder="For example, 70"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            disabled={saving}
          />
          <label htmlFor="height">Height <span>cm</span></label>
          <input
            id="height"
            type="number"
            inputMode="decimal"
            step="0.01"
            placeholder="For example, 175"
            value={height}
            onChange={(e) => setHeight(e.target.value)}
            disabled={saving}
          />
          <button type="submit" disabled={saving || loading}>
            {saving ? 'Saving…' : 'Save measurement'}
          </button>
        </form>
        {error && <p role="alert" className="error">{error}</p>}
        {message && <p role="status" className="success">{message}</p>}
      </section>

      <section aria-labelledby="history-title">
        <div className="section-heading">
          <h2 id="history-title">Health dashboard & history</h2>
          <button type="button" className="secondary" onClick={loadDashboard} disabled={loading || saving}>
            Reload
          </button>
        </div>

        {loading ? (
          <p role="status">Loading dashboard…</p>
        ) : (
          <>
            <div className="metrics-grid">
              <div className="metric-card">
                <span className="metric-label">Latest BMI</span>
                {estimate?.bmi != null ? (
                  <>
                    <strong className="metric-value">{estimate.bmi.toFixed(2)}</strong>
                    <span className="metric-sub">kg / m²</span>
                  </>
                ) : (
                  <p className="empty">Record your first measurement to see BMI.</p>
                )}
              </div>

              <div className="metric-card">
                <span className="metric-label">Estimated TDEE</span>
                {estimate?.tdee != null ? (
                  <>
                    <strong className="metric-value">{estimate.tdee.toFixed(2)} kcal/day</strong>
                    <span className="metric-sub">Daily energy expenditure estimate</span>
                  </>
                ) : estimate?.measurement_id == null ? (
                  <p className="empty">Record your first measurement first.</p>
                ) : (
                  <div className="missing-prompt">
                    <p className="empty">
                      TDEE unavailable. Complete your profile:{' '}
                      <strong>{missingLabels.join(', ') || 'required fields'}</strong>.
                    </p>
                    <button type="button" className="secondary" onClick={onGoToProfile}>
                      Go to Health profile
                    </button>
                  </div>
                )}
              </div>
            </div>

            <HistoryChart rows={rows} />

            {rows.length === 0 ? (
              <p className="empty">No measurements yet. Add your first record.</p>
            ) : (
              <div className="table-scroll">
                <table>
                  <caption>The 30 most recent records, newest first.</caption>
                  <thead>
                    <tr><th>Recorded at</th><th>kg</th><th>cm</th><th>BMI</th></tr>
                  </thead>
                  <tbody>
                    {rows.map((row) => (
                      <tr key={row.id}>
                        <td>{new Date(row.created_at).toLocaleString('en-GB')}</td>
                        <td>{row.weight_kg}</td>
                        <td>{row.height_cm}</td>
                        <td>{row.bmi.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}
      </section>
    </div>
  );
}