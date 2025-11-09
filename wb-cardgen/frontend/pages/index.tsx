import React, { useMemo, useState } from 'react'
import Upload from '../components/Upload'
import Step from '../components/Step'
import Button from '../components/Button'

type Uploaded = { file_id: string, url: string, width: number, height: number, format: string }
type Cutout = { cutout_id: string, url: string, width: number, height: number }
type Bg = { bg_id: string, name: string, preview_url: string }
type Composite = { composite_id: string, url: string, width: number, height: number }
type Benefit = { title: string, short_text: string }
type Variant = { variant_id: string, url: string }

const api = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export default function Home() {
  const [uploads, setUploads] = useState<Uploaded[]>([])
  const [cutout, setCutout] = useState<Cutout | null>(null)
  const [backgrounds, setBackgrounds] = useState<Bg[]>([])
  const [bgId, setBgId] = useState<string | null>(null)
  const [composite, setComposite] = useState<Composite | null>(null)
  const [benefits, setBenefits] = useState<Benefit[]>([])
  const [variants, setVariants] = useState<Variant[]>([])
  const [title, setTitle] = useState<string>('')

  const canCompose = !!cutout && !!bgId

  async function removeBg() {
    const f = uploads[0]
    const res = await fetch(`${api}/vision/remove_background`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file_id: f.file_id })
    })
    const data = await res.json()
    setCutout(data)
  }

  async function suggestBg() {
    const res = await fetch(`${api}/vision/suggest_backgrounds`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ width: 1500, height: 2000 })
    })
    const data = await res.json()
    setBackgrounds(data.items || [])
  }

  async function doCompose() {
    if (!cutout || !bgId) return
    const res = await fetch(`${api}/vision/compose`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cutout_id: cutout.cutout_id, bg_id: bgId, scale: 0.9 })
    })
    const data = await res.json()
    setComposite(data)
  }

  async function classifyAndBenefits() {
    const res = await fetch(`${api}/nlp/classify_category`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title })
    })
    const cat = await res.json()
    const res2 = await fetch(`${api}/nlp/generate_benefits`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category_id: cat.category_id, tone: 'concise', max_items: 5 })
    })
    const b = await res2.json()
    setBenefits(b.items || [])
  }

  async function generateCards() {
    if (!composite) return
    const res = await fetch(`${api}/card/generate`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ composite_id: composite.composite_id, benefits, count: 3, size_preset: 'WB_3x4' })
    })
    const data = await res.json()
    setVariants(data.variants || [])
  }

  const disabledGenerate = !composite || benefits.length === 0

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">WB Card Generator — MVP</h1>

      <Step title="1) Загрузка изображения товара">
        <Upload onDone={(items) => setUploads(items)} />
        {uploads.length > 0 && (
          <div className="mt-4 flex gap-4">
            {uploads.map(u => (
              <img key={u.file_id} src={`${api}${u.url}`} alt="" className="w-40 h-40 object-cover rounded-xl border" />
            ))}
          </div>
        )}
      </Step>

      <Step title="2) Автоудаление фона и подбор фона">
        <div className="flex gap-3">
          <Button label="Удалить фон" onClick={removeBg} disabled={uploads.length===0} />
          <Button label="Предложить фоны" onClick={suggestBg} />
        </div>
        <div className="grid grid-cols-3 gap-4 mt-4">
          {cutout && <div>
            <p className="text-sm mb-2">Вырез</p>
            <img src={`${api}${cutout.url}`} className="w-full rounded-xl border bg-white" />
          </div>}
          {backgrounds.map(bg => (
            <div key={bg.bg_id} className={`rounded-xl border overflow-hidden cursor-pointer ${bgId===bg.bg_id ? 'ring-4 ring-blue-500' : ''}`}
                 onClick={() => setBgId(bg.bg_id)}>
              <img src={`${api}${bg.preview_url}`} className="w-full" />
              <div className="p-2 text-sm">{bg.name}</div>
            </div>
          ))}
        </div>
        <div className="mt-3">
          <Button label="Скомпоновать" onClick={doCompose} disabled={!canCompose} />
        </div>
        {composite && <div className="mt-4">
          <p className="text-sm mb-2">Композиция</p>
          <img src={`${api}${composite.url}`} className="w-72 rounded-xl border bg-white" />
        </div>}
      </Step>

      <Step title="3) Категория и преимущества">
        <div className="flex gap-2 items-center">
          <input
            className="border rounded-xl px-3 py-2 w-full"
            placeholder="Название товара (для классификации)"
            value={title}
            onChange={e => setTitle(e.target.value)}
          />
          <Button label="Определить и сгенерировать" onClick={classifyAndBenefits} />
        </div>
        {benefits.length>0 && (
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            {benefits.map((b, i) => (
              <div key={i} className="bg-gray-50 border rounded-2xl p-3">
                <input className="w-full font-semibold mb-2 outline-none"
                       value={b.title}
                       onChange={e => {
                         const next = [...benefits]; next[i] = { ...b, title: e.target.value }; setBenefits(next);
                       }}/>
                <textarea className="w-full text-sm outline-none resize-none"
                          rows={3}
                          value={b.short_text}
                          onChange={e => {
                            const next = [...benefits]; next[i] = { ...b, short_text: e.target.value }; setBenefits(next);
                          }}/>
              </div>
            ))}
          </div>
        )}
      </Step>

      <Step title="4) Генерация инфографики">
        <Button label="Создать варианты" onClick={generateCards} disabled={disabledGenerate} />
        {variants.length>0 && (
          <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
            {variants.map(v => (
              <a key={v.variant_id} href={`${api}${v.url}`} target="_blank" className="block">
                <img src={`${api}${v.url}`} className="w-full rounded-2xl border bg-white" />
              </a>
            ))}
          </div>
        )}
      </Step>

      <div className="text-sm text-gray-500 mt-8">
        Готовые экспортные файлы можно открыть по ссылкам на изображение (PNG). Валидация доступна через API /validate.
      </div>
    </div>
  )
}
