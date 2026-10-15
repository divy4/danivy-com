import { useEffect, useState } from 'react'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline';
import { getTime } from './util.tsx'
import { Game, getGames } from './api.tsx'
import GameStatus from './GameStatus.tsx'
import './index.css'

const REFRESH_INTERVAL_SECONDS = 5
const REFRESH_TIMEOUT_SECONDS = 600

const theme = createTheme({
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          "&.Mui-disabled": {
            background: "#404040",
            color: "#808080"
          }
        }
      }
    }
  }
});


function App() {
  const [lastClick, setLastClick] = useState(getTime())
  const [games, setGames] = useState<Game[]>([])

  async function onClick() {
    setLastClick(getTime())
  }

  useEffect(() => {
    const refresh = async () => {
      console.log(`Refreshing game list at ${getTime()}`)
      setGames(await getGames())
      if (getTime() < lastClick + REFRESH_TIMEOUT_SECONDS) {
        setTimeout(refresh, 1000 * REFRESH_INTERVAL_SECONDS)
      }
    }

    refresh()
  }, [lastClick])

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box className="game-box">
        <Stack spacing={2} className="game-stack">
          {games.map((game, i) => (
            <GameStatus key={i} game={game} onClick={onClick}/>
          ))}
        </Stack>
      </Box>
    </ThemeProvider>
  )
}

export default App
