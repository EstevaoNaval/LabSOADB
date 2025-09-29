<template>
  <main>
    <div class="hidden lg:flex">
        <div class="dropdown dropdown-bottom dropdown-end m-auto">
          <div 
            tabindex="0" 
            role="button" 
            class="btn btn-ghost btn-primary text-xl font-semibold hover:text-primary"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
            </svg>
            <h1 class="text-xl">Export</h1> 
          </div>
          <ul tabindex="0" class="dropdown-content text-lg font-semibold menu bg-base-200 rounded-box z-[1] p-2 shadow w-32 relative overflow-hidden">
            <div
              v-if="loading"
              class="absolute inset-0 bg-base-200 bg-opacity-75 flex items-center justify-center rounded-box z-10"
            >
              <span class="loading loading-lg"></span>
            </div>

            <li
              @click="authStore.isAuthenticated ? startExport(option.id) : showLoginRequiredModal()"
              :class="{ 'cursor-not-allowed text-gray-400': !authStore.isAuthenticated, 'hover:text-primary': authStore.isAuthenticated }"
              class="transition-all"
              v-for="option in exportStore.exportFormats"
              :key="option.id"
              title="Login required"
            >
              <a class="flex items-center gap-1">
                <svg v-if="!authStore.isAuthenticated" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 text-slate-400">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 0 0 5.636 5.636m12.728 12.728A9 9 0 0 1 5.636 5.636m12.728 12.728L5.636 5.636" />
                </svg>

                {{ option.name }}
              </a>
            </li>

          </ul>
        </div>
    </div>
    <div class="hidden md:flex lg:hidden">
      <div class="dropdown dropdown-bottom dropdown-end m-auto">
        <div 
          tabindex="0" 
          role="button" 
          class="btn btn-ghost btn-primary font-semibold hover:text-primary"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
          </svg>
        </div>
        <ul tabindex="0" class="dropdown-content text-lg font-semibold menu bg-base-200 rounded-box z-[1] p-2 shadow w-32 relative overflow-hidden">
          <div
            v-if="loading"
            class="absolute inset-0 bg-base-200 bg-opacity-75 flex items-center justify-center rounded-box z-10"
          >
            <span class="loading loading-md"></span>
          </div>
          
          <li 
            @click="authStore.isAuthenticated ? startExport(option.id) : showLoginRequiredModal()" 
            :class="{ 'cursor-not-allowed text-gray-400': !authStore.isAuthenticated, 'hover:text-primary': authStore.isAuthenticated }"
            class="transition-all"
            v-for="option in exportStore.exportFormats" 
            :key="option.id"
            title="Login required"
          >
            <a class="flex items-center gap-1">
              <svg v-if="!authStore.isAuthenticated" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 text-slate-400">
                <path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 0 0 5.636 5.636m12.728 12.728A9 9 0 0 1 5.636 5.636m12.728 12.728L5.636 5.636" />
              </svg>
              {{ option.name }}
            </a>
          </li>
        </ul>
      </div>
    </div>
    <div class="flex md:hidden">
      <div class="dropdown dropdown-bottom dropdown-end m-auto">
        <div tabindex="0" role="button" class="btn btn-sm btn-ghost btn-primary font-semibold hover:text-primary">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
          </svg>
        </div>
        <ul tabindex="0" class="dropdown-content font-semibold menu bg-base-200 rounded-box z-[1] p-2 shadow w-32 relative overflow-hidden">
          <div
            v-if="loading"
            class="absolute inset-0 bg-base-200 bg-opacity-75 flex items-center justify-center rounded-box z-10"
          >
            <span class="loading loading-sm"></span>
          </div>
          
          <li 
            @click="authStore.isAuthenticated ? startExport(option.id) : showLoginRequiredModal()" 
            :class="{ 'cursor-not-allowed text-gray-400': !authStore.isAuthenticated, 'hover:text-primary': authStore.isAuthenticated }"
            class="transition-all"
            v-for="option in exportStore.exportFormats" 
            :key="option.id"
            title="Login required"
          >
            <a class="flex items-center gap-1">
              <svg v-if="!authStore.isAuthenticated" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5 text-slate-400">
                <path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 0 0 5.636 5.636m12.728 12.728A9 9 0 0 1 5.636 5.636m12.728 12.728L5.636 5.636" />
              </svg>
              {{ option.name }}
            </a>
          </li>
        </ul>
      </div>
    </div>
    <modal ref="exportLoginRequiredPromptRef">
      <LoginRequiredPrompt loginRequiredTo="Export Chemicals"></LoginRequiredPrompt>
    </modal>
  </main> 
</template>
  
<script setup>
  import StartExportSuccessToast from '~/components/StartExportSuccessToast.vue'
  import StartExportErrorToast from '~/components/StartExportErrorToast.vue'
  import Modal from '~/components/Modal.vue'

  import { useExportStore } from '~/stores/exportStore.js'
  import { useAuthStore } from '~/stores/auth.js'
  import pkg from 'vue-toastification'

  const { useToast } = pkg;

  const LoginRequiredPrompt = defineAsyncComponent({
    loader: () => import('~/components/LoginRequiredPrompt.vue')
  });

  // stores
  const authStore = useAuthStore()
  const exportStore = useExportStore()
  
  // refs
  const loading = ref(false)
  const exportLoginRequiredPromptRef = ref(null)

  async function startExport(export_format_id) {
    if (loading.value) return;
    loading.value = true;

    try {
      if (!authStore.isAuthenticated) return;

      exportStore.setCurrExportFormatId(export_format_id);

      const exportTaskId = await exportStore.startChemicalsExport();

      if (!exportTaskId) {
        showErrorToast();
        return;
      }

      showSuccessToast();
    } finally {
      loading.value = false;
    }
  }

  function showErrorToast() {
    let toast = useToast();

    toast.error(StartExportErrorToast, {
      icon: false,
      timeout: 8000,
    });
  }

  function showSuccessToast() {
    let toast = useToast();

    toast.success(StartExportSuccessToast, {
      icon: false,
      timeout: 8000,
    });
  }

  function showLoginRequiredModal() {
    if(exportLoginRequiredPromptRef.value) {
      exportLoginRequiredPromptRef.value.toggleComponentModal();
    }
  }

</script>
<style scoped>
    details > summary {
      list-style: none;
    }
    details > summary::-webkit-details-marker {
      display: none;
    }
</style>