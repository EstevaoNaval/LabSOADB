<!-- components/advanced-search/LiteratureFilters.vue -->
<template>
  <div class="card bg-base-100 shadow-lg border border-base-300">
    <div class="card-body p-4">
      <h3 class="card-title text-base mb-4 flex items-center gap-2">
        <DocumentTextIcon class="h-5 w-5" />
        Literature Filters
      </h3>
      
      <div class="space-y-4">
        <!-- DOI -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">DOI</span>
          </label>
          <input
            v-model="filterStore.filters.exact.doi"
            type="text"
            placeholder="10.1000/example"
            class="input input-bordered input-sm w-full"
          />
        </div>

        <!-- Title -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">Title</span>
          </label>
          <input
            v-model="filterStore.filters.exact.title"
            type="text"
            placeholder="Article title"
            class="input input-bordered input-sm w-full"
          />
        </div>

        <!-- Publication Date Range with Cally -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">Publication Date Range</span>
          </label>
          
          <div class="grid grid-cols-2 gap-2">
            <!-- From Date -->
            <div>
              <label class="label py-1">
                <span class="label-text text-xs">From</span>
              </label>
              <ClientOnly>
                <button
                  popovertarget="cally-from"
                  class="input input-bordered input-sm w-full text-left"
                  :id="'cally-from-btn'"
                  style="anchor-name: --cally-from"
                >
                  {{ formatDate(publicationDateFrom) || 'dd/mm/yyyy' }}
                </button>
                
                <div
                  popover
                  id="cally-from"
                  class="dropdown bg-base-100 rounded-box shadow-lg p-2"
                  style="position-anchor: --cally-from"
                >
                  <calendar-date
                    class="cally"
                    :value="publicationDateFrom"
                    @change="handleFromDateChange"
                  >
                    <svg 
                      aria-label="Previous" 
                      class="fill-current size-4" 
                      slot="previous" 
                      xmlns="http://www.w3.org/2000/svg" 
                      viewBox="0 0 24 24"
                    >
                      <path d="M15.75 19.5 8.25 12l7.5-7.5"></path>
                    </svg>
                    
                    <svg 
                      aria-label="Next" 
                      class="fill-current size-4" 
                      slot="next" 
                      xmlns="http://www.w3.org/2000/svg" 
                      viewBox="0 0 24 24"
                    >
                      <path d="m8.25 4.5 7.5 7.5-7.5 7.5"></path>
                    </svg>
                    
                    <calendar-month></calendar-month>
                  </calendar-date>
                </div>
              </ClientOnly>
            </div>

            <!-- To Date -->
            <div>
              <label class="label py-1">
                <span class="label-text text-xs">To</span>
              </label>
              <ClientOnly>
                <button
                  popovertarget="cally-to"
                  class="input input-bordered input-sm w-full text-left"
                  :id="'cally-to-btn'"
                  style="anchor-name: --cally-to"
                >
                  {{ formatDate(publicationDateTo) || 'dd/mm/yyyy' }}
                </button>
                
                <div
                  popover
                  id="cally-to"
                  class="dropdown bg-base-100 rounded-box shadow-lg p-2"
                  style="position-anchor: --cally-to"
                >
                  <calendar-date
                    class="cally"
                    :value="publicationDateTo"
                    @change="handleToDateChange"
                  >
                    <svg 
                      aria-label="Previous" 
                      class="fill-current size-4" 
                      slot="previous" 
                      xmlns="http://www.w3.org/2000/svg" 
                      viewBox="0 0 24 24"
                    >
                      <path d="M15.75 19.5 8.25 12l7.5-7.5"></path>
                    </svg>
                    
                    <svg 
                      aria-label="Next" 
                      class="fill-current size-4" 
                      slot="next" 
                      xmlns="http://www.w3.org/2000/svg" 
                      viewBox="0 0 24 24"
                    >
                      <path d="m8.25 4.5 7.5 7.5-7.5 7.5"></path>
                    </svg>
                    
                    <calendar-month></calendar-month>
                  </calendar-date>
                </div>
              </ClientOnly>
            </div>
          </div>

          <!-- Clear dates button -->
          <button
            v-if="publicationDateFrom || publicationDateTo"
            @click="clearDates"
            class="btn btn-ghost btn-xs mt-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="size-4" viewBox="0 0 16 16">
              <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z" />
            </svg>
            Clear dates
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useFilterStore } from '~/stores/filterStore'
import { DocumentTextIcon } from '@heroicons/vue/24/outline'

const filterStore = useFilterStore()

// Reactive date values
const publicationDateFrom = computed({
  get: () => filterStore.filters.range.publication_date.after,
  set: (val) => {
    filterStore.filters.range.publication_date.after = val
  }
})

const publicationDateTo = computed({
  get: () => filterStore.filters.range.publication_date.before,
  set: (val) => {
    filterStore.filters.range.publication_date.before = val
  }
})

// Format date for display
const formatDate = (dateString: string | null) => {
  if (!dateString) return null
  
  const date = new Date(dateString)
  return date.toLocaleDateString('pt-BR', { 
    year: 'numeric', 
    month: 'numeric', 
    day: 'numeric' 
  })
}

// Handle date changes from calendar
const handleFromDateChange = (event: Event) => {
  const target = event.target as any
  publicationDateFrom.value = target.value
  
  // Close popover
  const popover = document.getElementById('cally-from')
  if (popover) popover.hidePopover()
}

const handleToDateChange = (event: Event) => {
  const target = event.target as any
  publicationDateTo.value = target.value
  
  // Close popover
  const popover = document.getElementById('cally-to')
  if (popover) popover.hidePopover()
}

// Clear both dates
const clearDates = () => {
  publicationDateFrom.value = null
  publicationDateTo.value = null
}
</script>
