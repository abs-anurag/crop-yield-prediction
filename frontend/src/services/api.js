const BASE_URL = import.meta.env.VITE_API_URL || '';
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

async function fetchMock(path) {
  const response = await fetch(`${BASE_URL}/src/mock/${path}`);
  if (!response.ok) {
    throw new Error(`Mock file ${path} not found`);
  }
  return response.json();
}

export async function fetchMetadata() {
  if (USE_MOCK) {
    return fetchMock('metadata-response.json');
  }

  const res = await fetch(`${BASE_URL}/api/metadata`);
  if (!res.ok) {
    throw new Error('Metadata unavailable');
  }
  return res.json();
}

export async function predictYield(formData) {
  if (USE_MOCK) {
    await new Promise(resolve => setTimeout(resolve, 800));
    return fetchMock('prediction-response.json');
  }

  const res = await fetch(`${BASE_URL}/api/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData),
  });

  if (!res.ok) {
    const err = await res.json();
    throw err;
  }

  return res.json();
}

export async function fetchHealth() {
  if (USE_MOCK) {
    return { status: 'ok', model_loaded: true, version: '1.0.0' };
  }

  const res = await fetch(`${BASE_URL}/api/health`);
  if (!res.ok) {
    throw new Error('Health check failed');
  }
  return res.json();
}