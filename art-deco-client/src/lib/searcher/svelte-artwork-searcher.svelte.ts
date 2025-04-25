import type { Artwork } from '@lib/art-deco-types'
import type ArtworkSearcher from './artwork-searcher'
import ArtDecoService from '@lib/art-deco-service'

class SvelteArtworkSearcher {
  private searcher: ArtworkSearcher

  selectedImageUrl: string = $state('/blank.png')
  foundArtwork: Artwork[] = $state([])

  constructor(searcher: ArtworkSearcher) {
    this.searcher = searcher
  }

  static async create() {
    const searcher = await ArtDecoService.create()
    return new SvelteArtworkSearcher(searcher)
  }

  async uploadImage(selector: HTMLInputElement): Promise<void> {
    const file = selector.files?.[0]
    if (!file) return

    const arrayBuffer = await file.arrayBuffer()
    if (!arrayBuffer) return

    const blob = new Blob([arrayBuffer])
    const imageUrl = URL.createObjectURL(blob)
    this.selectedImageUrl = imageUrl
  }

  async findArtwork(): Promise<void> {
    if (!this.selectedImageUrl) {
      console.error('No image selected')
      return
    }

    this.foundArtwork = await this.searcher.findSimilarArtwork(this.selectedImageUrl)
  }
}

const artworkSearcher = await SvelteArtworkSearcher.create()
export default artworkSearcher
