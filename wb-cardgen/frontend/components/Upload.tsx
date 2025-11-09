import React, { useRef, useState } from 'react'

type Uploaded = { file_id: string, url: string, width: number, height: number, format: string }

export default function Upload({ onDone }: { onDone: (items: Uploaded[]) => void }) {
  const ref = useRef<HTMLInputElement>(null)
  const [loading, setLoading] = useState(false)

  const api = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

  async function handleFiles(files: FileList | null) {
    if (!files || files.length === 0) return
    setLoading(true)
    const form = new FormData()
    Array.from(files).forEach(f => form.append('files', f))
    const res = await fetch(`${api}/media/upload`, { method: 'POST', body: form })
    const data = await res.json()
    setLoading(false)
    onDone(data.items || [])
  }

  return (
    <div className="border-2 border-dashed rounded-2xl p-6 text-center bg-white">
      <input ref={ref} type="file" className="hidden" multiple accept="image/*"
             onChange={e => handleFiles(e.target.files)} />
      <p className="mb-2">Перетащите фото или выберите файлы</p>
      <button
        onClick={() => ref.current?.click()}
        className="px-4 py-2 rounded-2xl shadow bg-gray-800 text-white hover:bg-black"
        disabled={loading}
      >
        {loading ? 'Загрузка...' : 'Выбрать файлы'}
      </button>
    </div>
  )
}
