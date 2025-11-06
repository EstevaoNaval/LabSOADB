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

        async startChemicalsExportTask() {
            const config = useRuntimeConfig()
            const { $axios } = useNuxtApp()

            const filterStore = useFilterStore()
            const authStore = useAuthStore()

            let filters = filterStore.getFilterParams

            let params = {
                ...filters,
            }

            try {
                let response = await $axios.post(config.public.startExportChemicalEndpoint,
                    {
                        file_format: this.getCurrExportFormatValue(),
                    },
                    {
                        params: params,
                        headers: {
                            Authorization: `Bearer ${authStore.token}`
                        },
                    }
                )

                return response.data.id
            } catch (err) {
                return null
            }
        },
        async startChemicalsExport() {
            const exportTaskId = await this.startChemicalsExportTask()

            return exportTaskId
        }
    },
    persist: {
        storage: piniaPluginPersistedstate.localStorage(), // ✅ Correto
        pick: ['currExportFormatId']
    }
});