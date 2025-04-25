<script lang="ts">
  import SelectedImage from '@components/SelectedImage.svelte'
  import ImageSelector from '@components/ImageSelector.svelte'
  import FindArtworkButton from '@components/FindArtworkButton.svelte'

  let { clazz = '' } = $props()
</script>

<section class={clazz}>
  <SelectedImage clazz="w-134 h-134" />
  <div class="flex flex-row gap-4 pt-4">
    <ImageSelector clazz="flex-grow" />
    <FindArtworkButton />
  </div>
</section>
