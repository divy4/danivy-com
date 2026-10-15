import Button from '@mui/material/Button'
import Container from '@mui/material/Container'
import { Game, startGame } from './api.tsx'
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
  onClick: () => Void
}

function GameStatus(props: GameStatusProps) {
  const game : Game = props.game
  const onClickCallback = props.onClick

  async function start() {
    startGame(game)
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
      <div className="game-spacer"/>
      <Button variant="contained" onClick={start}>
        {game.enabled ? "Keep running" : "Start"}
      </Button>
      <img src={getStatusIcon(game)} className="game-status-icon"/>
    </Container>
  )
}

export default GameStatus
