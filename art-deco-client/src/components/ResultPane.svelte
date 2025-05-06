<script lang="ts">
  import type { Artwork } from '@lib/art-deco-types'

  interface Props {
    artwork: Artwork | null
    clazz?: string
  }

  let { artwork, clazz = '' }: Props = $props()

  const backgroundClass = 'bg-redis-black-90 bg-center bg-no-repeat bg-[length:25px] bg-[url(/redis-social.svg)]'

  let imageUrl = $derived(() => artwork?.url ?? '/blank.png')
  let altText = $derived(() => {
    const title = artwork?.title ?? 'Untitled'
    const author = artwork?.author ?? 'Unknown Artist'
    return `${title} by ${author}`
  })
</script>

<div class="w-72 h-72 p-4 flex flex-col justify-center items-center {backgroundClass} {clazz}">
  <img class="max-w-full max-h-full" src={imageUrl()} alt={altText()} title={altText()} />
</div>
