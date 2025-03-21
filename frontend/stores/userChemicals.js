import { defineStore } from 'pinia';
import { useAuthStore } from './auth'

export const useUserChemicalsStore = defineStore('userChemicalsStore', {
    state: () => ({
        chemicals: {},
    }),
    actions: {
        async fetchChemicalsPerUser() {
            const config = useRuntimeConfig()
            const { $axios } = useNuxtApp()
            const authStore = useAuthStore()

            if (authStore.token) {
                await $axios.get(
                    config.public.userChemicalsEndpoint,
                    {
                        headers: { Authorization: `Bearer ${authStore.token}` }
                    }
                ).then((response) => {
                    this.chemicals = response.data.results
                })
            }

        }
    },
    persist: true
})