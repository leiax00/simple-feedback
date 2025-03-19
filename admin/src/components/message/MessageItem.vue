<script setup>
  import { replyMsg } from "@/api/message.js"
  import { PJ_MSG } from "@/utils/keys.js"
  import { ElMessage } from "element-plus"

  defineOptions({ name: "MessageItem" })
  const props = defineProps({
    messageItem: {
      type: Object,
      required: true,
    },
  })

  const { messageItem } = toRefs(props)
  const { replyMsgData, refreshMsg } = inject(
    PJ_MSG,
    () => ({
      replyMsgData: { msgId: 0 },
      refreshMsg: () => {},
    }),
    true,
  )

  const pageData = reactive({
    replying: false,
    replyForm: {},
  })

  const showReply = computed(() => {
    return replyMsgData.value && messageItem.value.msgId === replyMsgData.value.msgId
  })

  const replyInput = ref(null)
  const toReply = () => {
    if (showReply.value) {
      resetReply()
      return
    }
    replyMsgData.value = messageItem.value
    pageData.replyForm = {
      topId: messageItem.value.topId || messageItem.value.msgId,
      parentId: messageItem.value.msgId,
      deviceId: messageItem.value.deviceId,
      ownerId: messageItem.value.ownerId,
      content: "",
    }
    nextTick(replyInput.value.focus)
  }
  const toReplyMsg = () => {
    replyMsg(pageData.replyForm)
      .then(() => {
        ElMessage({ message: "Success to reply!", type: "success", duration: 5 * 1000 })
        resetReply()
        refreshMsg()
      })
      .catch(() => {
        ElMessage({ message: "Failed to reply!", type: "error", duration: 5 * 1000 })
      })
  }
  const resetReply = () => {
    replyMsgData.value = {}
    pageData.replyForm = {}
  }
</script>

<template>
  <div class="message-item-main">
    <div class="msg-title grow flex flex-row flex-wrap items-center justify-between">
      <div class="title-wrapper flex flex-row flex-wrap items-center gap-2">
        <div class="user flex flex-row items-center">
          <el-icon class="avatar"><UserFilled /></el-icon>
          <div class="ml-2 text-zinc-300 text-base">{{ messageItem.createBy }}</div>
        </div>
        <div class="text-zinc-400 text-base">{{ messageItem.createTime }}</div>
        <div class="reply flex flex-row items-center justify-center text-green-700 cursor-pointer" @click="toReply">
          <el-icon :size="20"><ChatSquare /></el-icon>
          <div class="text-base ml-0.5">Reply</div>
        </div>
      </div>
      <div class="meta-wrapper flex flex-row flex-wrap items-center gap-2">
        <div class="text-zinc-300 text-base flex flex-row flex-wrap gap-1">
          <div class="text-zinc-500">ID:</div>
          <div class="text-zinc-400">{{ messageItem.msgId }}</div>
        </div>
        <template v-if="messageItem.meta">
          <div
            v-for="key in Object.keys(messageItem.meta)"
            :key="key"
            class="text-zinc-300 text-base flex flex-row flex-wrap gap-1"
          >
            <div class="text-zinc-500">{{ key }}:</div>
            <div class="text-zinc-400 break-all">{{ messageItem.meta[key] }}</div>
          </div>
        </template>
      </div>
    </div>
    <div class="msg-content-wrapper mt-1 pl-6">
      <div class="text-zinc-300">{{ messageItem.content }}</div>
    </div>
    <div v-show="showReply" class="reply-wrapper mt-4 px-6">
      <el-form ref="replyForm" :model="pageData.replyForm">
        <el-form-item prop="content">
          <el-input
            ref="replyInput"
            v-model="pageData.replyForm.content"
            type="textarea"
            :autosize="{ minRows: 3, maxRows: 10 }"
          />
        </el-form-item>
        <el-form-item class="btn-wrapper">
          <el-button type="primary" @click="toReplyMsg">Reply</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
  .message-item-main {
    & + .message-item-main {
      margin-top: 24px;
    }
    min-height: 48px;
    :deep(.el-icon) {
      &.avatar {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background-color: var(--color-zinc-500);
      }
    }
  }
</style>
