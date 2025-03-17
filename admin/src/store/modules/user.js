import { getToken, removeToken } from "@/utils/auth.js"
import { getInfo } from "@/api/login.js"

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
            if (error === 401) {
              this.token = ""
              removeToken()
              this.userInfo = {}
            }
            reject(error)
          })
      })
    },
  },
})

export default useUserStore
