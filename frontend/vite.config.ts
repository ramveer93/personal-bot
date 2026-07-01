import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import cssInjectedByJsPlugin from 'vite-plugin-css-injected-by-js'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    cssInjectedByJsPlugin()
  ],
  build: {
    rollupOptions: {
      output: {
        // Build everything into a single JS file
        entryFileNames: `widget.js`,
        chunkFileNames: `widget.js`,
        assetFileNames: `widget.[ext]`,
        manualChunks: undefined,
      }
    }
  }
})
