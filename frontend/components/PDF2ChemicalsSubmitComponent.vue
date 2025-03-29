<template>
  <main>
    <div v-if="showMainModal" class="container mx-auto p-6 ">
      <h2 class="text-center text-2xl font-bold mb-6">PDF2Chemicals: Submission Form</h2>
      
      <div class="grid md:grid-cols-2 mb-6">
        <div>
          <p class="text-lg">Conformations Format</p>
          <div class="grid grid-cols-2 mb-4">
            <label class="label cursor-pointer flex gap-2">
              <input type="checkbox" required class="checkbox checkbox-primary" />
              <span class="label-text mr-auto ">PDB</span>
            </label>
            <label class="label cursor-pointer flex gap-2">
              <input type="checkbox" required class="checkbox checkbox-primary" />
              <span class="label-text mr-auto ">SDF</span>
            </label>
            <label class="label cursor-pointer flex gap-2">
              <input type="checkbox" required class="checkbox checkbox-primary" />
              <span class="label-text mr-auto ">SMI</span>
            </label>
            <label class="label cursor-pointer flex gap-2">
              <input type="checkbox" required class="checkbox checkbox-primary" />
              <span class="label-text mr-auto ">MOL2</span>
            </label>
          </div>
        </div>

        <div>
          <p class="text-lg">2D Structure Format</p>
          <div class="grid grid-cols-2">
            <label class="label cursor-pointer flex gap-2">
              <input type="checkbox" required class="checkbox checkbox-primary" />
              <span class="label-text mr-auto ">PNG</span>
            </label>
            <label class="label cursor-pointer flex gap-2">
              <input type="checkbox" required class="checkbox checkbox-primary" />
              <span class="label-text mr-auto ">SVG</span>
            </label>
            <label class="label cursor-pointer flex gap-2">
              <input type="checkbox" required class="checkbox checkbox-primary" />
              <span class="label-text mr-auto ">JPG</span>
            </label>
          </div>
        </div>
      </div>
      
      
      <!-- Contêiner do Dashboard do Uppy -->
      <div ref="dashboardContainer" class="bg-base-300 rounded-lg p-4 mb-4"></div>

      <h2 class="text-left text-slate-500 text-md font-bold ">* Limit of 10 PDF files per upload.</h2>
    </div>
  
    <PDF2ChemicalsLoginPrompt v-if="showLoginPrompt" @close="showLoginPrompt = false"></PDF2ChemicalsLoginPrompt>
  </main>
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
const uppyDashboardHeight = () => {
  const isMobile = window.innerWidth < 480;
  const isTablet = window.innerWidth < 768;

  return isMobile ? 250 : isTablet ? 300 : 400
}

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
      height: uppyDashboardHeight(),
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