// /composables/usePassword.js
import { reactive } from 'vue';
import { useAuthStore } from '~/stores/auth';

export function usePassword() {
    const state = reactive({
        error: null
    });

    const changePasword = async (passwordData) => {
        const { $axios } = useNuxtApp()
        const config = useRuntimeConfig()

        const authStore = useAuthStore();

        await $axios.post(
            config.public.passwordChangeAPIEndpoint,
            passwordData,
            {
                headers: { Authorization: `Bearer ${authStore.token}` }
            }
        ).then((response) => {
            console.log("Corrigido")
            clearError();
        }).catch((err) => {
            if (err.response) {
                state.error = err.response.data
            } else if (err.request) {
                state.error = ['Connection failed']
            }
        });
    }

    const resetPassword = async (email) => {
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
            clearError();
        }).catch((err) => {
            if (err.response) {
                this.error = Object.values(err.response.data).flat(1)
            } else if (err.request) {
                this.error = ['Connection failed']
            }
        });
    };

    const confirmResetPassword = async (uid, token, new_passoword1, new_passoword2) => {
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
            clearError();
        }).catch((err) => {
            if (err.response) {
                this.error = Object.values(err.response.data).flat(1)
            } else if (err.request) {
                this.error = ['Connection failed']
            }
        });
    };

    const clearError = () => {
        state.error = null
    };

    return { state, changePasword, resetPassword, confirmResetPassword, clearError };
}
