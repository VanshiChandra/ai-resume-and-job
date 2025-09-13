const API_URL = import.meta.env.VITE_API_URL; // backend on Railway/Render

export async function fetchWithAuth(path, options = {}) {
  const token = localStorage.getItem("token");
  const headers = {
    ...options.headers,
    Authorization: token ? `Bearer ${token}` : "",
  };

  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) throw new Error("API request failed");
  return res.json();
}
