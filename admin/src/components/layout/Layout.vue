<script setup>
  defineOptions({ name: "Layout" })
  document.documentElement.classList.add("dark")

  const route = useRoute()
</script>

<template>
  <div class="layout-main grow flex flex-col">
    <div class="header-wrapper">
      <BaseHeader />
    </div>
    <div class="content-wrapper grow flex flex-col">
      <router-view :key="route.path" />
    </div>
    <div class="footer-wrapper">
      <BaseFooter />
    </div>
    <el-backtop :right="40" :bottom="92" />
  </div>
</template>

<style scoped>
  :deep(.el-backtop) {
    --el-backtop-bg-color: var(--color-zinc-700);
    --el-backtop-hover-bg-color: var(--color-zinc-500);
  }
  .layout-main {
  }
</style>
