import { name, version } from "@/../package.json"

const useAppStore = defineStore("app", {
  state: () => ({
    name,
    version,
  }),
})

export default useAppStore
