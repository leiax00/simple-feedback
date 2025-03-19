<script setup>
  defineOptions({ name: "Message" })

  const props = defineProps({
    message: {
      type: Object,
      required: true,
    },
  })
  const { message } = toRefs(props)
</script>

<template>
  <div class="message-main">
    <div class="first-msg">
      <MessageItem :message-item="message.info" />
    </div>
    <div v-if="message.subs.length > 1" class="subs-msg pl-6 mt-6">
      <template v-for="item in message.subs">
        <MessageItem
          v-if="message.info.msgId !== item.msgId"
          :key="item.msgId"
          :message-item="item"
          class="sub-msg-item"
        />
      </template>
    </div>
  </div>
</template>

<style scoped>
  .message-main {
    & + .message-main {
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid var(--color-zinc-500);
    }
  }
</style>
