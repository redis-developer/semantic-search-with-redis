<script lang="ts">
  import artworkSearcher from '@lib/searcher/svelte-artwork-searcher.svelte'

  let { clazz = '' } = $props()

  async function findArtwork() {
    await artworkSearcher.findArtwork()
  }
</script>

<button
  class="px-4 h-10 rounded-md bg-redis-hyper hover:bg-redis-deep-hyper cursor-pointer {clazz}"
  onclick={findArtwork}
>
  Find Artwork
</button>
