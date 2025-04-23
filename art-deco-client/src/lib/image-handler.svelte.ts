export async function uploadImage(selector: HTMLInputElement): Promise<string | null> {
  const file = selector.files?.[0]
  if (!file) return null

  const arrayBuffer = await file.arrayBuffer()
  if (!arrayBuffer) return null

  const blob = new Blob([arrayBuffer])
  const imageUrl = URL.createObjectURL(blob)
  return imageUrl
}
