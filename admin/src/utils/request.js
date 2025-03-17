import axios from "axios"
import { ElMessage } from "element-plus"
import { getToken } from "@/utils/auth"

axios.defaults.headers["Content-Type"] = "application/json;charset=utf-8"
// 创建axios实例
const service = axios.create({
  // axios中请求配置有baseURL选项，表示请求URL公共部分
  baseURL: import.meta.env.VITE_APP_BASE_API,
  // 超时
  timeout: 10000,
})

// request拦截器
service.interceptors.request.use(
  config => {
    // 是否需要设置 token
    const isToken = (config.headers || {}).isToken === false
    if (getToken() && !isToken) {
      config.headers["Authorization"] = "Bearer " + getToken() // 让每个请求携带自定义token 请根据实际情况自行修改
    }
    return config
  },
  error => {
    console.log(error)
    Promise.reject(error)
  },
)

// 响应拦截器
service.interceptors.response.use(
  res => {
    // 未设置状态码则默认成功状态
    const code = res.data.code || 200
    if (code === 200) {
      return Promise.resolve(res.data)
    } else {
      ElMessage({ message: res.data.msg, type: "error", duration: 5 * 1000 })
      return Promise.reject(new Error(res.data.msg || "Error"))
    }
  },
  error => {
    console.log(error)
    let { message } = error
    if (error.status === 401) {
      ElMessage({ message: error.response.data.detail, type: "error", duration: 5 * 1000 })
      if (error.config.url !== "/system/v1/user/info") {
        useRouter()
          .push({ path: "/login" })
          .then(() => {})
      }
    } else {
      ElMessage({ message: message, type: "error", duration: 5 * 1000 })
    }
    return Promise.reject(error.status)
  },
)

export default service
