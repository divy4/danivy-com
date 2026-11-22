import Button from '@mui/material/Button'
import Container from '@mui/material/Container'
import { Game, wakeGame } from './api.tsx'
import TitleTimer from './TitleTimer.tsx'
import getBackground from './backgrounds.tsx'
import './index.css'

import statusDisabled from './assets/status-disabled.svg'
import statusHealthy from './assets/status-healthy.svg'
import statusUnhealthy from './assets/status-unhealthy.svg'


function getStatusIcon(game: Game): string {
  if (!game.enabled) {
    return statusDisabled
  } else if (game.healthy) {
    return statusHealthy
  } else {
    return statusUnhealthy
  }
}

interface GameStatusProps {
  game: Game
  onClick: () => void
}

function GameStatus(props: GameStatusProps) {
  const game : Game = props.game
  const onClickCallback = props.onClick

  async function copy_cloudflared_command() {
    if (game.cloudflared_command !== null) {
      navigator.clipboard.writeText(game.cloudflared_command)
    }
  }

  async function copy_password() {
    if (game.password !== null) {
      navigator.clipboard.writeText(game.password)
    }
  }

  async function wake(hours: number) {
    wakeGame(game, hours)
    if (onClickCallback !== undefined) {
      await onClickCallback()
    }
  }

  const style = {
    backgroundImage: `url(${getBackground(game)})`
  }

  return (
    <Container maxWidth="lg" style={style} className={game.enabled ? "game-row-enabled" : "game-row-disabled"}>
      <TitleTimer title={game.name} endTime={game.end_time}/>
      <div className="expanding-spacer"/>

      {game.cloudflared_command !== null ? (
        <Button variant="contained" onClick={copy_cloudflared_command}>Copy command</Button>
      ) : null}

      {game.password !== null ? (
        <Button variant="contained" onClick={copy_password}>Copy password</Button>
      ) : null}

      <Container className="button-stack">
        <Button variant="contained" onClick={() => wake(1)}>1hr</Button>
        <Button variant="contained" onClick={() => wake(2)}>2hr</Button>
        <Button variant="contained" onClick={() => wake(3)}>3hr</Button>
        <Button variant="contained" onClick={() => wake(4)}>4hr</Button>
      </Container>

      <img src={getStatusIcon(game)} className="game-status-icon"/>

    </Container>
  )
}

export default GameStatus
