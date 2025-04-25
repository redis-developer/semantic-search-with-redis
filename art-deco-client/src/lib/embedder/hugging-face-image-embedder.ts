import type ImageEmbedder from '@/lib/embedder/image-embedder'

import { ImageFeatureExtractionPipeline, pipeline } from '@huggingface/transformers'

export default class HuggingFaceImageEmbedder implements ImageEmbedder {
  private featureExtractor: ImageFeatureExtractionPipeline

  constructor(featureExtractor: ImageFeatureExtractionPipeline) {
    this.featureExtractor = featureExtractor
  }

  static async create(): Promise<ImageEmbedder> {
    const featureExtractor = (await pipeline('image-feature-extraction', 'Xenova/clip-vit-base-patch32', {
      dtype: 'fp32'
    })) as unknown as ImageFeatureExtractionPipeline

    return new HuggingFaceImageEmbedder(featureExtractor)
  }

  async embed(url: string): Promise<string> {
    const bytes = await this.embedImage(url)
    const base64 = this.convertToBase64(bytes)
    return base64
  }

  private async embedImage(url: string): Promise<Uint8Array> {
    const tensor = await this.featureExtractor(url)
    const embedding = tensor.data as Float32Array
    const embeddingBytes = new Uint8Array(embedding.buffer)
    return embeddingBytes
  }

  private convertToBase64(bytes: Uint8Array): string {
    const binary = Array.from(bytes)
      .map(byte => String.fromCharCode(byte))
      .join('')
    const base64 = btoa(binary)
    return base64
  }
}
