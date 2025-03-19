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
  </div>
</template>

<style scoped></style>
