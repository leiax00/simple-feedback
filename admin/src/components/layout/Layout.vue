<script setup>
  import { useDark, useToggle } from "@vueuse/core"

  defineOptions({ name: "Layout" })
  const route = useRoute()
</script>

<template>
  <div class="layout-main">
    Hello World!
    <router-view :key="route.path" />
  </div>
</template>

<style scoped></style>
