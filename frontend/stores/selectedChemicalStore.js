import { defineStore } from 'pinia'
import { useNuxtApp } from '#app'

export const useSelectedChemicalStore = defineStore('selectedChemical', {
    state: () => ({
        selectedChemical: {},
        loading: true
    }),
    actions: {
        async fetchSelectedChemical(labsoadb_id) {
            this.loading = true

            const { $axios } = useNuxtApp()

            const response = await $axios.get(`/api/chemicals/${labsoadb_id}`)

            if (response.data) {
                this.selectedChemical = response.data
            }

            this.loading = false
        },

        getFirstPublicationDate() {
            let firstPublicationDate = new Date()

            for (let i = 0; i < this.selectedChemical.literature.length; i++) {
                let publicationDate = new Date(this.selectedChemical.literature[i].publication_date)

                if (publicationDate < firstPublicationDate) {
                    firstPublicationDate = publicationDate
                }
            }

            return firstPublicationDate
        },

        reset() {
            this.selectedChemical = {}
        }
    },
    persist: true,
})
