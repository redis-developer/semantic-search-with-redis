import type { Artwork } from '@lib/art-deco-types'
import type ArtworkSearcher from '@lib/searcher/artwork-searcher'
import ArtDecoService from '@lib/art-deco-service'

class SvelteArtworkSearcher {
  private searcher: ArtworkSearcher

  selectedImageUrl: string = $state('/blank.png')
  foundArtwork: Artwork[] = $state([])

  /* Create an instance with the given searcher */
  constructor(searcher: ArtworkSearcher) {
    this.searcher = searcher
  }

  /* Create an instance with default searcher */
  static async create() {
    const searcher = await ArtDecoService.create()
    return new SvelteArtworkSearcher(searcher)
  }

  /* Upload the image selected by the user and turn it into a data URL */
  async uploadImage(selector: HTMLInputElement): Promise<void> {
    /* Was a file selected */
    const file = selector.files?.[0]
    if (!file) return

    /* Get the file data */
    const arrayBuffer = await file.arrayBuffer()
    if (!arrayBuffer) return

    /* Turn the image data into a data URL */
    const blob = new Blob([arrayBuffer])
    const imageUrl = URL.createObjectURL(blob)

    /* Set the selected image URL in the Svelte state */
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
