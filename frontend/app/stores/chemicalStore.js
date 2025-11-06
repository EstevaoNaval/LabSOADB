import { defineStore } from 'pinia'
import { useNuxtApp } from '#app'
import { useSortStore } from './sortingStore.js'

export const useChemicalStore = defineStore('chemical', {
    state: () => ({
        chemicals: [],
        totalChemicals: 0
    }),
    actions: {
        async fetchAllChemicals(params = {}) {
            const sortStore = useSortStore()
            const { $axios } = useNuxtApp()

            params = {
                ...params,
                ordering: sortStore.getCurrSortOption(),
            }

            const response = await $axios.get('/api/chemicals', { params: params })

            this.chemicals = response.data.results
            this.totalChemicals = response.data.count
        },
        async fetchSearch(params = {}) {
            const sortStore = useSortStore()
            const { $axios } = useNuxtApp()

            params = {
                ...params,
                ordering: sortStore.getCurrSortOption(),
            }

            const response = await $axios.get('/api/chemicals/search', { params: params })

            this.chemicals = response.data.results
            this.totalChemicals = response.data.count
        }
    }
})
