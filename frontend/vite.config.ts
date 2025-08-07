import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueDevTools from 'vite-plugin-vue-devtools'
import { visualizer } from 'rollup-plugin-visualizer';


// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
    vue(),
    VueDevTools(),
    visualizer({
    filename: 'dist/report.html',
    open: true, 
    gzipSize: true,
    brotliSize: true,
  }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0', 
    port: 5173,      
  }
})
