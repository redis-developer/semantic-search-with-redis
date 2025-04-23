import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  esbuild: {
    target: 'es2022'
  },
  build: {
    target: 'es2022',
    chunkSizeWarningLimit: 1000
  },
  plugins: [tailwindcss(), svelte()],
  resolve: {
    alias: {
      '@': path.resolve('./src'),
      '@lib': path.resolve('./src/lib'),
      '@components': path.resolve('./src/components')
    }
  }
})
