import * as path from "node:path"
import { readFileSync } from "node:fs"
import globals from "globals"
import pluginJs from "@eslint/js"
import pluginVue from "eslint-plugin-vue"
import pluginPrettier from "eslint-plugin-prettier/recommended"

const autoImportConfig = JSON.parse(readFileSync(path.resolve("./eslint-auto-import.json"), "utf-8"))
/** @type {import('eslint').Linter.Config[]} */
export default [
  {
    files: ["**/*.{js,mjs,cjs,vue}"],
  },
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...autoImportConfig.globals,
      },
    },
  },
  pluginJs.configs.recommended,
  ...pluginVue.configs["flat/essential"],
  pluginPrettier,
  {
    rules: {
      "vue/multi-word-component-names": "off", // 关闭必须使用多个单词作为组件名称的检测
      "no-unused-vars": "warn", // 关闭未使用变量的检测
    },
  },
]
