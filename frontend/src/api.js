const TOKEN_KEY = 'g13_auth_token';

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export async function request(path, options = {}) {
  const token = getToken();
  const headers = { ...(options.headers || {}) };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  if (options.body && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(path, { ...options, headers });

  if (response.status === 204) {
    return null;
  }

  const body = await response.json().catch(() => ({}));

  if (!response.ok) {
    let message = 'The request failed. Please try again.';
    if (Array.isArray(body.detail) && body.detail.length > 0) {
      const first = body.detail[0];
      const field = first?.loc?.at(-1);
      if (field === 'weight_kg') {
        message = 'Weight must be greater than 0 and no more than 500 kg, with up to 2 decimal places.';
      } else if (field === 'height_cm') {
        message = 'Height must be between 50 and 250 cm, with up to 2 decimal places.';
      } else {
        message = field ? `${field}: ${first.msg}` : first.msg;
      }
    } else if (typeof body.detail === 'string') {
      message = body.detail;
    }

    const err = new Error(message);
    err.status = response.status;
    throw err;
  }

  return body;
}

export const authApi = {
  register: (email, password) =>
    request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),
  login: (email, password) =>
    request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),
  logout: () => request('/api/auth/logout', { method: 'POST' }),
  me: () => request('/api/auth/me'),
};

export const profileApi = {
  get: () => request('/api/profile'),
  update: (payload) =>
    request('/api/profile', {
      method: 'PUT',
      body: JSON.stringify(payload),
    }),
};

export const measurementApi = {
  list: () => request('/api/measurements'),
  create: (weight_kg, height_cm) =>
    request('/api/measurements', {
      method: 'POST',
      body: JSON.stringify({ weight_kg, height_cm }),
    }),
};

export const healthApi = {
  estimate: () => request('/api/health/estimate'),
};

export const adminApi = {
  listUsers: () => request('/api/admin/users'),
  lockUser: (userId) => request(`/api/admin/users/${userId}/lock`, { method: 'POST' }),
  unlockUser: (userId) => request(`/api/admin/users/${userId}/unlock`, { method: 'POST' }),
};

function workoutHeaders(user) {
  if (!user) return {};
  return {
    'X-User-Id': String(user.id),
    'X-User-Role': user.role,
  };
}

export const workoutApi = {
  getCurrentPlan: (user) =>
    request('/api/workout-plans/current', { headers: workoutHeaders(user) }),
  createPlan: (user, goal) =>
    request('/api/workout-plans', {
      method: 'POST',
      headers: workoutHeaders(user),
      body: JSON.stringify({ goal }),
    }),
  completeSession: (user, sessionId) =>
    request(`/api/workout-sessions/${sessionId}/complete`, {
      method: 'POST',
      headers: workoutHeaders(user),
    }),
  getStreak: (user) =>
    request('/api/streak', { headers: workoutHeaders(user) }),
  listCategories: (user) =>
    request('/api/exercise-categories', { headers: workoutHeaders(user) }),
  listExercises: (user, params = {}) => {
    const query = new URLSearchParams();
    if (params.category) query.set('category', params.category);
    if (params.goal) query.set('goal', params.goal);
    const qs = query.toString();
    return request(qs ? `/api/exercises?${qs}` : '/api/exercises', {
      headers: workoutHeaders(user),
    });
  },
};

export const foodApi = {
  list: (params = {}) => {
    const query = new URLSearchParams();
    if (params.meal_slot) query.set('meal_slot', params.meal_slot);
    if (params.max_price_vnd !== '' && params.max_price_vnd != null) {
      query.set('max_price_vnd', String(params.max_price_vnd));
    }
    if (params.tag) query.set('tag', params.tag);
    const qs = query.toString();
    return request(qs ? `/api/foods?${qs}` : '/api/foods');
  },
  create: (payload) =>
    request('/api/foods', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  remove: (foodId) =>
    request(`/api/foods/${foodId}`, { method: 'DELETE' }),
};