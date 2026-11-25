import React, { useEffect, useState } from 'react';
import { workoutApi } from '../api';

const GOAL_OPTIONS = [
  { value: 'weight_loss', label: 'Weight loss (4 sessions/week)' },
  { value: 'muscle_gain', label: 'Muscle gain (4 sessions/week)' },
  { value: 'maintenance', label: 'Maintenance (3 sessions/week)' },
];

export default function WorkoutsView({ user }) {
  const [plan, setPlan] = useState(null);
  const [streak, setStreak] = useState(null);
  const [goal, setGoal] = useState('weight_loss');
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [completingId, setCompletingId] = useState(null);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  // Exercise catalog preview
  const [categories, setCategories] = useState([]);
  const [exercises, setExercises] = useState([]);
  const [filterCat, setFilterCat] = useState('');
  const [showCatalog, setShowCatalog] = useState(false);

  async function loadWorkoutData() {
    setLoading(true);
    setError('');
    try {
      const [streakData, catData] = await Promise.all([
        workoutApi.getStreak(user),
        workoutApi.listCategories(user),
      ]);
      setStreak(streakData);
      setCategories(catData);

      try {
        const current = await workoutApi.getCurrentPlan(user);
        setPlan(current);
        setGoal(current.goal);
      } catch (e) {
        if (e.status === 404) {
          setPlan(null);
        } else {
          throw e;
        }
      }
    } catch (e) {
      setError(e.message || 'Unable to load workout data.');
    } finally {
      setLoading(false);
    }
  }

  async function loadExercises(categoryValue = filterCat) {
    try {
      const data = await workoutApi.listExercises(user, { category: categoryValue || undefined });
      setExercises(data);
    } catch (e) {
      setError(e.message || 'Unable to load exercises.');
    }
  }

  useEffect(() => {
    loadWorkoutData();
  }, [user.id]);

  useEffect(() => {
    if (showCatalog) {
      loadExercises(filterCat);
    }
  }, [showCatalog, filterCat]);

  async function handleGeneratePlan(event) {
    event.preventDefault();
    if (creating) return;
    setCreating(true);
    setError('');
    setMessage('');
    try {
      const created = await workoutApi.createPlan(user, goal);
      setPlan(created);
      setMessage(`Generated new ${goal.replace('_', ' ')} workout plan.`);
    } catch (e) {
      setError(e.message || 'Unable to generate workout plan.');
    } finally {
      setCreating(false);
    }
  }

  async function handleComplete(sessionId) {
    if (completingId !== null) return;
    setCompletingId(sessionId);
    setError('');
    setMessage('');
    try {
      const res = await workoutApi.completeSession(user, sessionId);
      setPlan((prev) =>
        prev
          ? {
              ...prev,
              sessions: prev.sessions.map((s) =>
                s.id === sessionId ? { ...s, completed: true } : s
              ),
            }
          : prev
      );
      setStreak((prev) => ({
        ...(prev || {}),
        current_streak: res.current_streak,
        active_today: res.active_today,
        last_active_date: res.activity_date,
      }));
      setMessage(
        res.already_completed
          ? 'Session was already marked complete.'
          : `Session completed! Current streak: ${res.current_streak} day(s).`
      );
    } catch (e) {
      setError(e.message || 'Unable to complete session.');
    } finally {
      setCompletingId(null);
    }
  }

  return (
    <div className="stack">
      <section className="metrics-grid" aria-label="Workout streak and generator">
        <div className="metric-card">
          <span className="metric-label">Current Streak</span>
          <strong className="metric-value">
            {streak ? `${streak.current_streak} day${streak.current_streak === 1 ? '' : 's'}` : '—'}
          </strong>
          <span className="metric-sub">
            {streak?.active_today
              ? 'Active today'
              : streak?.last_active_date
                ? `Last active: ${streak.last_active_date}`
                : 'Complete a session to start your streak'}
          </span>
        </div>

        <form className="metric-card" onSubmit={handleGeneratePlan}>
          <label htmlFor="workout-goal" className="metric-label">Workout Goal</label>
          <select
            id="workout-goal"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            disabled={creating}
          >
            {GOAL_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
          <button type="submit" disabled={creating || loading}>
            {creating ? 'Generating…' : plan ? 'Replace with new plan' : 'Generate workout plan'}
          </button>
        </form>
      </section>

      {error && <p role="alert" className="error">{error}</p>}
      {message && <p role="status" className="success">{message}</p>}

      <section aria-labelledby="plan-title">
        <div className="section-heading">
          <h2 id="plan-title">Active workout plan</h2>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              type="button"
              className="secondary"
              onClick={() => setShowCatalog((v) => !v)}
            >
              {showCatalog ? 'Hide exercise catalog' : 'Browse exercises'}
            </button>
            <button type="button" className="secondary" onClick={loadWorkoutData} disabled={loading}>
              Reload
            </button>
          </div>
        </div>

        {loading ? (
          <p role="status">Loading workout plan…</p>
        ) : !plan ? (
          <p className="empty">No active workout plan yet. Choose a goal above and click Generate.</p>
        ) : (
          <>
            <p className="metric-sub" style={{ marginBottom: '1rem' }}>
              <strong>Goal:</strong> {plan.goal.replace('_', ' ')} · <strong>Template:</strong> {plan.template}
            </p>
            <div className="sessions-grid">
              {plan.sessions.map((s) => (
                <article key={s.id} className="session-card">
                  <div className="section-heading">
                    <h3>Day {s.day_number} · {s.title}</h3>
                    {s.completed ? (
                      <span className="badge active">Completed</span>
                    ) : (
                      <button
                        type="button"
                        className="secondary"
                        disabled={completingId !== null}
                        onClick={() => handleComplete(s.id)}
                      >
                        {completingId === s.id ? 'Saving…' : 'Mark complete'}
                      </button>
                    )}
                  </div>
                  <ol className="exercise-list">
                    {s.items.map((item) => (
                      <li key={item.position}>
                        <div>
                          <strong>{item.exercise_name}</strong>{' '}
                          <span className="metric-sub">
                            — {item.sets} sets ×{' '}
                            {item.reps != null
                              ? `${item.reps} reps`
                              : `${item.duration_seconds}s`}{' '}
                            (rest {item.rest_seconds}s)
                          </span>
                        </div>
                        {item.instructions && (
                          <p className="metric-sub" style={{ margin: '0.2rem 0 0' }}>
                            {item.instructions}
                          </p>
                        )}
                      </li>
                    ))}
                  </ol>
                </article>
              ))}
            </div>
          </>
        )}
      </section>

      {showCatalog && (
        <section aria-labelledby="catalog-title" style={{ marginTop: '1.5rem' }}>
          <div className="section-heading">
            <h2 id="catalog-title">Approved exercise catalog</h2>
            <select
              aria-label="Filter by category"
              value={filterCat}
              onChange={(e) => setFilterCat(e.target.value)}
            >
              <option value="">All categories</option>
              {categories.map((c) => (
                <option key={c.id} value={c.name}>{c.name}</option>
              ))}
            </select>
          </div>
          {exercises.length === 0 ? (
            <p className="empty">No exercises match this filter.</p>
          ) : (
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Category</th>
                    <th>Difficulty</th>
                    <th>Equipment</th>
                    <th>Goals</th>
                  </tr>
                </thead>
                <tbody>
                  {exercises.map((ex) => (
                    <tr key={ex.id}>
                      <td>{ex.name}</td>
                      <td>{ex.category}</td>
                      <td>{ex.difficulty}</td>
                      <td>{ex.equipment}</td>
                      <td>{ex.goal_tags.join(', ')}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      )}
    </div>
  );
}