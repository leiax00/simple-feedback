<script setup>
  import useAppStore from "@/store/modules/app.js"
  import useUserStore from "@/store/modules/user.js"

  defineOptions({ name: "BaseHeader" })
  const appStore = useAppStore()
  const userStore = useUserStore()
  const router = useRouter()
  const logout = () => {
    userStore.logout().then(() => {
      router.push("/login")
    })
  }
</script>

<template>
  <div class="header-main px-6 h-16 flex flex-row items-center justify-between">
    <div class="logo-wrapper flex flex-row items-baseline">
      <div class="title text-2xl">Simple Feedback</div>
      <div class="ml-2 version dark:text-zinc-400 text-xs">v{{ appStore.version }}</div>
    </div>
    <div class="right-wrapper flex flex-row items-center justify-center">
      <el-button link @click="logout">登出</el-button>
    </div>
  </div>
</template>
