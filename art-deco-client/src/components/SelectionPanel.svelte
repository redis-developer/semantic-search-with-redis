<script lang="ts">
  const defaultImageUrl = '/redis-logo-white.svg'

  import SelectedImage from '@components/SelectedImage.svelte'
  import { uploadImage } from '@lib/image-handler.svelte'

  let imageUrl = $state(defaultImageUrl)

  async function imageSelected(event: Event) {
    const input = event.target as HTMLInputElement
    imageUrl = (await uploadImage(input)) ?? defaultImageUrl
  }
</script>

<section>
  <SelectedImage {imageUrl} />
  <div class="flex flex-row gap-4 pt-4">
    <input
      class="file:bg-redis-hyper file:text-redis-white file:h-10 file:px-4 file:mr-3 file:text-sm hover:file:bg-redis-deep-hyper hover:file:cursor-pointer bg-redis-white text-redis-black rounded-md h-10 py-0 flex-grow"
      type="file"
      id="image-input"
      accept="image/*"
      onchange={imageSelected}
    />

    <button
      class="px-4 h-10 rounded-md bg-redis-hyper hover:bg-redis-deep-hyper cursor-pointer"
      id="generate-button"
      type="submit"
    >
      Find Artwork
    </button>
  </div>
</section>
