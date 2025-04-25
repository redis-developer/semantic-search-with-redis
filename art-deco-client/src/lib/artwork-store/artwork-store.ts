import type { Artwork } from '@lib/art-deco-types'

export default interface ArtworkStore {
  fetchArtworkById: (id: string) => Promise<Artwork | null>
  searchArtworkByEmbedding: (embedding: string) => Promise<Artwork[]>
}
