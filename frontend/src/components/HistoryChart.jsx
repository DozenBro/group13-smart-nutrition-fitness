import React, { useState } from 'react';

export default function HistoryChart({ rows }) {
  const [metric, setMetric] = useState('weight_kg');

  if (!rows || rows.length === 0) {
    return null;
  }

  // API returns newest-first; chart requires chronological order (oldest-first)
  const chronological = [...rows].reverse();
  const values = chronological.map((r) => Number(r[metric]));
  const unit = metric === 'weight_kg' ? 'kg' : 'BMI';

  const width = 560;
  const height = 220;
  const padLeft = 48;
  const padRight = 20;
  const padTop = 20;
  const padBottom = 38;
  const chartW = width - padLeft - padRight;
  const chartH = height - padTop - padBottom;

  const rawMin = Math.min(...values);
  const rawMax = Math.max(...values);
  const spread = rawMax - rawMin || 2;
  const minVal = Math.max(0, rawMin - spread * 0.15);
  const maxVal = rawMax + spread * 0.15;

  const points = chronological.map((row, idx) => {
    const x =
      chronological.length === 1
        ? padLeft + chartW / 2
        : padLeft + (idx / (chronological.length - 1)) * chartW;
    const val = Number(row[metric]);
    const y = padTop + chartH - ((val - minVal) / (maxVal - minVal || 1)) * chartH;
    const dateLabel = new Date(row.created_at).toLocaleDateString('en-GB', {
      day: '2-digit',
      month: '2-digit',
    });
    return { x, y, val, dateLabel, id: row.id };
  });

  const polylinePoints = points.map((p) => `${p.x},${p.y}`).join(' ');
  const yTicks = [maxVal, (maxVal + minVal) / 2, minVal];

  return (
    <div className="chart-box">
      <div className="section-heading">
        <h3>Trend chart ({unit})</h3>
        <div className="tabs" style={{ marginBottom: 0 }}>
          <button
            type="button"
            className={metric === 'weight_kg' ? 'tab active' : 'tab'}
            onClick={() => setMetric('weight_kg')}
          >
            Weight (kg)
          </button>
          <button
            type="button"
            className={metric === 'bmi' ? 'tab active' : 'tab'}
            onClick={() => setMetric('bmi')}
          >
            BMI
          </button>
        </div>
      </div>

      <div className="chart-scroll">
        <svg viewBox={`0 0 ${width} ${height}`} className="history-svg" role="img" aria-label={`Chronological ${unit} chart`}>
          {yTicks.map((tick, i) => {
            const y = padTop + (i / 2) * chartH;
            return (
              <g key={i}>
                <line x1={padLeft} y1={y} x2={width - padRight} y2={y} className="chart-grid" />
                <text x={padLeft - 8} y={y + 4} textAnchor="end" className="chart-label">
                  {tick.toFixed(1)}
                </text>
              </g>
            );
          })}

          {points.length > 1 && (
            <polyline fill="none" points={polylinePoints} className="chart-line" />
          )}

          {points.map((p, i) => {
            const showDate =
              points.length <= 6 || i === 0 || i === points.length - 1 || i % Math.ceil(points.length / 5) === 0;
            return (
              <g key={p.id}>
                <circle cx={p.x} cy={p.y} r="4" className="chart-dot">
                  <title>{`${p.dateLabel}: ${p.val.toFixed(2)} ${unit}`}</title>
                </circle>
                {showDate && (
                  <text x={p.x} y={height - 10} textAnchor="middle" className="chart-label">
                    {p.dateLabel}
                  </text>
                )}
              </g>
            );
          })}
        </svg>
      </div>
    </div>
  );
}