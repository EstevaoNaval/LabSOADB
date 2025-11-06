import { defineStore } from 'pinia';
import { getChemicalService } from '~/factories/chemicalServiceFactory'
import { useChemicalStore } from '~/stores/chemicalStore'
import { useChemicalSummaryStore } from '~/stores/chemicalSummaryStore'

export const useFetchChemicalStore = defineStore('fetchChemicalStore', {
    state: () => ({
        chemicals: [],
        totalChemicals: 0,
        loading: false,
        mode: 'summary',
        type: 'search',
        error: ''
    }),
    actions: {
        async fetchChemicals(params = {}) {
            this.loading = true

            const chemicalStore = useChemicalStore()
            const chemicalSummaryStore = useChemicalSummaryStore()

            // Chemical Search Service
            const chemicalService = getChemicalService(this.mode)

            try {
                switch (this.type) {
                    case 'search':
                        await chemicalService.fetchSearch(params)
                        break
                    case 'selected':
                        if (route.query.id) {
                            await chemicalService.fetchSelectedChemical()
                        }
                        break
                    case 'all':
                        await chemicalService.fetchAll(params)
                        break
                }
            } catch (err) {
                this.error = err.message
            }

            // Atualiza os dados para renderização
            if (this.error === '') {
                this.chemicals = this.mode === 'summary' ? chemicalSummaryStore.summaries : chemicalStore.chemicals
                this.totalChemicals = this.mode === 'summary' ? chemicalSummaryStore.totalSummaries : chemicalStore.totalChemicals
            } else {
                this.chemicals = []
            }

            this.error = ''
            this.loading = false;
        },

        setMode(mode) {
            this.mode = mode
        },

        setType(type) {
            this.type = type
        }
    }
});