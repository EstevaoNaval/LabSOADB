// stores/authStore.js
import { defineStore } from 'pinia';
import { useAuthStore } from './auth';

export const useUserStore = defineStore('user', {
    state: () => ({
        user: null,
        error: null
    }),
    actions: {
        async fetchUserProfile() {
            const { $axios } = useNuxtApp()
            const config = useRuntimeConfig()

            const authStore = useAuthStore();

            if (authStore.token) {
                await $axios.get(
                    config.public.userProfileAPIEndpoint,
                    {
                        headers: { Authorization: `Bearer ${authStore.token}` }
                    }
                ).then((response) => {
                    this.clearUserProfile()
                    this.user = response.data
                })
            }
        },

        async resendEmail(email) {
            const { $axios } = useNuxtApp()
            const config = useRuntimeConfig()

            await $axios.post(
                config.public.resendEmailConfirmationAPIEndpoint,
                {
                    'email': email
                }
            ).catch((err) => {
                if (err.response) {
                    this.error = err.response.data
                } else if (err.request) {
                    this.error = { 'connection': 'Connection failed' }
                }
            })
        },

        async verifyEmail(verifyEmailKey) {
            const { $axios } = useNuxtApp()
            const config = useRuntimeConfig()

            await $axios.post(
                config.public.verifyEmailAPIEndpoint,
                {
                    'key': verifyEmailKey
                }
            ).catch((err) => {
                if (err.response) {
                    this.error = err.response.data
                } else if (err.request) {
                    this.error = { 'connection': 'Connection failed' }
                }
            })
        },

        async registerUser(userData) {
            const { $axios } = useNuxtApp()
            const config = useRuntimeConfig()

            await $axios.post(
                config.public.userRegisterAPIEndpoint,
                userData
            ).then((response) => {
                this.clearUserProfile()
            }).catch((err) => {
                if (err.response) {
                    this.error = err.response.data
                } else if (err.request) {
                    this.error = { 'connection': 'Connection failed' }
                }
            })
        },

        async deleteUser() {
            const { $axios } = useNuxtApp()
            const config = useRuntimeConfig()

            const authStore = useAuthStore();

            if (authStore.token) {
                await $axios.delete(
                    config.public.userAPIEndpoint,
                    {
                        headers: { Authorization: `Bearer ${authStore.token}` }
                    }
                ).then((response) => {
                    this.clearUserProfile()
                })
            }
        },

        clearUserProfile() {
            this.user = null
            this.error = null
        },

        clearError() {
            this.error = null
        }
    },
    persist: true
});
