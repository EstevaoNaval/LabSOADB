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

            return response
        },

        getFilenameFromContentDisposition(header) {
            // First, try to match filename* (RFC 5987, UTF-8 encoded)
            let filename = null;
            const filenameStarMatch = header.match(/filename\*\s*=\s*([^']*)''([^;]*)/i);
            if (filenameStarMatch && filenameStarMatch.length > 2) {
                filename = decodeURIComponent(filenameStarMatch[2]);
            } else {
                // Fallback: Try to match regular filename
                const filenameMatch = header.match(/filename\s*=\s*["']?([^"';]+)["']?/i);
                if (filenameMatch && filenameMatch.length > 1) {
                    filename = filenameMatch[1];
                }
            }
            return filename;
        },

        async downloadPDF2ChemicalsResultFile(taskId) {
            let response = await this.fetchPDF2ChemicalsResultFile(taskId)

            let filename = this.getFilenameFromContentDisposition(response.headers["content-disposition"])

            const blob = new Blob([response.data]);

            const downloadUrl = window.URL.createObjectURL(blob);

            const link = document.createElement("a");
            link.href = downloadUrl;
            link.download = filename; // Define o nome do arquivo
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