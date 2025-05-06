import type ArtworkStore from '@lib/artwork-store/artwork-store'
import type { Artwork } from '@lib/art-deco-types'

type JsonArtwork = {
  ulid: string
  title: string
  author: string
  image_url: string
}

type JsonArtworks = JsonArtwork[]

export default class RestApiArtworkStore implements ArtworkStore {
  private endpoint: string

  /* create an instance with the given endpoint */
  constructor(endpoint: string) {
    this.endpoint = endpoint
  }

  /* create an instance with the default endpoint */
  static create(): ArtworkStore {
    const endpoint = 'http://localhost:8000'
    return new RestApiArtworkStore(endpoint)
  }

  /* fetch artwork by id from the server */
  async fetchArtworkById(id: string): Promise<Artwork | null> {
    /* make a simple GET request for the artwork */
    const response = await this.invokeGet(`${this.endpoint}/items/${id}`)

    /* if the artwork is not found, return null */
    if (response.status === 404) return null

    /* make sure there aren't any other errors */
    this.validateResponse(response)

    /* parse the JSON to an object */
    const json = (await response.json()) as JsonArtwork
    const artwork = this.jsonToArtwork(json)

    /* return the artwork */
    return artwork
  }

  /* search for similar artwork by embedding */
  async searchArtworkByEmbedding(embedding: string): Promise<Artwork[]> {
    /* Add the embedding to the request body */
    const params = new URLSearchParams()
    params.append('embedding', embedding)

    /* make a POST request to the server */
    const response = await this.invokePost(`${this.endpoint}/items/search`, params)

    /* make sure there aren't any errors */
    this.validateResponse(response)

    /* parse the JSON to an array of objects */
    const json = (await response.json()) as JsonArtworks
    const artworks = this.toJsonArtworks(json)

    /* return the artworks */
    return artworks
  }

  /* invoke the GET request with the given URL */
  private async invokeGet(url: string): Promise<Response> {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json'
      }
    })

    return response
  }

  /* invoke the POST request with the given URL and body */
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

  /* validate the response from the server and throw an error accordingly */
  private validateResponse(response: Response): void {
    if (!response.ok) throw new Error(`Error fetching data from server: ${response.statusText} (${response.status})`)
  }

  /* convert the JSON array to an array of Artwork objects */
  private toJsonArtworks(json: JsonArtworks): Artwork[] {
    return json.map(item => this.jsonToArtwork(item))
  }

  /* convert the JSON object to an Artwork object */
  private jsonToArtwork(json: JsonArtwork): Artwork {
    return {
      id: json.ulid,
      title: json.title,
      author: json.author,
      url: json.image_url
    }
  }
}
