<script lang="ts">
  import type { Artwork } from '@/lib/art-deco-types'

  interface Props {
    artwork: Artwork | null
    clazz?: string
  }

  let { artwork, clazz = '' }: Props = $props()

  const defaultImage = '/blank.png'

  let imageUrl = $derived(() => artwork?.url ?? defaultImage)
</script>

<div
  class="w-72 h-72 bg-redis-black-90 flex justify-center items-center bg-center bg-no-repeat bg-[length:25px] bg-[url(/redis-social.svg)] p-4 {clazz}"
>
  <img class="max-w-full max-h-full" src={imageUrl()} alt="" />
</div>
