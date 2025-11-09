export const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function removeBg(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/remove-bg`, {
    method: "POST",
    body: formData,
  });

  return res.blob();
}

export async function generateCards(data) {
  const res = await fetch(`${API_URL}/card/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function validateCard(path) {
  const res = await fetch(`${API_URL}/validate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path }),
  });
  return res.json();
}
