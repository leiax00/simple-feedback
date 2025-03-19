import request from "@/utils/request.js"

/**
 * 获取设备归属列表
 // * @returns {Promise<Array>}
 */
export function getDeviceOwners() {
  return request({
    url: "/device/v1/owners",
    method: "get",
  })
}
