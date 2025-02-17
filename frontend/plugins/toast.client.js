// plugins/toast.client.ts
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

export default defineNuxtPlugin((nuxtApp) => {
    const options = {
        // Configurações do toast, como duração, posição, etc.
        timeout: 5000,
        position: 'top-right',
        newestOnTop: true
    }
    nuxtApp.vueApp.use(Toast, options)
})
