<template>
  <main>
    <div v-if="showMainModal" class="container mx-auto p-6 relative overflow-hidden">
      <div
        v-if="loading"
        class="absolute inset-0 bg-base-200 bg-opacity-85 flex items-center justify-center rounded-box z-10"
      >
        <span class="loading loading-lg"></span>
      </div>
      
      <h2 class="text-center text-2xl font-bold mb-6">PDF2Chemicals</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 mb-6 gap-4">
        <div class="mx-auto card bg-base-100 p-4 shadow">
          <p class="text-lg mb-2">Export Format</p>
          <div class="grid grid-cols-1">
            <label class="label cursor-pointer flex gap-2">
              <input type="radio" name="pdf2chemicals-export-format-radio" value="zip" v-model="exportFormatRadio" class="radio radio-primary" checked="checked" />
              <span class="label-text mr-auto ">ZIP</span>
            </label>
            <label class="label cursor-pointer flex gap-2">
              <input type="radio" name="pdf2chemicals-export-format-radio" value="json" v-model="exportFormatRadio" class="radio radio-primary" />
              <span class="label-text mr-auto ">JSON</span>
            </label>
          </div>
        </div>
        
        <div class="mx-auto card bg-base-100 p-4 shadow">
          <p class="text-lg mb-2">Conformations Format</p>
          <div v-if="exportFormatRadio === 'json'" class="text-sm text-gray-500 mb-2">Fixed to MOL2 for JSON export.</div>
          <div class="grid grid-cols-2">
            <label v-for="confsFormat in chemicalsConfsFormats" :key="confsFormat.id" class="label cursor-pointer flex gap-2">
              <input 
                :id="confsFormat.id"
                type="checkbox"
                :value="confsFormat.value" 
                v-model="chemicalsConfsFormatCheckbox"
                class="checkbox checkbox-primary"
                :disabled="exportFormatRadio === 'json'"
              />
              <span class="label-text mr-auto ">{{ confsFormat.label }}</span>
            </label>
          </div>
        </div>

        <div class="mx-auto card bg-base-100 p-4 shadow">
          <p class="text-lg mb-2">2D Structure Format</p>
          <div v-if="exportFormatRadio === 'json'" class="text-sm text-gray-500 mb-2">Fixed to SVG for JSON export.</div>
          <div class="grid grid-cols-2">
            <label v-for="chemical2DStructureFormat in chemicals2DStructureFormats" :key="chemical2DStructureFormat.id" class="label cursor-pointer flex gap-2">
              <input 
                type="checkbox" 
                :id="chemical2DStructureFormat.id"
                :value="chemical2DStructureFormat.value" 
                v-model="chemicals2DStructureFormatCheckbox" 
                class="checkbox checkbox-primary" 
                :disabled="exportFormatRadio === 'json'"
              />
              <span class="label-text mr-auto ">{{ chemical2DStructureFormat.label }}</span>
            </label>
          </div>
        </div>
      </div>
      
      <!-- Contêiner do Dashboard do Uppy -->
      <div ref="dashboardContainer" class="bg-base-300 rounded-lg p-4 mb-4"></div>
      
      <div class="grid grid-cols-2 my-auto items-center">
        <h2 class="text-left text-slate-500 text-sm md:text-md font-bold my-auto">* Limit of 10 PDF files per upload.</h2>
        <button @click="uploadFiles" class="btn btn-primary text-lg ml-auto">Upload</button>
      </div>

      <div v-if="uploadMessage" class="mt-4 alert" :class="{ 'alert-success': uploadSuccess, 'alert-error': !uploadSuccess }">
        {{ uploadMessage }}
      </div>
    </div>

    <LoginRequiredPrompt loginRequiredTo="PDF2Chemicals" v-if="showLoginPrompt" @close="showLoginPrompt = false"></LoginRequiredPrompt>
  </main>
</template>

<script setup>
import Uppy from '@uppy/core'
import Dashboard from '@uppy/dashboard'
import XHRUpload from '@uppy/xhr-upload'

