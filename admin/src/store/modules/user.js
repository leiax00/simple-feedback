import { getToken, removeToken, setToken } from "@/utils/auth.js"
import { getInfo, login } from "@/api/login.js"

const useUserStore = defineStore("user", {
  state: () => ({
    token: getToken(),
    userInfo: {},
  }),
  actions: {
    getInfo() {
      return new Promise((resolve, reject) => {
        getInfo()
          .then(res => {
            this.userInfo = res
            resolve(res)
          })
          .catch(error => {
            this.resetToken()
            reject(error)
          })
      })
    },
    login({ username, password }) {
      return new Promise((resolve, reject) => {
        login({ username: username.trim(), password: password })
          .then(({ access_token: accessToken, token_type: tokenType }) => {
            this.token = accessToken
            setToken(accessToken)
            resolve({ accessToken, tokenType })
          })
          .catch(error => {
            reject(error)
          })
      })
    },
    logout() {
      return new Promise(resolve => {
        this.resetToken()
        resolve()
      })
    },
    resetToken() {
      this.token = ""
      removeToken()
      this.userInfo = {}
    },
  },
})

export default useUserStore
