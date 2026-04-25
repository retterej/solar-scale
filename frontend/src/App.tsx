import { useState } from 'react'
import { fetchScale, type AnchorMode, type ScaledBody } from './api'
import { CalculatorForm } from './CalculatorForm'
import { ResultsTable } from './ResultsTable'
import './index.css'

export default function App() {
  const [results, setResults] = useState<ScaledBody[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(objectName: string, mode: AnchorMode, value: number, unit: string) {
    setLoading(true)
    setError(null)
    try {
      setResults(await fetchScale(objectName, mode, value, unit))
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-5xl mx-auto px-6 py-12 space-y-8">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Solar Scale</h1>
          <p className="text-gray-500 mt-1">Scale the solar system to any size.</p>
        </div>

        <CalculatorForm onSubmit={handleSubmit} loading={loading} />

        {error && <p className="text-red-500 text-sm">{error}</p>}

        {results.length > 0 && <ResultsTable results={results} />}
      </div>
    </div>
  )
}
