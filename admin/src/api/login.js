import request from "@/utils/request"

export function login({ username, password }) {
  return request({
    url: "/system/v1/login",
    headers: {
      isToken: false,
    },
    method: "post",
    data: { username, password },
  })
}

export function getInfo() {
  return request({
    url: "/system/v1/user/info",
    method: "get",
  })
}
