<template>
  <main>
    <!-- Desktop View -->
    <div class="hidden lg:flex">
      <div class="dropdown dropdown-bottom dropdown-end">
        <div ref="exportButtonDesktop" tabindex="0" role="button" class="btn btn-outline btn-primary gap-2"
          :aria-label="loading ? 'Exporting...' : 'Export data'">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
          </svg>
          <span>Export</span>
          <span v-if="loading" class="loading loading-spinner loading-xs"></span>
        </div>

        <ul tabindex="0"
          class="dropdown-content menu bg-base-100 rounded-box z-10 mt-2 p-2 shadow-xl border border-base-300 w-52">
          <!-- Header -->
          <div class="px-3 py-2 border-b border-base-300 mb-1">
            <p class="font-semibold text-sm">Export Format</p>
          </div>

          <!-- Export Options -->
          <li v-for="option in exportStore.exportFormats" :key="option.id">
            <button @click="handleExport(option.id, 'desktop')" :disabled="!authStore.isAuthenticated || loading"
              class="flex items-center justify-between group" :class="{
                'opacity-60': !authStore.isAuthenticated || loading
              }">
              <span class="font-medium">{{ option.name }}</span>

              <div v-if="!authStore.isAuthenticated" class="tooltip tooltip-left" data-tip="Login required">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="w-4 h-4 text-warning">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
                </svg>
              </div>

              <svg v-else-if="loading && loadingFormat === option.id" class="w-4 h-4 animate-spin text-primary"
                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
            </button>
          </li>

          <!-- Footer Message -->
          <div v-if="!authStore.isAuthenticated" class="px-3 py-2 mt-1 border-t border-base-300 bg-base-200 rounded-lg">
            <div class="flex items-start gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="w-4 h-4 mt-0.5 text-info flex-shrink-0">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
              </svg>
              <div>
                <p class="text-xs font-medium text-base-content/90">Login Required</p>
                <p class="text-xs text-base-content/70 mt-0.5">
                  Please
                  <NuxtLink to="/auth/login" class="link link-primary">login</NuxtLink>
                  to export chemicals
                </p>
              </div>
            </div>
          </div>
        </ul>
      </div>
    </div>

    <!-- Mobile/Tablet View -->
    <div class="flex lg:hidden">
      <div class="dropdown dropdown-bottom dropdown-start">
        <div ref="exportButtonMobile" tabindex="0" role="button" class="btn btn-sm btn-outline btn-primary gap-2"
          :aria-label="loading ? 'Exporting...' : 'Export data'">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
          </svg>
          <span class="hidden md:inline">Export</span>
          <span v-if="loading" class="loading loading-spinner loading-xs"></span>
        </div>

        <ul tabindex="0"
          class="dropdown-content menu bg-base-100 rounded-box z-10 mt-2 p-2 shadow-xl border border-base-300 w-52">
          <!-- Header -->
          <div class="px-3 py-2 border-b border-base-300 mb-1">
            <p class="font-semibold text-sm">Export Format</p>
          </div>

          <!-- Export Options -->
          <li v-for="option in exportStore.exportFormats" :key="option.id">
            <button @click="handleExport(option.id, 'mobile')" :disabled="!authStore.isAuthenticated || loading"
              class="flex items-center justify-between group" :class="{
                'opacity-60': !authStore.isAuthenticated || loading
              }">
              <span class="font-medium">{{ option.name }}</span>

              <div v-if="!authStore.isAuthenticated" class="tooltip tooltip-left" data-tip="Login required">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="w-4 h-4 text-warning">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
                </svg>
              </div>

              <svg v-else-if="loading && loadingFormat === option.id" class="w-4 h-4 animate-spin text-primary"
                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
            </button>
          </li>

          <!-- Footer Message -->
          <div v-if="!authStore.isAuthenticated" class="px-3 py-2 mt-1 border-t border-base-300 bg-base-200 rounded-lg">
            <div class="flex items-start gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="w-4 h-4 mt-0.5 text-info flex-shrink-0">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
              </svg>
              <div>
                <p class="text-xs font-medium text-base-content/90">Login Required</p>
                <p class="text-xs text-base-content/70 mt-0.5">
                  Please
                  <NuxtLink to="/auth/login" class="link link-primary">login</NuxtLink>
                  to export
                </p>
              </div>
            </div>
          </div>
        </ul>
      </div>
    </div>

    <!-- Login Required Modal (fallback) -->
    <Modal ref="exportLoginRequiredPromptRef">
      <LoginRequiredPrompt loginRequiredTo="Export Chemicals" />
    </Modal>
  </main>
</template>

<script setup>
import { ref, defineAsyncComponent } from 'vue'
import { useExportStore } from '~/stores/exportStore'
import { useAuthStore } from '~/stores/auth'
import { useToast } from 'vue-toastification'
import { navigateTo } from 'nuxt/app';
import Modal from '~/components/Modal.vue'

import StartExportSuccessToast from '~/components/StartExportSuccessToast.vue'
import StartExportErrorToast from '~/components/StartExportErrorToast.vue'

const LoginRequiredPrompt = defineAsyncComponent({
  loader: () => import('~/components/LoginRequiredPrompt.vue')
})

// Stores
const authStore = useAuthStore()
const exportStore = useExportStore()
const toast = useToast()

// Refs
const loading = ref(false)
const loadingFormat = ref(null)
const exportLoginRequiredPromptRef = ref(null)
const exportButtonDesktop = ref(null)
const exportButtonMobile = ref(null)

// Functions
function toggleExportButtonDisableAttr(view) {
  const button = view === 'desktop' ? exportButtonDesktop.value : exportButtonMobile.value

  if (!button) return

  if (loading.value) {
    button.setAttribute('disabled', true)
  } else {
    button.removeAttribute('disabled')
  }
}

async function handleExport(exportFormatId, view) {
  if (!authStore.isAuthenticated) {
    showLoginRequiredModal()
    return
  }

  if (loading.value) return

  loading.value = true
  loadingFormat.value = exportFormatId
  toggleExportButtonDisableAttr(view)

  try {
    exportStore.setCurrExportFormatId(exportFormatId)
    const exportTaskId = await exportStore.startChemicalsExport()

    if (!exportTaskId) {
      showErrorToast()
      return
    }

    showSuccessToast()

    // Close dropdown after successful export
    const button = view === 'desktop' ? exportButtonDesktop.value : exportButtonMobile.value
    if (button) {
      button.blur()
    }

    navigateTo('/dashboard#user-task-table')
  } catch (error) {
    console.error('Export error:', error)
    showErrorToast()
  } finally {
    loading.value = false
    loadingFormat.value = null
    toggleExportButtonDisableAttr(view)
  }
}

function showErrorToast() {
  toast.error(StartExportErrorToast, {
    icon: false,
    timeout: 8000
  })
}

function showSuccessToast() {
  toast.success(StartExportSuccessToast, {
    icon: false,
    timeout: 8000
  })
}

function showLoginRequiredModal() {
  if (exportLoginRequiredPromptRef.value) {
    exportLoginRequiredPromptRef.value.toggleComponentModal()
  }
}
</script>