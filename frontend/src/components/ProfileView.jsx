import React, { useEffect, useState } from 'react';
import { profileApi } from '../api';

const ACTIVITY_OPTIONS = [
  { value: 'sedentary', label: 'Sedentary (little or no exercise)' },
  { value: 'lightly_active', label: 'Lightly active (1–3 days/week)' },
  { value: 'moderately_active', label: 'Moderately active (3–5 days/week)' },
  { value: 'active', label: 'Active (6–7 days/week)' },
  { value: 'very_active', label: 'Very active (intense daily exercise)' },
];

export default function ProfileView({ onSessionExpired }) {
  const [savedProfile, setSavedProfile] = useState(null);
  const [ageYears, setAgeYears] = useState('');
  const [sex, setSex] = useState('');
  const [activityLevel, setActivityLevel] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  async function loadProfile() {
    setLoading(true);
    setError('');
    try {
      const data = await profileApi.get();
      setSavedProfile(data);
      setAgeYears(data.age_years != null ? String(data.age_years) : '');
      setSex(data.sex_for_equation || '');
      setActivityLevel(data.activity_level || '');
    } catch (e) {
      if (e.status === 401) {
        onSessionExpired();
        return;
      }
      setError(e.message || 'Unable to load profile.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProfile();
  }, []);

  async function handleSave(event) {
    event.preventDefault();
    if (saving) return;
    setError('');
    setMessage('');

    if (ageYears.trim() === '' || !sex || !activityLevel) {
      setError('All three fields (age, sex, and activity level) are required.');
      return;
    }

    const parsedAge = Number(ageYears);
    if (!Number.isInteger(parsedAge) || parsedAge < 19 || parsedAge > 78) {
      setError('Age must be a whole number between 19 and 78.');
      return;
    }

    setSaving(true);
    try {
      const updated = await profileApi.update({
        age_years: parsedAge,
        sex_for_equation: sex,
        activity_level: activityLevel,
      });
      setSavedProfile(updated);
      setMessage('Profile saved. Refresh the page to verify persistence.');
    } catch (e) {
      if (e.status === 401) {
        onSessionExpired();
        return;
      }
      setError(e.message || 'Unable to save profile.');
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return <p role="status">Loading profile…</p>;
  }

  const hasSaved = savedProfile && savedProfile.updated_at !== null;

  return (
    <div className="layout">
      <section className="entry" aria-labelledby="profile-form-title">
        <h2 id="profile-form-title">Health profile</h2>
        <form onSubmit={handleSave} noValidate>
          <label htmlFor="age_years">Age <span>years (19–78)</span></label>
          <input
            id="age_years"
            type="number"
            min="19"
            max="78"
            step="1"
            placeholder="For example, 25"
            value={ageYears}
            onChange={(e) => setAgeYears(e.target.value)}
            disabled={saving}
          />

          <label htmlFor="sex_for_equation">Sex (for TDEE equation)</label>
          <select
            id="sex_for_equation"
            value={sex}
            onChange={(e) => setSex(e.target.value)}
            disabled={saving}
          >
            <option value="">-- Select sex --</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>

          <label htmlFor="activity_level">Activity level</label>
          <select
            id="activity_level"
            value={activityLevel}
            onChange={(e) => setActivityLevel(e.target.value)}
            disabled={saving}
          >
            <option value="">-- Select activity level --</option>
            {ACTIVITY_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>

          <button type="submit" disabled={saving}>
            {saving ? 'Saving…' : 'Save profile'}
          </button>
        </form>

        {error && <p role="alert" className="error">{error}</p>}
        {message && <p role="status" className="success">{message}</p>}
      </section>

      <section aria-labelledby="profile-summary-title">
        <div className="section-heading">
          <h2 id="profile-summary-title">Saved profile</h2>
          <button type="button" className="secondary" onClick={loadProfile} disabled={saving}>
            Reload
          </button>
        </div>

        {!hasSaved ? (
          <p className="empty">Your profile is not set yet. Complete the form to enable TDEE calculations.</p>
        ) : (
          <dl className="profile-summary">
            <div><dt>Age</dt><dd>{savedProfile.age_years} years</dd></div>
            <div><dt>Sex</dt><dd>{savedProfile.sex_for_equation}</dd></div>
            <div>
              <dt>Activity level</dt>
              <dd>{ACTIVITY_OPTIONS.find((o) => o.value === savedProfile.activity_level)?.label || savedProfile.activity_level}</dd>
            </div>
            <div><dt>Last updated</dt><dd>{new Date(savedProfile.updated_at).toLocaleString('en-GB')}</dd></div>
          </dl>
        )}
      </section>
    </div>
  );
}