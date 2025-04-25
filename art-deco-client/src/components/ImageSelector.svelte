<script lang="ts">
  import artworkSearcher from '@lib/searcher/svelte-artwork-searcher.svelte'

  let { clazz = '' } = $props()

  async function imageSelected(event: Event) {
    artworkSearcher.uploadImage(event.target as HTMLInputElement)
  }
</script>

<input
  class="file:bg-redis-hyper file:text-redis-white file:h-10 file:px-4 file:mr-3 file:text-sm hover:file:bg-redis-deep-hyper hover:file:cursor-pointer bg-redis-white text-redis-black rounded-md h-10 py-0 pr-4 {clazz}"
  type="file"
  accept="image/*"
  onchange={imageSelected}
/>
