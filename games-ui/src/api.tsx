export class Game {
  name: string = ""
  enabled: boolean = false
  healthy: boolean = false
  start_time: int | null = null
  end_time: int | null = null
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

export async function startGame(game: Game) : Promise<void> {
  await fetch(`/api/v1/games/${game.name}/start`, {
    method: "POST"
  })
}
