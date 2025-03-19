import request from "@/utils/request.js"

export function getTopicList(params) {
  return request({
    url: "/message/v1/list/topic",
    params: params,
    method: "get",
  })
}

export function topicAllInList(params) {
  return request({
    url: "/message/v1/list/topic-all",
    params: params,
    method: "get",
  })
}

export function replyMsg(data) {
  return request({
    url: "/message/v1/new",
    data,
    method: "post",
  })
}
