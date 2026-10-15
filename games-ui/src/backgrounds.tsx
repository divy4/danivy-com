import { Game } from './api.tsx'
import minecraft from './assets/minecraft.webp'
import spaceEngineers2 from './assets/space-engineers-2.webp'
import valheim from './assets/valheim.webp'
import yoda from './assets/yoda.webp'


function getBackground(game: Game) {
  if (game.name.includes("minecraft")) {
    return minecraft
  } else if (game.name.includes("space-engineers")) {
    return spaceEngineers2
  } else if (game.name.includes("valheim")) {
    return valheim
  }
  return yoda
}

export default getBackground
