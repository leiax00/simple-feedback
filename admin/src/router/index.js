import NProgress from "nprogress"
import "nprogress/nprogress.css"
import { createRouter, createWebHistory } from "vue-router"
import routes from "@/router/routes"
import useUserStore from "@/store/modules/user.js"

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_APP_PREFIX),
  routes,
})

const whiteList = ["/login", "/register"]

router.beforeEach((to, from, next) => {
  NProgress.start()
  let store = useUserStore()
  console.log(to.path)
  if (store.token) {
    if (to.path === "/login") {
      next({ path: "/" })
      NProgress.done()
    } else if (whiteList.indexOf(to.path) !== -1) {
      next()
    } else {
      if (!store.id) {
        console.log("需要获取用户信息")
        store
          .getInfo()
          .then(() => {
            next()
          })
          .catch(err => {
            console.log(err)
            store.resetToken()
            next({ path: `/login?redirect=${to.fullPath}` })
          })
      } else {
        next()
      }
    }
  } else {
    if (whiteList.indexOf(to.path) !== -1) {
      next()
    } else {
      next({ path: `/login?redirect=${to.fullPath}` })
      NProgress.done()
    }
  }
})

router.afterEach(() => {
  NProgress.done()
})

export default router
