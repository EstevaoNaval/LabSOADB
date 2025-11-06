import { defineStore } from 'pinia'
import { useNuxtApp } from '#app'
import { useSortStore } from './sortingStore.js'
import { useFilterStore } from './filterStore.js'

export const useChemicalSummaryStore = defineStore('chemicalSummary', {
    state: () => ({
        summaries: [],
        totalSummaries: 0
    }),
    actions: {
        async fetchAllChemicalsSummary(params = {}) {
            const sortStore = useSortStore()
            const filterStore = useFilterStore()
            const { $axios } = useNuxtApp()

            const filters = filterStore.getFilterParams

            params = {
                ...params,
                ...filters,
                ordering: sortStore.getCurrSortOption(),
            }

            const response = await $axios.get('/api/chemicals/summary', {
                params: params
            })

            this.summaries = response.data.results
            this.totalSummaries = response.data.count
        },
        async fetchSearchSummary(params = {}) {
            const sortStore = useSortStore()
            const filterStore = useFilterStore()
            const { $axios } = useNuxtApp()

            const filters = filterStore.getFilterParams

            params = {
                ...params,
                ...filters,
                ordering: sortStore.getCurrSortOption(),
            }

            const response = await $axios.get('/api/chemicals/search/summary', {
                params: params
            })

            this.summaries = response.data.results
            this.totalSummaries = response.data.count
        }
    }
})
