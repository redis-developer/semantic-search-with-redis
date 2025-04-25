import type { Artwork } from '@/lib/art-deco-types'

export default interface ArtworkSearcher {
  findSimilarArtwork: (imageUrl: string) => Promise<Artwork[]>
}
