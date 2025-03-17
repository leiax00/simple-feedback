import Layout from "@/components/layout/Layout.vue"

export default [
  {
    path: "/",
    redirect: "home",
    component: Layout,
    children: [
      { path: "index", redirect: "home" },
      {
        path: "home",
        component: () => import("@/views/Home.vue"),
      },
    ],
  },
  {
    path: "/login",
    component: () => import("@/views/Login.vue"),
  },
  {
    path: "/404",
    component: () => import("@/views/error/Page404.vue"),
  },
  { path: "/:pathMatch(.*)*", name: "not-found", redirect: "/404" },
]
