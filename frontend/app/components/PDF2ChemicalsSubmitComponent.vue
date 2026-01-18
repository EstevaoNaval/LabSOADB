<template>
  <main>
    <div v-if="showMainModal" class="container mx-auto p-4 md:p-6 relative">
      <!-- Loading Overlay with Backdrop Blur -->
      <Transition name="fade">
        <div v-if="loading"
          class="absolute inset-0 bg-base-200/90 backdrop-blur-sm flex flex-col items-center justify-center rounded-box z-10">
          <span class="loading loading-lg loading-spinner text-primary"></span>
          <p class="mt-4 text-sm font-medium">Processing your files...</p>
        </div>
      </Transition>

      <!-- Header Section -->
      <div class="text-center mb-8">
        <h1
          class="text-3xl md:text-4xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent mb-2">
          PDF2Chemicals
        </h1>
        <p class="text-sm md:text-base text-base-content/70">
          Extract chemical structures from PDF documents
        </p>
      </div>

      <!-- Configuration Cards -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        <!-- Export Format Card -->
        <div class="card bg-base-100 shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div class="card-body p-5">
            <div class="flex items-center gap-2 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 class="card-title text-lg">Export Format</h3>
            </div>
            <div class="space-y-2">
              <label class="flex items-center gap-3 p-3 rounded-lg hover:bg-base-200 transition-colors cursor-pointer">
                <input type="radio" name="export-format" value="zip" v-model="exportFormatRadio"
                  class="radio radio-primary radio-sm" />
                <div class="flex-1">
                  <span class="font-medium">ZIP Archive</span>
                  <p class="text-xs text-base-content/60">Compressed file bundle</p>
                </div>
              </label>
              <label class="flex items-center gap-3 p-3 rounded-lg hover:bg-base-200 transition-colors cursor-pointer">
                <input type="radio" name="export-format" value="json" v-model="exportFormatRadio"
                  class="radio radio-primary radio-sm" />
                <div class="flex-1">
                  <span class="font-medium">JSON</span>
                  <p class="text-xs text-base-content/60">Structured data format</p>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- Conformations Format Card -->
        <div class="card bg-base-100 shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div class="card-body p-5">
            <div class="flex items-center gap-2 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
              </svg>
              <h3 class="card-title text-lg">Conformations</h3>
            </div>
            <Transition name="fade">
              <div v-if="exportFormatRadio === 'json'" class="alert alert-info mb-3 py-2 text-xs">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                  class="stroke-current shrink-0 w-4 h-4">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>Fixed to MOL2 for JSON</span>
              </div>
            </Transition>
            <div class="grid grid-cols-2 gap-2">
              <label v-for="format in chemicalsConfsFormats" :key="format.id"
                class="flex items-center gap-2 p-2 rounded-lg hover:bg-base-200 transition-colors cursor-pointer"
                :class="{ 'opacity-50 cursor-not-allowed': exportFormatRadio === 'json' && format.value !== 'mol2' }">
                <input :id="format.id" type="checkbox" :value="format.value" v-model="chemicalsConfsFormatCheckbox"
                  class="checkbox checkbox-primary checkbox-sm" :disabled="exportFormatRadio === 'json'" />
                <span class="text-sm font-medium">{{ format.label }}</span>
              </label>
            </div>
          </div>
        </div>

        <!-- 2D Structure Format Card -->
        <div class="card bg-base-100 shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div class="card-body p-5">
            <div class="flex items-center gap-2 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <h3 class="card-title text-lg">2D Structure</h3>
            </div>
            <Transition name="fade">
              <div v-if="exportFormatRadio === 'json'" class="alert alert-info mb-3 py-2 text-xs">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                  class="stroke-current shrink-0 w-4 h-4">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>Fixed to SVG for JSON</span>
              </div>
            </Transition>
            <div class="grid grid-cols-2 gap-2">
              <label v-for="format in chemicals2DStructureFormats" :key="format.id"
                class="flex items-center gap-2 p-2 rounded-lg hover:bg-base-200 transition-colors cursor-pointer"
                :class="{ 'opacity-50 cursor-not-allowed': exportFormatRadio === 'json' && format.value !== 'svg' }">
                <input type="checkbox" :id="format.id" :value="format.value"
                  v-model="chemicals2DStructureFormatCheckbox" class="checkbox checkbox-primary checkbox-sm"
                  :disabled="exportFormatRadio === 'json'" />
                <span class="text-sm font-medium">{{ format.label }}</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Upload Area -->
      <div class="card bg-base-100 shadow-lg mb-4">
        <div class="card-body p-4">
          <div ref="dashboardContainer"></div>
        </div>
      </div>

      <!-- Action Bar -->
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 bg-base-100 rounded-lg shadow">
        <div class="flex items-center gap-2 text-sm text-base-content/70">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Maximum 10 PDF files per upload</span>
        </div>
        <button @click="uploadFiles" class="btn btn-primary btn-lg gap-2 min-w-[160px]" :disabled="loading">
          <svg v-if="!loading" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <span v-if="loading" class="loading loading-spinner loading-sm"></span>
          {{ loading ? 'Uploading...' : 'Upload Files' }}
        </button>
      </div>

      <!-- Status Messages -->
      <Transition name="slide-fade">
        <div v-if="uploadMessage" class="mt-4">
          <div class="alert shadow-lg" :class="uploadSuccess ? 'alert-success' : 'alert-error'">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none"
              viewBox="0 0 24 24">
              <path v-if="uploadSuccess" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ uploadMessage }}</span>
          </div>
        </div>
      </Transition>
    </div>

    <LoginRequiredPrompt loginRequiredTo="PDF2Chemicals" v-if="showLoginPrompt" @close="showLoginPrompt = false">
    </LoginRequiredPrompt>
  </main>
