/* models */
import type { Artwork } from '@lib/art-deco-types'

/* driving ports */
import type ArtworkSearcher from '@lib/searcher/artwork-searcher'

/* driven ports */
import type ImageEmbedder from '@lib/embedder/image-embedder'
import type ArtworkStore from '@lib/artwork-store/artwork-store'

/* driven adapters */
import HuggingFaceImageEmbedder from '@lib/embedder/hugging-face-image-embedder'
import RestApiArtworkStore from '@lib/artwork-store/rest-api-artwork-store'

export default class ArtDecoService implements ArtworkSearcher {
  private imageEmbedder: ImageEmbedder
  private artworkStore: ArtworkStore

  /* create an instance of ArtDecoService with the given adapters */
  constructor(imageEmbedder: ImageEmbedder, artworkStore: ArtworkStore) {
    this.imageEmbedder = imageEmbedder
    this.artworkStore = artworkStore
  }

  /* create an instance of ArtDecoService with default adapters */
  static async create(): Promise<ArtDecoService> {
    const imageEmbedder = await HuggingFaceImageEmbedder.create()
    const artworkStore = RestApiArtworkStore.create()
    return new ArtDecoService(imageEmbedder, artworkStore)
  }

  /* find similar artwork by embedding the image url and searching the store */
  async findSimilarArtwork(url: string): Promise<Artwork[]> {
    const embedding = await this.imageEmbedder.embed(url)
    const artwork = this.artworkStore.searchArtworkByEmbedding(embedding)
    return artwork
  }
}