import '@uppy/core/css/style.min.css';
import '@uppy/dashboard/css/style.min.css';

import { useThemeStore } from '~/stores/theme';
import { useAuthStore } from '~/stores/auth'

import LoginRequiredPrompt from '~/components/LoginRequiredPrompt.vue';

const config = useRuntimeConfig()

const themeStore = useThemeStore()
const authStore = useAuthStore()

const dashboardContainer = ref(null)

const loading = ref(false)
const uploadMessage = ref('')
const uploadSuccess = ref(false)

const showLoginPrompt = ref(false);
const showMainModal = ref(false);
const exportFormatRadio = ref('zip')
const chemicalsConfsFormatCheckbox = ref(['mol2'])
const chemicals2DStructureFormatCheckbox = ref(['jpg'])

const chemicalsConfsFormats = [
  {
    id: 'confsFormat-1',
    label: 'PDB',
    value: 'pdb'
  },
  {
    id: 'confsFormat-2',
    label: 'SDF',
    value: 'sdf'
  },
  {
    id: 'confsFormat-3',
    label: 'MOL2',
    value: 'mol2'
  },
  {
    id: 'confsFormat-4',
    label: 'SMI',
    value: 'smi'
  },
]

const chemicals2DStructureFormats = [
  {
    id: 'chemicals2DStructureFormat-1',
    label: 'PNG',
    value: 'png'
  },
  {
    id: 'chemicals2DStructureFormat-2',
    label: 'JPG',
    value: 'jpg'
  },
  {
    id: 'chemicals2DStructureFormat-3',
    label: 'SVG',
    value: 'svg'
  },
]

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
  autoProceed: false,
})

const uploadEndpoint = `${config.public.pdf2ChemicalsPDFSubmitEndpoint}`

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
    uppy.use(Dashboard, {
      target: dashboardContainer.value,
      inline: true,
      showProgressDetails: true,
      note: 'Drag PDF files or click to select',
      width: '100%',
      height: uppyDashboardHeight(),
      theme: themeStore.isDarkMode ? 'dark' : 'light',
      hideUploadButton: true
    })

    uppy.use(XHRUpload, {
      headers: uppyHeaders,
      formData: true,
      method: 'POST',
      endpoint: uploadEndpoint,
      fieldName: 'pdf_files'
    })

    // Add event listeners for better UX feedback
    uppy.on('upload-success', () => {
      uploadSuccess.value = true
      uploadMessage.value = 'Upload successful!'
    })

    uppy.on('upload-error', () => {
      uploadSuccess.value = false
      uploadMessage.value = 'Upload failed. Please try again.'
    })
  }
}

const uploadFiles = async () => {
  if (loading.value) return;
  loading.value = true;
  uploadMessage.value = ''

  try {
    setUppyUploadMeta()
    await uppy.upload()
  } finally {
    loading.value = false
  }
} 

const setUppyUploadMeta = () => {
  let uppyUploadMeta = {}

  uppyUploadMeta['export_format'] = exportFormatRadio.value

  if(chemicalsConfsFormatCheckbox.value.length > 0) {
    uppyUploadMeta['conf_format'] = chemicalsConfsFormatCheckbox.value
  }

  if(chemicals2DStructureFormatCheckbox.value.length > 0) {
    uppyUploadMeta['structure_format'] = chemicals2DStructureFormatCheckbox.value
  }

  uppy.setMeta(uppyUploadMeta);
}

watch(exportFormatRadio, (newVal) => {
  if (newVal === 'json') {
    chemicalsConfsFormatCheckbox.value = ['mol2']
    chemicals2DStructureFormatCheckbox.value = ['svg']
  }
  // No need for toggles; :disabled handles it
})

onBeforeMount(() => {
  checkAuth()
})

onMounted(() => {
  initializeUppy()
})

onBeforeUnmount(() => {
  if (uppy) uppy.destroy();
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