<script lang="ts">
  import ResultPane from '@components/ResultPane.svelte'
  import artworkSearcher from '@lib/searcher/svelte-artwork-searcher.svelte'

  let { clazz = '' } = $props()

  const firstArtwork = $derived(() => artworkSearcher.foundArtwork[0] ?? null)
  const secondArtwork = $derived(() => artworkSearcher.foundArtwork[1] ?? null)
  const thirdArtwork = $derived(() => artworkSearcher.foundArtwork[2] ?? null)
  const fourthArtwork = $derived(() => artworkSearcher.foundArtwork[3] ?? null)
</script>

<section class="grid grid-cols-2 gap-4 {clazz}">
  <ResultPane artwork={firstArtwork()} />
  <ResultPane artwork={secondArtwork()} />
  <ResultPane artwork={thirdArtwork()} />
  <ResultPane artwork={fourthArtwork()} />
</section>
