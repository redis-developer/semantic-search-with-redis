export default interface ImageEmbedder {
  embed: (url: string) => Promise<string>
}
