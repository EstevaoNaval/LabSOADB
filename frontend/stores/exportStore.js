import { defineStore } from 'pinia';
import { useFilterStore } from './filterStore'
import { useAuthStore } from './auth';

export const useExportStore = defineStore('export', {
    state: () => ({
        currExportFormatId: 0,
        exportFormats: [
            {
                id: 0,
                name: 'CSV',
                value: 'csv'
            },
            {
                id: 1,
                name: 'XLSX',
                value: 'xlsx'
            },
            {
                id: 2,
                name: 'XLS',
                value: 'xls'
            },
            {
                id: 3,
                name: 'ODS',
                value: 'ods'
            },
            {
                id: 4,
                name: 'JSON',
                value: 'json'
            },
            {
                id: 5,
                name: 'HTML',
                value: 'html'

            }
        ]
    }),
    actions: {
        setCurrExportFormatId(exportFormatId) {
            this.currExportFormatId = exportFormatId
        },
        getCurrExportFormatValue() {
            return this.exportFormats[this.currExportFormatId]['value']
        },

        async fetchChemicalsExportDataFileUrl(exportTaskId) {
            const config = useRuntimeConfig()
            const { $axios } = useNuxtApp()

            const authStore = useAuthStore()

            let dataFileUrl = null

            while (dataFileUrl == null) {
                let response = await $axios.get(`${config.public.retrieveExportChemicalEndpoint}${exportTaskId}/`, {
                    headers: { Authorization: `Bearer ${authStore.token}` },
                })

                dataFileUrl = response.data.data_file
            }

            return dataFileUrl
        },
        async startChemicalsExportTask() {
            const config = useRuntimeConfig()
            const { $axios } = useNuxtApp()

            const filterStore = useFilterStore()
            const authStore = useAuthStore()

            let filters = filterStore.getFilterParams

            let params = {
                ...filters,
            }

            let response = await $axios.post(config.public.startExportChemicalEndpoint,
                {
                    file_format: this.getCurrExportFormatValue(),
                },
                {
                    params: params,
                    headers: { Authorization: `Bearer ${authStore.token}` },
                }
            )

            return response.data.id
        },
        async downloadChemicalsExport() {
            const exportTaskId = await this.startChemicalsExportTask()

            const dataFileUrl = await this.fetchChemicalsExportDataFileUrl(exportTaskId)

            const filename = this.getFilenameFromDataFileUrl(dataFileUrl)

            // create "a" HTML element with href to file & click
            const link = document.createElement('a');
            link.href = dataFileUrl;

            link.setAttribute('download', filename); //or any other extension
            document.body.appendChild(link);
            link.click();

            // clean up "a" element & remove ObjectURL
            document.body.removeChild(link);
        },
        getFilenameFromDataFileUrl(dataFileUrl) {
            return dataFileUrl.split('/').at(-1);
        }
    },
    persist: true
});