import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import tailwindcss from "@tailwindcss/vite"
import AutoImport from "unplugin-auto-import/vite"
import Components from "unplugin-vue-components/vite"
import { ElementPlusResolver } from "unplugin-vue-components/resolvers"

// https://vite.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "@": "/src",
    },
  },
  plugins: [
    vue(),
    tailwindcss(),
    AutoImport({
      imports: ["vue", "vue-router", "pinia"],
      resolvers: [ElementPlusResolver()],
      eslintrc: {
        enabled: true,
        filepath: "./eslint-auto-import.json",
        globalsPropValue: "readonly",
      },
      dts: "src/auto-imports.d.ts",
    }),
    Components({
      dirs: ["src/components"], // 组件目录
      extensions: ["vue"],
      deep: true,
      resolvers: [ElementPlusResolver()],
      dts: "src/components.d.ts",
    }),
  ],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        // rewrite: path => path.replace(/^\/api/, ""),
      },
    },
  },
})
