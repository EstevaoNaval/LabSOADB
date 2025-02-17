<template>
    <div v-if="showMainModal" class="container mx-auto p-6 ">
      <h2 class="text-center text-2xl font-bold mb-4">Upload de Arquivos PDF</h2>
  
      <!-- Contêiner do Dashboard do Uppy -->
      <div ref="dashboardContainer" class="bg-base-300 rounded-lg p-4"></div>
    </div>

    <PDF2ChemicalsLoginPrompt v-if="showLoginPrompt" @close="showLoginPrompt = false"></PDF2ChemicalsLoginPrompt>
</template>

<script setup>
import Uppy from '@uppy/core'
import Dashboard from '@uppy/dashboard'
import XHRUpload from '@uppy/xhr-upload'

import { useThemeStore } from '~/stores/theme';
import { useAuthStore } from '~/stores/auth'
import { useUserStore } from '~/stores/user'

import PDF2ChemicalsLoginPrompt from '~/components/PDF2ChemicalsLoginPrompt.vue';

import '@uppy/core/dist/style.min.css';
import '@uppy/dashboard/dist/style.min.css';


const config = useRuntimeConfig()

const themeStore = useThemeStore()
const authStore = useAuthStore()
const userStore = useUserStore()

const dashboardContainer = ref(null)

const showLoginPrompt = ref(false);
const showMainModal = ref(false);

// Configuração do Uppy e estado dos arquivos
const uppy = new Uppy({
  restrictions: {
    maxNumberOfFiles: 10,
    allowedFileTypes: ['application/pdf'],
  },
  autoProceed: false, // Para só iniciar o upload quando o botão for clicado
})

const uploadEndpoint = `${config.public.apiHost}${config.public.pdf2ChemicalsPDFSubmitEndpoint}`

const uppyHeaders = {
  Authorization: `Bearer ${authStore.token}`,
}

const checkAuth = () => {
  if (!authStore.isAuthenticated) {
    showLoginPrompt.value = true;
  } else {
    showMainModal.value = true;
  }
};


const initializeUppy = () => {
  if(authStore.isAuthenticated) {
    // Inicializa o Dashboard dentro do contêiner
    uppy.use(Dashboard, {
      target: dashboardContainer.value,
      inline: true, // Exibe o Dashboard diretamente na página
      showProgressDetails: true,
      note: 'Drag PDF files or click to select',
      width: '100%',
      theme: themeStore.isDarkMode ? 'dark' : 'light'
    })

    uppy.use(XHRUpload, {
      headers: uppyHeaders,
      formData: true,
      method: 'POST',
      endpoint: uploadEndpoint,
      fieldName: 'pdf_files'
    })

    uppy.setMeta({ email: userStore.user.email });
  }
}

onBeforeMount(() => {
  checkAuth()
})

onMounted(() => {
  initializeUppy()
})

onBeforeUnmount(() => {
  uppy.destroy()
})
</script>

<style scoped>
.drag-drop-container {
  min-height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>