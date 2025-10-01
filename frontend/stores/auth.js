// stores/authStore.js
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: null,
        isAuthenticated: false,
        error: []
    }),
    actions: {
        async login(email, password) {
            const { $axios } = useNuxtApp()
            const config = useRuntimeConfig()

            console.log(config.public.loginAPIEndpoint)

            await $axios.post(
                config.public.loginAPIEndpoint,
                {
                    username: email,
                    password: password
                }
            ).then(
                (response) => {
                    this.token = response.data.token;
                    this.isAuthenticated = true;
                    this.error = []
                }
            ).catch(
                (err) => {
                    if (err.response) {
                        this.error = Object.values(err.response.data).flat(1)
                    } else if (err.request) {
                        this.error = ['Connection failed']
                    }
                }
            );
        },

        async resetPassword(email) {
            const { $axios } = useNuxtApp()
            const config = useRuntimeConfig()

            await $axios.post(
                config.public.resetPasswordAPIEndpoint,
                {
                    email: email
                }
            ).then((response) => {
                this.token = null;
                this.isAuthenticated = false;
                this.error = [];
            }).catch((err) => {
                if (err.response) {
                    this.error = Object.values(err.response.data).flat(1)
                } else if (err.request) {
                    this.error = ['Connection failed']
                }
            });
        },

        async confirmResetPassword(uid, token, new_passoword1, new_passoword2) {
            const { $axios } = useNuxtApp()
            const config = useRuntimeConfig()

            await $axios.post(
                config.public.confirmResetPasswordAPIEndpoint,
                {
                    uid: uid,
                    token: token,
                    new_passoword1: new_passoword1,
                    new_passoword2: new_passoword2
                }
            ).then((response) => {
                this.token = null;
                this.isAuthenticated = false;
                this.error = [];
            }).catch((err) => {
                if (err.response) {
                    this.error = Object.values(err.response.data).flat(1)
                } else if (err.request) {
                    this.error = ['Connection failed']
                }
            });
        },

        async logout() {
            const { $axios } = useNuxtApp()
            const config = useRuntimeConfig()

            await $axios.post(
                config.public.logoutAPIEndpoint,
                {},
                {
                    headers: { Authorization: `Bearer ${this.token}` }
                }
            ).then((response) => {
                this.token = null;
                this.isAuthenticated = false;
                this.error = [];
            }).catch((err) => {
                if (err.response) {
                    this.error = Object.values(err.response.data).flat(1)
                } else if (err.request) {
                    this.error = ['Connection failed']
                }
            });
        },

        clearError() {
            this.error = []
        }
    },
    persist: true
});
