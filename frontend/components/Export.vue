<template>
    <div class="hidden lg:flex">
        <div class="dropdown dropdown-bottom dropdown-end m-auto">
          <div tabindex="0" role="button" class="btn btn-ghost btn-primary text-xl font-semibold hover:text-primary">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
            </svg>
            <h1 class="text-xl">Export</h1>
          </div>
          <ul tabindex="0" class="dropdown-content text-lg font-semibold menu bg-base-200 rounded-box z-[1] p-2 shadow w-32">
            <li @click="handleExport(option.id)" class="hover:text-primary" v-for="option in exportStore.exportFormats" :key="option.id">
              <a>{{ option.name }}</a>
            </li>
          </ul>
        </div>
    </div>
    <div class="hidden md:flex lg:hidden">
        <div class="dropdown dropdown-bottom dropdown-end m-auto">
          <div tabindex="0" role="button" class="btn btn-ghost btn-primary font-semibold hover:text-primary">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
            </svg>
          </div>
          <ul tabindex="0" class="dropdown-content text-lg font-semibold menu bg-base-200 rounded-box z-[1] p-2 shadow w-32">
            <li @click="handleExport(option.id)" class="hover:text-primary" v-for="option in exportStore.exportFormats" :key="option.id">
              <a>{{ option.name }}</a>
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
            <ul tabindex="0" class="dropdown-content font-semibold menu bg-base-200 rounded-box z-[1] p-2 shadow w-32">
                <li @click="handleExport(option.id)" class="hover:text-primary" v-for="option in exportStore.exportFormats" :key="option.id">
                  <a>{{ option.name }}</a>
                </li>
            </ul>
        </div>
    </div>
</template>
  
<script setup>
  import {useExportStore} from '~/stores/exportStore.js'
  import {useAuthStore} from '~/stores/auth.js'

  const authStore = useAuthStore()
  const exportStore = useExportStore()
  
  async function handleExport(export_format_id) {
    exportStore.setCurrExportFormatId(export_format_id)
    
    if(authStore.isAuthenticated) {
      await exportStore.downloadChemicalsExport()
    }else{
    
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