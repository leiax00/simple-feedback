<script setup>
  import useUserStore from "@/store/modules/user.js"

  defineOptions({ name: "Login" })
  document.documentElement.classList.add("dark")

  const form = reactive({
    username: "",
    password: "",
  })

  const userStore = useUserStore()
  const router = useRouter()
  const toLogin = () => {
    console.log("login", form)
    userStore.login(form).then(res => {
      console.log(JSON.stringify(res))
      return router.push({ path: "/home" })
    })
  }
</script>

<template>
  <div class="login-main flex flex-col w-full justify-center items-center">
    <div class="login-content flex flex-col bg-zinc-700 text-zinc-300 dark:bg-white dark:text-zinc-800">
      <!--    <button class="bg-blue-500 mb-6" @click="changeTheme">{{ isDark ? "light" : "dark" }}</button>-->
      <div class="text-center pb-6 text-xl">Simple Feedback</div>
      <el-form :model="form" label-width="auto" style="max-width: 600px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password placeholder="密码" />
        </el-form-item>
        <el-form-item class="btn-wrapper">
          <el-button type="primary" @click="toLogin">Login</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
  .login-content {
    padding: calc(var(--spacing) * 6);
    border-radius: var(--radius-sm);
    min-width: var(--window-min-width);

    .page-login {
      color: var(--color-blue-500);
    }

    :deep(.el-form-item) {
      &.btn-wrapper {
        .el-form-item__content {
          justify-content: center;
        }
      }
    }
  }
</style>
