import React, { useEffect, useState } from 'react';
import { foodApi } from '../api';

const EMPTY_FORM = {
  name: '',
  portion_desc: '',
  calories: '',
  protein_g: '',
  carbs_g: '',
  fat_g: '',
  price_vnd: '',
  meal_slot: 'lunch',
  preference_tags: '',
  nutrition_source: '',
  price_source: '',
};

export default function FoodsView() {
  const [foods, setFoods] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  // Filters
  const [mealSlot, setMealSlot] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [tag, setTag] = useState('');

  // Create form
  const [form, setForm] = useState(EMPTY_FORM);

  async function loadFoods(overrides = null) {
    setLoading(true);
    setError('');
    const params = overrides || {
      meal_slot: mealSlot.trim(),
      max_price_vnd: maxPrice.trim(),
      tag: tag.trim(),
    };
    try {
      setFoods(await foodApi.list(params));
    } catch (e) {
      setError(e.message || 'Unable to load food list.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadFoods();
  }, []);

  function updateField(key, value) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  async function handleFilter(event) {
    event.preventDefault();
    loadFoods();
  }

  function handleResetFilters() {
    setMealSlot('');
    setMaxPrice('');
    setTag('');
    loadFoods({ meal_slot: '', max_price_vnd: '', tag: '' });
  }

  async function handleCreate(event) {
    event.preventDefault();
    if (saving) return;
    setError('');
    setMessage('');

    const required = [
      'name', 'portion_desc', 'calories', 'protein_g', 'carbs_g',
      'fat_g', 'price_vnd', 'meal_slot', 'nutrition_source', 'price_source',
    ];
    for (const key of required) {
      if (String(form[key]).trim() === '') {
        setError(`Please fill in "${key.replace('_', ' ')}".`);
        return;
      }
    }

    setSaving(true);
    try {
      const payload = {
        name: form.name.trim(),
        portion_desc: form.portion_desc.trim(),
        calories: Number(form.calories),
        protein_g: Number(form.protein_g),
        carbs_g: Number(form.carbs_g),
        fat_g: Number(form.fat_g),
        price_vnd: parseInt(form.price_vnd, 10),
        meal_slot: form.meal_slot.trim(),
        preference_tags: form.preference_tags.trim() || null,
        nutrition_source: form.nutrition_source.trim(),
        price_source: form.price_source.trim(),
      };
      const created = await foodApi.create(payload);
      setFoods((prev) => [...prev, created].sort((a, b) => a.name.localeCompare(b.name)));
      setForm(EMPTY_FORM);
      setMessage(`Added "${created.name}".`);
    } catch (e) {
      setError(e.message || 'Unable to add food item.');
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(item) {
    if (deletingId !== null) return;
    setDeletingId(item.id);
    setError('');
    setMessage('');
    try {
      await foodApi.remove(item.id);
      setFoods((prev) => prev.filter((f) => f.id !== item.id));
      setMessage(`Removed "${item.name}".`);
    } catch (e) {
      setError(e.message || 'Unable to remove food item.');
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <div className="layout">
      <section className="entry" aria-labelledby="food-entry-title">
        <h2 id="food-entry-title">Add food item</h2>
        <form onSubmit={handleCreate} noValidate>
          <label htmlFor="food-name">Food name</label>
          <input
            id="food-name"
            placeholder="e.g. Pho ga"
            value={form.name}
            onChange={(e) => updateField('name', e.target.value)}
            disabled={saving}
          />

          <label htmlFor="food-portion">Portion description</label>
          <input
            id="food-portion"
            placeholder="e.g. 1 medium bowl (450g)"
            value={form.portion_desc}
            onChange={(e) => updateField('portion_desc', e.target.value)}
            disabled={saving}
          />

          <div className="form-grid-2">
            <div>
              <label htmlFor="food-cal">Calories <span>kcal</span></label>
              <input
                id="food-cal"
                type="number"
                step="0.01"
                value={form.calories}
                onChange={(e) => updateField('calories', e.target.value)}
                disabled={saving}
              />
            </div>
            <div>
              <label htmlFor="food-price">Price <span>VND</span></label>
              <input
                id="food-price"
                type="number"
                step="1000"
                value={form.price_vnd}
                onChange={(e) => updateField('price_vnd', e.target.value)}
                disabled={saving}
              />
            </div>
          </div>

          <div className="form-grid-3">
            <div>
              <label htmlFor="food-pro">Protein <span>g</span></label>
              <input
                id="food-pro"
                type="number"
                step="0.1"
                value={form.protein_g}
                onChange={(e) => updateField('protein_g', e.target.value)}
                disabled={saving}
              />
            </div>
            <div>
              <label htmlFor="food-carb">Carbs <span>g</span></label>
              <input
                id="food-carb"
                type="number"
                step="0.1"
                value={form.carbs_g}
                onChange={(e) => updateField('carbs_g', e.target.value)}
                disabled={saving}
              />
            </div>
            <div>
              <label htmlFor="food-fat">Fat <span>g</span></label>
              <input
                id="food-fat"
                type="number"
                step="0.1"
                value={form.fat_g}
                onChange={(e) => updateField('fat_g', e.target.value)}
                disabled={saving}
              />
            </div>
          </div>

          <label htmlFor="food-slot">Meal slot</label>
          <input
            id="food-slot"
            placeholder="breakfast / lunch / dinner / snack"
            value={form.meal_slot}
            onChange={(e) => updateField('meal_slot', e.target.value)}
            disabled={saving}
          />

          <label htmlFor="food-tags">Preference tags (optional)</label>
          <input
            id="food-tags"
            placeholder="e.g. high_protein, vietnamese"
            value={form.preference_tags}
            onChange={(e) => updateField('preference_tags', e.target.value)}
            disabled={saving}
          />

          <label htmlFor="food-nsrc">Nutrition source</label>
          <input
            id="food-nsrc"
            placeholder="e.g. NIN Vietnam Food Composition Table"
            value={form.nutrition_source}
            onChange={(e) => updateField('nutrition_source', e.target.value)}
            disabled={saving}
          />

          <label htmlFor="food-psrc">Price source</label>
          <input
            id="food-psrc"
            placeholder="e.g. Hanoi local market 2026"
            value={form.price_source}
            onChange={(e) => updateField('price_source', e.target.value)}
            disabled={saving}
          />

          <button type="submit" disabled={saving}>
            {saving ? 'Adding…' : 'Add food'}
          </button>
        </form>
        {error && <p role="alert" className="error">{error}</p>}
        {message && <p role="status" className="success">{message}</p>}
      </section>

      <section aria-labelledby="food-list-title">
        <div className="section-heading">
          <h2 id="food-list-title">Food catalog ({foods.length})</h2>
        </div>

        <form className="filter-bar" onSubmit={handleFilter}>
          <input
            placeholder="Meal slot (e.g. lunch)"
            value={mealSlot}
            onChange={(e) => setMealSlot(e.target.value)}
          />
          <input
            type="number"
            placeholder="Max price (VND)"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
          />
          <input
            placeholder="Tag (e.g. vegetarian)"
            value={tag}
            onChange={(e) => setTag(e.target.value)}
          />
          <button type="submit" className="secondary" disabled={loading}>Filter</button>
          <button type="button" className="secondary" onClick={handleResetFilters} disabled={loading}>
            Reset
          </button>
        </form>

        {loading ? (
          <p role="status">Loading foods…</p>
        ) : foods.length === 0 ? (
          <p className="empty">No foods found.</p>
        ) : (
          <div className="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>Name & portion</th>
                  <th>Slot</th>
                  <th>Kcal</th>
                  <th>P / C / F (g)</th>
                  <th>Price (VND)</th>
                  <th>Tags</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {foods.map((f) => (
                  <tr key={f.id}>
                    <td>
                      <strong>{f.name}</strong>
                      <div className="metric-sub">{f.portion_desc}</div>
                    </td>
                    <td>{f.meal_slot}</td>
                    <td>{f.calories}</td>
                    <td>{f.protein_g} / {f.carbs_g} / {f.fat_g}</td>
                    <td>{f.price_vnd.toLocaleString('en-US')}</td>
                    <td>{f.preference_tags || '—'}</td>
                    <td>
                      <button
                        type="button"
                        className="secondary"
                        disabled={deletingId !== null}
                        onClick={() => handleDelete(f)}
                      >
                        {deletingId === f.id ? 'Removing…' : 'Delete'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}