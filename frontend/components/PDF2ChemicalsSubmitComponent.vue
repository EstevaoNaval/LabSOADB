<template>
  <main>
    <div v-if="showMainModal" class="container mx-auto p-6 relative overflow-hidden">
      <div
        v-if="loading"
        class="absolute inset-0 bg-base-200 bg-opacity-85 flex items-center justify-center rounded-box z-10"
      >
        <span class="loading loading-lg"></span>
      </div>
      
      <h2 class="text-center text-2xl font-bold mb-6">PDF2Chemicals: Submission Form</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 mb-6">
        <div class="mx-auto">
          <p class="text-lg">Export Format</p>
          <div class="grid grid-cols-1 mb-4">
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
        
        <div class="mx-auto">
          <p class="text-lg">Conformations Format</p>
          <div class="grid grid-cols-2 mb-4">
            <label v-for="confsFormat in chemicalsConfsFormats" :key="confsFormat.id" class="label cursor-pointer flex gap-2">
              <input 
                :id="confsFormat.id"
                type="checkbox"
                :value="confsFormat.value" 
                v-model="chemicalsConfsFormatCheckbox"
                class="checkbox checkbox-primary"
                required 
              />
              <span class="label-text mr-auto ">{{ confsFormat.label }}</span>
            </label>
          </div>
        </div>

        <div class="mx-auto">
          <p class="text-lg">2D Structure Format</p>
          <div class="grid grid-cols-2">
            <label v-for="chemical2DStructureFormat in chemicals2DStructureFormats" :key="chemical2DStructureFormat.id" class="label cursor-pointer flex gap-2">
              <input 
                type="checkbox" 
                :id="chemical2DStructureFormat.id"
                :value="chemical2DStructureFormat.value" 
                v-model="chemicals2DStructureFormatCheckbox" 
                class="checkbox checkbox-primary" 
                required
              />
              <span class="label-text mr-auto ">{{ chemical2DStructureFormat.label }}</span>
            </label>
          </div>
        </div>
      </div>
      
      <!-- Contêiner do Dashboard do Uppy -->
      <div ref="dashboardContainer" class="bg-base-300 rounded-lg p-4 mb-4"></div>
      
      <div class="grid grid-cols-2 my-auto">
        <h2 class="text-left text-slate-500 text-sm md:text-md font-bold my-auto">* Limit of 10 PDF files per upload.</h2>
        <button @click="uploadFiles" class="btn btn-primary text-lg ml-auto">Upload</button>
      </div>
    </div>

    <LoginRequiredPrompt loginRequiredTo="PDF2Chemicals" v-if="showLoginPrompt" @close="showLoginPrompt = false"></LoginRequiredPrompt>
  </main>
</template>

<script setup>
import Uppy from '@uppy/core'
import Dashboard from '@uppy/dashboard'
import XHRUpload from '@uppy/xhr-upload'

import { useThemeStore } from '~/stores/theme';
import { useAuthStore } from '~/stores/auth'

import LoginRequiredPrompt from '~/components/LoginRequiredPrompt.vue';

import '@uppy/core/dist/style.min.css';
import '@uppy/dashboard/dist/style.min.css';

const config = useRuntimeConfig()

const themeStore = useThemeStore()
const authStore = useAuthStore()

const dashboardContainer = ref(null)

const loading = ref(false)

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
    id: 'chemicals2DStructureFormat-3',
    label: 'JPG',
    value: 'jpg'
  },
  {
    id: 'chemicals2DStructureFormat-2',
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
  }
}

const uploadFiles = async () => {
  if (loading.value) return;
  loading.value = true;

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

  console.log(uppyUploadMeta)

  uppy.setMeta(uppyUploadMeta);
}

const setJsonConfsDefaultFormat = () => {
  chemicalsConfsFormatCheckbox.value = ['mol2']
}

const setJson2DStructureDefaultFormat = () => {
  chemicals2DStructureFormatCheckbox.value = ['svg']
}

const toggleConfsFormatCheckboxDisabled = () => {
  for (let i = 0; i < chemicalsConfsFormats.length; i++) {
    let confsFormatHTMLEntity = document.querySelector(`#${chemicalsConfsFormats[i].id}`)
    confsFormatHTMLEntity.disabled = !confsFormatHTMLEntity.disabled
  }
}

const toggle2DStructureFormatCheckboxDisabled = () => {
  for (let i = 0; i < chemicals2DStructureFormats.length; i++) {
    let chemical2DStructureFormatHTMLEntity = document.querySelector(`#${chemicals2DStructureFormats[i].id}`)
    chemical2DStructureFormatHTMLEntity.disabled = !chemical2DStructureFormatHTMLEntity.disabled
  }
}

onBeforeMount(() => {
  checkAuth()
})

onMounted(() => {
  initializeUppy()
})

onBeforeUnmount(() => {
  if (uppy) uppy.destroy();
})

watch(() => exportFormatRadio.value, () => {
  if(exportFormatRadio.value == 'json') {
    setJsonConfsDefaultFormat()
    setJson2DStructureDefaultFormat()
  }

  toggleConfsFormatCheckboxDisabled()
  toggle2DStructureFormatCheckboxDisabled()
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