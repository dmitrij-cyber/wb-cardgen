"use client";
import { useState } from "react";
import { removeBg, generateCards, validateCard } from "../utils/api";

export default function TestPanel() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!file) return alert("Выберите файл");
    const processed = await removeBg(file);
    setResult(URL.createObjectURL(processed));
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>WB Cardgen Test</h2>

      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Удалить фон</button>

      {result && (
        <div>
          <h3>Результат:</h3>
          <img src={result} width={200} />
        </div>
      )}
    </div>
  );
}
