<script lang="ts">
  let { imageUrl } = $props()
  const firstUrl = imageUrl
</script>

<div class="w-134 h-134 bg-redis-black-90 flex justify-center items-center p-8">
  <img class="max-w-full max-h-full object-contain {imageUrl === firstUrl ? 'p-32' : ''}" src={imageUrl} alt="" />
</div>
