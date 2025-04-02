import { defineStore } from 'pinia';
import { useAuthStore } from './auth'

export const useUserTasksStore = defineStore('userTasksStore', {
    state: () => ({
        tasks: [],
        totalTasks: 0
    }),
    actions: {
        async fetchTasksPerUser(params = {}) {
            const config = useRuntimeConfig()
            const { $axios } = useNuxtApp()
            const authStore = useAuthStore()

            if (authStore.token) {
                await $axios.get(
                    config.public.userTasksEndpoint,
                    {
                        headers: { Authorization: `Bearer ${authStore.token}` },
                        params: params
                    }
                ).then((response) => {
                    this.tasks = response.data.results
                    this.totalTasks = response.data.count
                })
            }

        }
    },
    persist: true
})