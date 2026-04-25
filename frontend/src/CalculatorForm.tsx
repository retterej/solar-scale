import { useState } from 'react'
import type { AnchorMode } from './api'

interface Props {
  onSubmit: (objectName: string, mode: AnchorMode, value: number, unit: string) => void
  loading: boolean
}

const BODIES = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

export function CalculatorForm({ onSubmit, loading }: Props) {
  const [objectName, setObjectName] = useState('Neptune')
  const [mode, setMode] = useState<AnchorMode>('orbit')
  const [value, setValue] = useState('')
  const [unit, setUnit] = useState('ft')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSubmit(objectName, mode, Number(value), unit)
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-wrap gap-3 items-end">
      <div className="flex flex-col gap-1">
        <label className="text-sm text-gray-500">Object</label>
        <select
          value={objectName}
          onChange={(e) => setObjectName(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2 bg-white text-sm"
        >
          {BODIES.map((b) => <option key={b}>{b}</option>)}
        </select>
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm text-gray-500">Anchor by</label>
        <select
          value={mode}
          onChange={(e) => setMode(e.target.value as AnchorMode)}
          className="border border-gray-300 rounded px-3 py-2 bg-white text-sm"
        >
          <option value="orbit">Orbit distance</option>
          <option value="size">Diameter</option>
        </select>
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm text-gray-500">Value</label>
        <input
          type="number"
          min="0"
          step="any"
          required
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2 w-28 text-sm"
          placeholder="e.g. 142"
        />
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm text-gray-500">Unit</label>
        <select
          value={unit}
          onChange={(e) => setUnit(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2 bg-white text-sm"
        >
          <option value="ft">ft</option>
          <option value="in">in</option>
          <option value="mi">mi</option>
          <option value="m">m</option>
          <option value="cm">cm</option>
          <option value="km">km</option>
        </select>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="bg-gray-900 text-white rounded px-4 py-2 text-sm hover:bg-gray-700 disabled:opacity-50 cursor-pointer"
      >
        {loading ? 'Calculating…' : 'Calculate'}
      </button>
    </form>
  )
}
