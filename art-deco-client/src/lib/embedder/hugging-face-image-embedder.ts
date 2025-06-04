import { ImageFeatureExtractionPipeline, pipeline } from '@huggingface/transformers'

import type ImageEmbedder from '@lib/embedder/image-embedder'

export default class HuggingFaceImageEmbedder implements ImageEmbedder {
  private featureExtractor: ImageFeatureExtractionPipeline

  /* create an instance with the given feature extractor */
  constructor(featureExtractor: ImageFeatureExtractionPipeline) {
    this.featureExtractor = featureExtractor
  }

  /* create an instance with default feature extractor */
  static async create(): Promise<ImageEmbedder> {
    const featureExtractor = await pipeline('image-feature-extraction', 'Xenova/clip-vit-base-patch32', {
      dtype: 'fp32'
    })

    return new HuggingFaceImageEmbedder(featureExtractor)
  }

  /* embed the image url and return the base64 string */
  async embed(url: string): Promise<string> {
    const bytes = await this.embedImage(url)
    const base64 = this.convertToBase64(bytes)
    return base64
  }

  /* embed the image url and return the bytes */
  private async embedImage(url: string): Promise<Uint8Array> {
    /* Extract the image features */
    const tensor = await this.featureExtractor(url)
    const embedding = tensor.data as Float32Array

    /* Normalize the embedding */
    const norm = Math.sqrt(embedding.reduce((sum, val) => sum + val * val, 0))
    const normalizedEmbedding = embedding.map(val => val / norm)

    /* Return the embedding bytes */
    const embeddingBytes = new Uint8Array(normalizedEmbedding.buffer)
    return embeddingBytes
  }

  /* convert the bytes to base64 string */
  private convertToBase64(bytes: Uint8Array): string {
    const binary = Array.from(bytes)
      .map(byte => String.fromCharCode(byte))
      .join('')
    const base64 = btoa(binary)
    return base64
  }
}
