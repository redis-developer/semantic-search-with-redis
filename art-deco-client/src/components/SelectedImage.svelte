<script lang="ts">
  import artworkSearcher from '@lib/searcher/svelte-artwork-searcher.svelte'

  let { clazz = '' } = $props()

  const imageUrl = $derived(() => artworkSearcher.selectedImageUrl)
</script>

<div
  class="bg-redis-black-90 flex justify-center items-center bg-center bg-no-repeat bg-[length:50px] bg-[url(/redis-social.svg)] p-8 {clazz}"
>
  <img class="max-w-full max-h-full" src={imageUrl()} alt="Your selection" />
</div>
