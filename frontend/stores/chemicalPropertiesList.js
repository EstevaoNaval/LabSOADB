import { defineStore } from 'pinia'
import { useNuxtApp } from '#app'
import { useFilterStore } from './filterStore.js'
import roundValue from '~/utils/util'

export const useChemicalPropertiesListStore = defineStore('chemicalPropertiesList', {
    state: () => ({
        properties: {
            count_lipinski_violation: [],
            count_pains_alert: [],
            jplogp: [],
            molecular_weight: [],
            tpsa: [],
            mp_lower_bound: [],
            mp_upper_bound: [],
            h_bond_acceptor: [],
            h_bond_donor: [],
            heavy_atom: [],
            rotatable_bond: []
        }
    }),
    actions: {
        async fetchAllChemicalProperties() {
            const filterStore = useFilterStore()
            const { $axios } = useNuxtApp()

            const filters = filterStore.getFilterParams

            const params = {
                ...filters,
            }

            // Faz a requisição para o endpoint de propriedades
            const response = await $axios.get('/api/chemicals/prop-list/', {
                params: params
            })

            // Atualiza as listas de propriedades com os dados retornados pela API
            this.properties = {
                count_lipinski_violation: response.data.results.count_lipinski_violation.map(roundValue) || [],
                count_pains_alert: response.data.results.count_pains_alert.map(roundValue) || [],
                jplogp: response.data.results.jplogp.map(roundValue) || [],
                molecular_weight: response.data.results.molecular_weight.map(roundValue) || [],
                tpsa: response.data.results.tpsa.map(roundValue) || [],
                mp_lower_bound: response.data.results.mp_lower_bound.map(roundValue) || [],
                mp_upper_bound: response.data.results.mp_upper_bound.map(roundValue) || [],
                h_bond_acceptor: response.data.results.h_bond_acceptor.map(roundValue) || [],
                h_bond_donor: response.data.results.h_bond_donor.map(roundValue) || [],
                heavy_atom: response.data.results.heavy_atom.map(roundValue) || [],
                rotatable_bond: response.data.results.rotatable_bond.map(roundValue) || [],
            }

            // Atualiza o total de itens na store de paginação
            //paginationStore.setTotalItems(response.data.total_count)
        }
    },
    persist: true, // Persistência da store
})
