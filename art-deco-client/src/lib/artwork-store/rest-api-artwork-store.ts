import type { Artwork } from '@lib/art-deco-types'
import type ArtworkStore from '@lib/artwork-store/artwork-store'

type JsonArtwork = {
  ulid: string
  title: string
  artist: string
  image_url: string
}

type JsonArtworks = JsonArtwork[]

export default class RestApiArtworkStore implements ArtworkStore {
  private endpoint: string

  constructor(endpoint: string) {
    this.endpoint = endpoint
  }

  static create(): ArtworkStore {
    const endpoint = 'http://localhost:8000'
    return new RestApiArtworkStore(endpoint)
  }

  async fetchArtworkById(id: string): Promise<Artwork | null> {
    const response = await this.invokeGet(`${this.endpoint}/items/${id}`)

    if (response.status === 404) return null
    this.validateResponse(response)

    const json = (await response.json()) as JsonArtwork
    const artwork = this.jsonToArtwork(json)

    return artwork
  }

  async searchArtworkByEmbedding(embedding: string): Promise<Artwork[]> {
    const params = new URLSearchParams()
    params.append('embedding', embedding)

    const response = await this.invokePost(`${this.endpoint}/items/search`, params)

    this.validateResponse(response)

    const json = (await response.json()) as JsonArtworks
    const artworks = this.toJsonArtworks(json)

    return artworks
  }

  private async invokeGet(url: string): Promise<Response> {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json'
      }
    })

    return response
  }

  private async invokePost(url: string, body: URLSearchParams): Promise<Response> {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        Accept: 'application/json'
      },
      body: body
    })

    return response
  }

  private validateResponse(response: Response): void {
    if (!response.ok) throw new Error(`Error fetching data from server: ${response.statusText} (${response.status})`)
  }

  private toJsonArtworks(json: JsonArtworks): Artwork[] {
    return json.map(item => this.jsonToArtwork(item))
  }

  private jsonToArtwork(json: JsonArtwork): Artwork {
    return {
      id: json.ulid,
      title: json.title,
      author: json.artist,
      url: json.image_url
    }
  }
}
