export interface Measurement {
  imperial: string
  metric: string
}

export interface ScaledBody {
  name: string
  kind: string
  orbit_au: number
  distance: Measurement
  diameter: Measurement
}

export type AnchorMode = 'orbit' | 'size'

export async function fetchScale(
  objectName: string,
  mode: AnchorMode,
  value: number,
  unit: string,
): Promise<ScaledBody[]> {
  const params = new URLSearchParams({
    object_name: objectName,
    unit,
    [mode]: String(value),
  })
  const res = await fetch(`/api/scale?${params}`)
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail ?? `Request failed: ${res.status}`)
  }
  return res.json()
}
