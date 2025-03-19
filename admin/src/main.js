import { createApp } from "vue"
import "element-plus/dist/index.css"
import "./style.css"
import App from "./App.vue"
import router from "@/router"
import store from "@/store"
import { UserFilled, ChatSquare } from "@element-plus/icons-vue"

const app = createApp(App)
app.component("UserFilled", UserFilled)
app.component("ChatSquare", ChatSquare)
app.use(router).use(store).mount("#app")
