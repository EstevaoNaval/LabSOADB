import { defineStore } from 'pinia';
import { getChemicalService } from '~/factories/chemicalServiceFactory'
import { useChemicalStore } from '~/stores/chemicalStore'
import { useChemicalSummaryStore } from '~/stores/chemicalSummaryStore'

export const useFetchChemicalStore = defineStore('fetchChemicalStore', {
    state: () => ({
       chemicals: [],
       loading: false,
       mode: 'summary',
       type: 'search',
       error: ''
    }),
    actions: {
        async fetchChemicals() {
            this.loading = true

            const chemicalStore = useChemicalStore()
            const chemicalSummaryStore = useChemicalSummaryStore()

            // Chemical Search Service
            const chemicalService = getChemicalService(this.mode)
        
            try {    
                switch (this.type) {
                    case 'search':
                        await chemicalService.fetchSearch()
                        break
                    case 'selected':
                        if (route.query.id) {
                            await chemicalService.fetchSelectedChemical()
                        }
                        break
                    case 'all':
                        await chemicalService.fetchAll()
                }
            } catch (err) {
                this.error = err.message
            }

            // Atualiza os dados para renderização
            if(this.error === '') {
                this.chemicals = this.mode === 'summary' ? chemicalSummaryStore.summaries : chemicalStore.chemicals
            }else {
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
    },
    persist: true
});