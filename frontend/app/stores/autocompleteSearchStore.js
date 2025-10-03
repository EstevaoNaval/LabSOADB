import { defineStore } from 'pinia'
import { useNuxtApp } from '#app'

export const useAutocompleteSearchStore = defineStore('autocompleteSearch', {
    state: () => ({
        suggestions: [],
    }),
    actions: {
        async autocompleteSearch(query) {
            const { $axios } = useNuxtApp()

            const response = await $axios.get('/api/chemicals/autocomplete', { params: { query } })
            
            this.suggestions = response.data
        }
    },
    persist: true,
})
