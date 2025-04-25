<script lang="ts">
  import SelectionPanel from '@components/SelectionPanel.svelte'
  import ResultsPanel from '@components/ResultsPanel.svelte'

  let { clazz = '' } = $props()
</script>

<main class="flex flex-row gap-4 m-4 mb-32 {clazz}">
  <SelectionPanel />
  <ResultsPanel />
</main>
