import type { ScaledBody } from './api'

interface Props {
  results: ScaledBody[]
}

const COL = 'px-4 py-2 text-sm'
const COL_R = `${COL} text-right`

export function ResultsTable({ results }: Props) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-left">
        <thead>
          <tr className="border-b border-gray-200 text-gray-500 text-xs uppercase tracking-wide">
            <th className={COL}>Body</th>
            <th className={COL_R}>Orbit (AU)</th>
            <th className={COL_R}>Distance (imperial)</th>
            <th className={COL_R}>Distance (metric)</th>
            <th className={COL_R}>Diameter (imperial)</th>
            <th className={COL_R}>Diameter (metric)</th>
          </tr>
        </thead>
        <tbody>
          {results.map((body) => (
            <tr key={body.name} className="border-b border-gray-100 hover:bg-gray-50">
              <td className={`${COL} font-medium text-gray-900`}>{body.name}</td>
              <td className={`${COL_R} text-gray-500`}>
                {body.orbit_au > 0 ? body.orbit_au.toFixed(3) : '--'}
              </td>
              <td className={COL_R}>{body.distance.imperial}</td>
              <td className={COL_R}>{body.distance.metric}</td>
              <td className={COL_R}>{body.diameter.imperial}</td>
              <td className={COL_R}>{body.diameter.metric}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
