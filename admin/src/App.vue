<script setup>
  const zIndex = ref(3000)
  // eslint-disable-next-line no-unused-vars
  const size = ref("small")
</script>

<template>
  <el-config-provider size="default" :z-index="zIndex">
    <router-view />
  </el-config-provider>
</template>

<style scoped></style>
