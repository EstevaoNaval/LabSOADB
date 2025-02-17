// https://nuxt.com/docs/api/configuration/nuxt-config
import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  ssr: true,
  target: 'server',

  generate: {
    routes: [
      '/about',
      '/pdf2chemicals/about',
      '/pdf2chemicals/features'
    ]
  },

  devtools: { enabled: true },

  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    'pinia-plugin-persistedstate/nuxt',
    '@nuxt/image',
  ],

  srcDir: './',

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
    '~/assets/css/collapse-animation.css'
  ],

  runtimeConfig: {
    public: {
      apiHost: process.env.API_URL_HOST,
      docsAPIEndpoint: process.env.DOCS_API_ENDPOINT,
      loginAPIEndpoint: process.env.LOGIN_API_ENDPOINT,
      logoutAPIEndpoint: process.env.LOGOUT_API_ENDPOINT,
      resetPasswordAPIEndpoint: process.env.RESET_PASSWORD_API_ENDPOINT,
      confirmResetPasswordAPIEndpoint: process.env.CONFIRM_RESET_PASSWORD_API_ENDPOINT,
      userProfileAPIEndpoint: process.env.USER_PROFILE_API_ENDPOINT,
      userRegisterAPIEndpoint: process.env.USER_REGISTER_API_ENDPOINT,
      downloadChemicalConformationsEndpoint: process.env.DOWNLOAD_CHEMICAL_CONFORMATIONS_ENPOINT,
      startExportChemicalEndpoint: process.env.START_EXPORT_CHEMICAL_ENDPOINT,
      retrieveExportChemicalEndpoint: process.env.RETRIEVE_EXPORT_CHEMICAL_ENDPOINT,
      verifyEmailAPIEndpoint: process.env.VERIFY_EMAIL_API_ENDPOINT,
      resendEmailConfirmationAPIEndpoint: process.env.RESEND_EMAIL_CONFIRMATION_API_ENDPOINT,
      pdf2ChemicalsPDFSubmitEndpoint: process.env.PDF2CHEMICALS_PDF_SUBMIT_ENDPOINT
    }
  },

  compatibilityDate: '2025-02-16'
})