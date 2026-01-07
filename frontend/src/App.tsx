import React, { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export default function App() {
  const [file, setFile] = useState<File | null>(null)
  const [label, setLabel] = useState('')
  const [detectResult, setDetectResult] = useState<any | null>(null)
  const [recognizeResult, setRecognizeResult] = useState<any | null>(null)

  async function postFile(endpoint: string, extra?: Record<string, any>) {
    if (!file) return
    const fd = new FormData()
    fd.append('file', file)
    if (extra) {
      Object.entries(extra).forEach(([k, v]) => fd.append(k, v as any))
    }
    const res = await fetch(`${API_BASE}${endpoint}`, { method: 'POST', body: fd })
    return await res.json()
  }

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Face Recognizer Gallery</h1>

      <div className="bg-white p-4 rounded shadow-sm mb-4">
        <label className="block mb-2">Upload an image</label>
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />

        <div className="mt-3 flex gap-2">
          <button
            className="px-3 py-1 bg-indigo-600 text-white rounded"
            onClick={async () => {
              const r = await postFile('/detect')
              setDetectResult(r)
            }}
          >
            Detect
          </button>

          <button
            className="px-3 py-1 bg-green-600 text-white rounded"
            onClick={async () => {
              const r = await postFile('/recognize')
              setRecognizeResult(r)
            }}
          >
            Recognize
          </button>

          <input
            className="border p-1 rounded"
            placeholder="Label to add"
            value={label}
            onChange={(e) => setLabel(e.target.value)}
          />

          <button
            className="px-3 py-1 bg-blue-600 text-white rounded"
            onClick={async () => {
              if (!label) return alert('Please add a label')
              const r = await postFile('/add_face', {label})
              alert(JSON.stringify(r))
            }}
          >
            Add to Gallery
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded shadow-sm">
          <h2 className="font-semibold mb-2">Detect Result</h2>
          <pre className="text-sm">{JSON.stringify(detectResult, null, 2)}</pre>
        </div>

        <div className="bg-white p-4 rounded shadow-sm">
          <h2 className="font-semibold mb-2">Recognize Result</h2>
          <pre className="text-sm">{JSON.stringify(recognizeResult, null, 2)}</pre>
        </div>
      </div>
    </div>
  )
}
