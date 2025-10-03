import { defineStore } from 'pinia';
import { useAuthStore } from './auth'

export const useUserChemicalsStore = defineStore('userChemicalsStore', {
    state: () => ({
        chemicals: [],
        totalChemicals: 0
    }),
    actions: {
        async fetchChemicalsPerUser(params = {}) {
            const config = useRuntimeConfig()
            const { $axios } = useNuxtApp()
            const authStore = useAuthStore()

            if (authStore.token) {
                await $axios.get(
                    config.public.userChemicalsEndpoint,
                    {
                        headers: { Authorization: `Bearer ${authStore.token}` },
                        params: params
                    }
                ).then((response) => {
                    this.chemicals = response.data.results
                    this.totalChemicals = response.data.count
                })
            }

        }
    },
    persist: true
})