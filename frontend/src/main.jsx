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
        ? 'Cân nặng phải lớn hơn 0 và không quá 500 kg, tối đa 2 chữ số thập phân.'
        : 'Chiều cao phải từ 50 đến 250 cm, tối đa 2 chữ số thập phân.');
    }
    throw new Error(body.detail || 'Yêu cầu chưa thành công. Hãy thử lại.');
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
      setError(e.message || 'Chưa kết nối được máy chủ.');
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
      setError('Hãy nhập đầy đủ cân nặng và chiều cao.');
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
      setMessage('Đã lưu số đo. Bạn có thể tải lại trang để kiểm tra.');
      setWeight('');
    } catch (e) {
      setError(e.message || 'Chưa lưu được số đo.');
    } finally {
      setSaving(false);
    }
  }

  const latest = rows[0];
  return (
    <main>
      <header>
        <p className="eyebrow">GROUP 13 · SMART NUTRITION & FITNESS</p>
        <h1>Theo dõi số đo</h1>
        <p>Lưu cân nặng, chiều cao và xem lại các lần ghi nhận.</p>
      </header>
      <p className="notice">Bản thực hành dùng dữ liệu giả lập. Đang phát triển chức năng tài khoản.</p>
      <div className="layout">
        <section className="entry" aria-labelledby="entry-title">
          <h2 id="entry-title">Ghi nhận mới</h2>
          <form onSubmit={save} noValidate>
            <label htmlFor="weight">Cân nặng <span>kg</span></label>
            <input id="weight" type="number" inputMode="decimal" step="0.01" placeholder="Ví dụ 70" value={weight} onChange={e => setWeight(e.target.value)} disabled={saving} />
            <label htmlFor="height">Chiều cao <span>cm</span></label>
            <input id="height" type="number" inputMode="decimal" step="0.01" placeholder="Ví dụ 175" value={height} onChange={e => setHeight(e.target.value)} disabled={saving} />
            <button type="submit" disabled={saving || loading}>{saving ? 'Đang lưu…' : 'Lưu số đo'}</button>
          </form>
          {error && <p role="alert" className="error">{error}</p>}
          {message && <p role="status" className="success">{message}</p>}
        </section>
        <section aria-labelledby="history-title">
          <div className="section-heading">
            <h2 id="history-title">Lịch sử gần đây</h2>
            <button className="secondary" onClick={loadHistory} disabled={loading || saving}>Tải lại</button>
          </div>
          {latest && <p className="latest">BMI gần nhất <strong>{latest.bmi.toFixed(2)}</strong><span>BMI = cân nặng / (chiều cao theo mét)²</span></p>}
          {loading ? <p role="status">Đang tải lịch sử…</p> : rows.length === 0 ? <p className="empty">Chưa có số đo. Hãy thêm lần ghi nhận đầu tiên.</p> :
            <div className="table-scroll"><table>
              <caption>30 lần ghi nhận gần nhất, mới nhất ở trên.</caption>
              <thead><tr><th>Thời gian</th><th>kg</th><th>cm</th><th>BMI</th></tr></thead>
              <tbody>{rows.map(row => <tr key={row.id}>
                <td>{new Date(row.created_at).toLocaleString('vi-VN')}</td>
                <td>{row.weight_kg}</td><td>{row.height_cm}</td><td>{row.bmi.toFixed(2)}</td>
              </tr>)}</tbody>
            </table></div>}
        </section>
      </div>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);

