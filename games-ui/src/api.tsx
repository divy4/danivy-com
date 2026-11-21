export class Game {
  name: string = ""
  enabled: boolean = false
  healthy: boolean = false
  start_time: number | null = null
  end_time: number | null = null
}


export async function getGames() : Promise<Game[]> {
  const response = await fetch(`/api/v1/games`)
  const rawGames = JSON.parse(await response.text())
  const games = []
  for (const rawGame of rawGames) {
    const game = Object.assign(new Game(), rawGame)
    games.push(game)
  }
  return games
}

export async function wakeGame(game: Game, hours: number) : Promise<void> {
  await fetch(`/api/v1/games/${game.name}/wake`, {
    method: "POST",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({hours: hours}),
  })
}

