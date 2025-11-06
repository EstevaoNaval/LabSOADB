import qs from 'qs';

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

            if (!authStore.token) {
                return
            }

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
        },
        async revokeTask(taskId) {
            const config = useRuntimeConfig()
            const { $axios } = useNuxtApp()
            const authStore = useAuthStore()

            if (authStore.token) {
                await $axios.post(
                    config.public.taskRevokeEndpoint,
                    {
                        'task_id': taskId
                    },
                    {
                        headers: { Authorization: `Bearer ${authStore.token}` },
                    }
                )
            }
        },
        async getTotalSuccessfulTasks() {
            const config = useRuntimeConfig()
            const { $axios } = useNuxtApp()
            const authStore = useAuthStore()

            let totalSuccessfulTasks = 0

            let params = {
                status: 'SUCCESS'
            }

            await $axios.get(
                config.public.userTasksEndpoint,
                {
                    headers: { Authorization: `Bearer ${authStore.token}` },
                    params: params,
                }
            ).then((response) => {
                totalSuccessfulTasks = response.data.count
            })

            return totalSuccessfulTasks
        },
        async getTotalPendingTasks() {
            const config = useRuntimeConfig()
            const { $axios } = useNuxtApp()
            const authStore = useAuthStore()

            let totalPendingTasks = 0

            let params = {
                status: ['PENDING', 'RETRY'],
            }

            await $axios.get(
                config.public.userTasksEndpoint,
                {
                    headers: { Authorization: `Bearer ${authStore.token}` },
                    params: params,
                }
            ).then((response) => {
                totalPendingTasks = response.data.count
            })

            return totalPendingTasks
        },
        async getTotalFailedTasks() {
            const config = useRuntimeConfig()
            const { $axios } = useNuxtApp()
            const authStore = useAuthStore()

            let totalFailedTasks = 0

            let params = {
                status: 'FAILURE'
            }

            await $axios.get(
                config.public.userTasksEndpoint,
                {
                    headers: { Authorization: `Bearer ${authStore.token}` },
                    params: params,
                }
            ).then((response) => {
                totalFailedTasks = response.data.count
            })

            return totalFailedTasks
        }
    }
})