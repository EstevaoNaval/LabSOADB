import { defineStore } from 'pinia';
import { useAuthStore } from './auth'

export const useUserTaskStore = defineStore('userTaskStore', {
    state: () => ({
        tasks: {},
    }),
    actions: {
        async fetchTasksPerUser() {
            const config = useRuntimeConfig()
            const { $axios } = useNuxtApp()
            const authStore = useAuthStore()

            if (authStore.token) {
                await $axios.get(
                    config.public.userTasksEndpoint,
                    {
                        headers: { Authorization: `Bearer ${authStore.token}` }
                    }
                ).then((response) => {
                    this.tasks = response.data.results
                })
            }

        }
    },
    persist: true
})