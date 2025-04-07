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

        async fetchPDF2ChemicalsResultFile(taskId) {
            const config = useRuntimeConfig()
            const { $axios } = useNuxtApp()
            const authStore = useAuthStore()

            let response = null

            if (authStore.token) {
                response = await $axios.get(
                    `${config.public.downloadPdf2ChemicalsResultFileEndpoint}${taskId}/`,
                    {
                        headers: { Authorization: `Bearer ${authStore.token}` },
                        responseType: "blob"
                    }
                )
            }

            return response.data
        },

        async downloadPDF2ChemicalsResultFile(taskId) {
            let fileData = await this.fetchPDF2ChemicalsResultFile(taskId)

            const blob = new Blob([fileData]);

            const downloadUrl = window.URL.createObjectURL(blob);

            const link = document.createElement("a");
            link.href = downloadUrl;
            link.download = `${taskId}.json`; // Define o nome do arquivo
            document.body.appendChild(link);
            link.click();

            document.body.removeChild(link);
            window.URL.revokeObjectURL(downloadUrl);
        },

        getFilenameFromDataFileUrl(dataFileUrl) {
            return dataFileUrl.split('/').at(-1);
        }
    },
    persist: true
})