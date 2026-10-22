import { useEffect, useState } from 'react'
import { getTime } from './util.tsx'

interface TitleTimerProps {
  title: string
  endTime: number | null
}

function TitleTimer(props: TitleTimerProps) {
  const [now, setNow] = useState(() => getTime())

  useEffect(() => {
    const interval = setInterval(() => setNow(getTime()), 30000)
    return () => {
      clearInterval(interval)
    }
  }, [])

  let s = `${props.title}`
  const total_seconds = Math.max(0, (props.endTime ?? now) - now)
  if (total_seconds > 0) {
    const total_minutes = Math.floor(total_seconds / 60)
    const hours = Math.floor(total_minutes / 60)
    const minutes = total_minutes % 60

    s += ` - `
    if (hours > 0) {
      s += `${hours}h`
    }
    if (minutes > 0) {
      s += `${minutes}m`
    }
    if (hours == 0 && minutes == 0) {
      s += `<1m`
    }
    s += " left"
  }

  return (
    <p className="game-title">{s}</p>
  )
}

export default TitleTimer
