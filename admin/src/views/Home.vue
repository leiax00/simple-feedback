<script setup>
  import { getDeviceOwners } from "@/api/device.js"
  import { topicAllInList } from "@/api/message.js"
  import { PJ_MSG } from "@/utils/keys.js"

  defineOptions({ name: "Home" })

  const pageData = reactive({
    curOwner: null,
    msgs: [],
    replyMsgData: {},
  })

  const ownerTreeProps = {
    children: "children",
    label: "ownerName",
  }
  const ownerTree = ref([])
  const loadOwners = () => {
    getDeviceOwners().then(({ data: owners }) => {
      const map = {}
      const tree = []

      for (const item of owners) {
        map[item.ownerId] = { ...item, children: [] }
      }
      for (const item of owners) {
        const node = map[item.ownerId]
        if (item.parentId === 0) {
          tree.push(node)
        } else {
          const parent = map[item.parentId]
          if (parent) {
            parent.children.push(node)
          } else {
            tree.push(node)
          }
        }
      }
      console.log(tree)
      ownerTree.value = tree
    })
  }

  const onOwnerClick = data => {
    console.log(data.ownerName)
    pageData.curOwner = data.parentId !== 0 ? data : null
    if (data.parentId !== 0) {
      pageData.curOwner = data
      loadOwnerTopics()
    }
  }

  const loadOwnerTopics = () => {
    topicAllInList({ ownerId: pageData.curOwner.ownerId }).then(({ rows }) => {
      console.log(rows)
      pageData.msgs = rows
    })
  }

  provide(PJ_MSG, {
    replyMsgData: pageData.replyMsgData,
    refreshMsg: loadOwnerTopics,
  })
  onMounted(() => {
    loadOwners()
  })
</script>

<template>
  <div class="px-6 grow flex flex-col sm:flex-row gap-6">
    <div
      class="w-full sm:w-5/12 md:w-4/12 lg:w-3/12 border border-solid dark:border-zinc-700 rounded-md sm:mb-6 p-3 lg:p-6"
    >
      <el-tree
        accordion
        :expand-on-click-node="false"
        :default-expand-all="true"
        :data="ownerTree"
        :props="ownerTreeProps"
        @node-click="onOwnerClick"
      />
    </div>
    <div
      class="flex flex-col w-full sm:w-7/12 md:w-8/12 lg:w-9/12 border border-solid dark:border-zinc-700 rounded-md sm:mb-6 p-3 lg:p-6"
    >
      <div v-if="pageData.curOwner" class="grow msg-wrapper flex flex-col">
        <div class="owner-name text-xl">{{ pageData.curOwner.ownerName }}</div>
        <div class="msg-wrapper flex flex-col mt-8">
          <Message v-for="msg in pageData.msgs" :key="msg.info.msgId" :message="msg" />
        </div>
      </div>
      <div v-else class="grow msg-wrapper flex flex-col items-center justify-center">
        <div class="msg-title text-xl text-zinc-500">Please select one product type!</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
  :deep(.el-tree) {
    --el-fill-color-blank: var(--color-zinc-800);
    --el-tree-node-content-height: 26px;
    --el-tree-node-hover-bg-color: var(--color-zinc-700);
    --el-tree-text-color: var(--color-zinc-300);
    --el-tree-expand-icon-color: var(--el-text-color-placeholder);
  }

  :deep(.el-collapse) {
    --el-fill-color-blank: var(--color-zinc-700);
    --el-border-color-lighter: var(--color-zinc-500);

    .el-collapse-item {
      .el-collapse-item__header {
        height: unset;
        min-height: var(--el-collapse-header-height);
        padding-left: 24px;

        .el-icon {
          --color: var(--color-zinc-300);
        }
      }
    }
  }

  .msg-wrapper {
    .msg-item {
      & + .msg-item {
        margin-top: 24px;
      }

      .msg-title {
        .meta-item {
          & + .meta-item {
            margin-left: 20px;
          }
        }
      }
    }
  }
</style>
