// https://nuxt.com/docs/api/configuration/nuxt-config
import { defineNuxtConfig } from 'nuxt/config'
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  ssr: true,
  target: 'server',

  build: {
    transpile: ['vue-toastification']
  },

  generate: {
    routes: [
      '/about',
      '/pdf2chemicals/about',
      '/pdf2chemicals/features'
    ]
  },

  vite: {
    server: {
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path,
        },
        '/files': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path,
        }
      }
    },
    plugins: [
      tailwindcss()
    ]
  },

  nitro: {
    routeRules: {
      '/api/**': { 
        proxy: {
          to: `${process.env.NUXT_API_URL_HOST || 'http://django-api:8000'}/api/**`
        }
      },
      '/files/**': { 
        proxy: {
          to: `${process.env.NUXT_API_URL_HOST || 'http://django-api:8000'}/files/**`
        }
      }
    }
  },

  devtools: { enabled: true },

  devServer: {
    port: 3000,
    host: '0.0.0.0'
  },

  modules: [
    '@pinia/nuxt',
    'pinia-plugin-persistedstate/nuxt',
    '@nuxt/image',
    'nuxt-anchorscroll'
  ],

  piniaPluginPersistedstate: {
    storage: 'cookies', // Default para SSR
    cookieOptions: {
      sameSite: 'strict',
    },
    debug: false, // true para ver logs
  },

  srcDir: 'app/',

  plugins: [
    '~/plugins/axios.js',
    { src: '~/plugins/aos.client.js', ssr: false },
    { src: '~/plugins/toast.client.js', ssr: false },
    '~/plugins/close-details.js',
    '~/plugins/collapse-animation.js',
    '~/plugins/default-theme.js'
  ],

  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
    }
  },

  css: [
    '~/assets/css/collapse-animation.css',
    '~/assets/css/tailwind.css'
  ],

  anchorscroll: {
    hooks: ['page:finish'], // Default hook; triggers after page loads
  },

  runtimeConfig: {
    public: {
      // CRÍTICO: Deixe vazio para client-side usar paths relativos
      apiHost: '',

      // Para SSR (server-side dentro do container)
      apiHostServer: process.env.NUXT_PUBLIC_API_URL_HOST || 'http://django-api:8000',

      docsAPIEndpoint: process.env.NUXT_PUBLIC_DOCS_API_ENDPOINT,
      loginAPIEndpoint: process.env.NUXT_PUBLIC_LOGIN_API_ENDPOINT,
      logoutAPIEndpoint: process.env.NUXT_PUBLIC_LOGOUT_API_ENDPOINT,
      passwordChangeAPIEndpoint: process.env.NUXT_PUBLIC_PASSWORD_CHANGE_API_ENDPOINT,
      resetPasswordAPIEndpoint: process.env.NUXT_PUBLIC_RESET_PASSWORD_API_ENDPOINT,
      confirmResetPasswordAPIEndpoint: process.env.NUXT_PUBLIC_CONFIRM_RESET_PASSWORD_API_ENDPOINT,
      userProfileAPIEndpoint: process.env.NUXT_PUBLIC_USER_PROFILE_API_ENDPOINT,
      userRegisterAPIEndpoint: process.env.NUXT_PUBLIC_USER_REGISTER_API_ENDPOINT,
      downloadChemicalConformationsEndpoint: process.env.NUXT_PUBLIC_DOWNLOAD_CHEMICAL_CONFORMATIONS_ENPOINT,
      startExportChemicalEndpoint: process.env.NUXT_PUBLIC_START_EXPORT_CHEMICAL_ENDPOINT,
      retrieveExportChemicalEndpoint: process.env.NUXT_PUBLIC_RETRIEVE_EXPORT_CHEMICAL_ENDPOINT,
      verifyEmailAPIEndpoint: process.env.NUXT_PUBLIC_VERIFY_EMAIL_API_ENDPOINT,
      resendEmailConfirmationAPIEndpoint: process.env.NUXT_PUBLIC_RESEND_EMAIL_CONFIRMATION_API_ENDPOINT,
      pdf2ChemicalsPDFSubmitEndpoint: process.env.NUXT_PUBLIC_PDF2CHEMICALS_PDF_SUBMIT_ENDPOINT || '/api/pdf2chemicals/submit/',
      userTasksEndpoint: process.env.NUXT_PUBLIC_USER_TASKS_ENDPOINT,
      userChemicalsEndpoint: process.env.NUXT_PUBLIC_USER_CHEMICALS_ENDPOINT,
      taskRevokeEndpoint: process.env.NUXT_PUBLIC_TASK_REVOKE_ENDPOINT,
      downloadPdf2ChemicalsResultFileEndpoint: process.env.NUXT_PUBLIC_DOWNLOAD_PDF2CHEMICALS_RESULT_FILE_ENDPOINT
    }
  },

  compatibilityDate: '2025-02-16'
})