</template>

<script setup>
import Uppy from '@uppy/core'
import Dashboard from '@uppy/dashboard'
import XHRUpload from '@uppy/xhr-upload'

import '@uppy/core/css/style.min.css';
import '@uppy/dashboard/css/style.min.css';

import { navigateTo } from 'nuxt/app';

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
  if (authStore.isAuthenticated) {
    uppy.use(Dashboard, {
      target: dashboardContainer.value,
      inline: true,
      showProgressDetails: true,
      note: 'Drag PDF files here or click to browse',
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

    uppy.on('upload-success', () => {
      uploadSuccess.value = true
      uploadMessage.value = 'Upload successful! Your files are being processed.'
      setTimeout(() => {
        uploadMessage.value = ''
      }, 5000)
    })

    uppy.on('upload-error', (file, error) => {
      uploadSuccess.value = false
      uploadMessage.value = error?.message || 'Upload failed. Please try again.'
      setTimeout(() => {
        uploadMessage.value = ''
      }, 5000)
    })
  }
}

const uploadFiles = async () => {
  if (loading.value) return;

  const fileCount = uppy.getFiles().length
  if (fileCount === 0) {
    uploadSuccess.value = false
    uploadMessage.value = 'Please select at least one PDF file to upload.'
    setTimeout(() => {
      uploadMessage.value = ''
    }, 3000)
    return
  }

  loading.value = true;
  uploadMessage.value = ''

  try {
    setUppyUploadMeta()
    await uppy.upload()

    closeModal()
    navigateTo('/dashboard#user-task-table')
  } finally {
    loading.value = false
  }
}

const setUppyUploadMeta = () => {
  let uppyUploadMeta = {}

  uppyUploadMeta['export_format'] = exportFormatRadio.value

  if (chemicalsConfsFormatCheckbox.value.length > 0) {
    uppyUploadMeta['conf_format'] = chemicalsConfsFormatCheckbox.value
  }

  if (chemicals2DStructureFormatCheckbox.value.length > 0) {
    uppyUploadMeta['structure_format'] = chemicals2DStructureFormatCheckbox.value
  }

  uppy.setMeta(uppyUploadMeta);
}

const closeModal = inject('closeModal')

watch(exportFormatRadio, (newVal) => {
  if (newVal === 'json') {
    chemicalsConfsFormatCheckbox.value = ['mol2']
    chemicals2DStructureFormatCheckbox.value = ['svg']
  }
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
/* Smooth Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from {
  transform: translateY(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
</style>