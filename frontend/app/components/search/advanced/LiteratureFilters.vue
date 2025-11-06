<!-- components/advanced-search/LiteratureFilters.vue -->
<template>
  <div class="space-y-6">
    <!-- Active Filters Badges -->
    <div v-if="activeFiltersCount > 0" class="flex flex-wrap gap-2">
      <div 
        v-for="filter in activeFiltersList" 
        :key="filter.key"
        class="badge badge-primary gap-2 px-3 py-2"
      >
        <span class="text-xs font-medium">{{ filter.label }}: {{ filter.value }}</span>
        <button 
          type="button" 
          @click="clearFilter(filter.key)"
          class="btn btn-ghost btn-xs btn-circle hover:bg-primary-content"
        >
          <XMarkIcon class="h-3 w-3" />
        </button>
      </div>
    </div>

    <!-- Filters Card -->
    <div class="card bg-base-200 shadow-sm">
      <div class="card-body p-4 space-y-4">
        <!-- DOI -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium flex items-center gap-2">
              <DocumentTextIcon class="h-4 w-4" />
              DOI
            </span>
          </label>
          <input
            v-model="doi"
            @input="debouncedUpdate"
            type="text"
            placeholder="10.1000/example"
            class="input input-bordered input-sm w-full"
          />
        </div>

        <!-- Title -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium flex items-center gap-2">
              <DocumentTextIcon class="h-4 w-4" />
              Title
            </span>
          </label>
          <input
            v-model="title"
            @input="debouncedUpdate"
            type="text"
            placeholder="Article title"
            class="input input-bordered input-sm w-full"
          />
        </div>

        <!-- Publication Date Range -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium flex items-center gap-2">
              <CalendarIcon class="h-4 w-4" />
              Publication Date Range
            </span>
          </label>
          
          <div class="grid grid-cols-2 gap-2">
            <!-- From Date -->
            <div>
              <label class="label py-1">
                <span class="label-text text-xs">From</span>
              </label>
              <input
                v-model="publicationDateFrom"
                @change="handleDateChange"
                type="date"
                class="input input-bordered input-sm w-full"
              />
            </div>

            <!-- To Date -->
            <div>
              <label class="label py-1">
                <span class="label-text text-xs">To</span>
              </label>
              <input
                v-model="publicationDateTo"
                @change="handleDateChange"
                type="date"
                class="input input-bordered input-sm w-full"
              />
            </div>
          </div>

          <!-- Clear dates button -->
          <button
            v-if="publicationDateFrom || publicationDateTo"
            @click="clearDates"
            class="btn btn-ghost btn-xs mt-2 gap-1"
          >
            <XMarkIcon class="h-4 w-4" />
            Clear dates
          </button>
        </div>
      </div>
    </div>

    <!-- Clear All Button -->
    <div v-if="activeFiltersCount > 0" class="flex justify-end">
      <button 
        @click="clearAllFilters"
        class="btn btn-outline btn-sm gap-2"
      >
        <XMarkIcon class="h-4 w-4" />
        Clear All Literature Filters
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, inject } from 'vue'
import { useFilterStore } from '~/stores/filterStore'
import { useFetchChemicalStore } from '~/stores/fetchChemicalStore'
import { useChemicalPropertiesListStore } from '~/stores/chemicalPropertiesList'
import { 
  DocumentTextIcon, 
  CalendarIcon,
  XMarkIcon 
} from '@heroicons/vue/24/outline'

const filterStore = useFilterStore()
const fetchChemicalStore = useFetchChemicalStore()
const chemicalPropertiesListStore = useChemicalPropertiesListStore()

// ✅ Inject reload trigger from parent
const reloadHistogramTrigger = inject<Ref<number>>('reloadHistogramTrigger', ref(1))

// Debounce timer
let debounceTimer: ReturnType<typeof setTimeout> | null = null

// DOI
const doi = computed({
  get: () => filterStore.filters.exact.doi || '',
  set: (val) => filterStore.setExactFilter('doi', val)
})

// Title
const title = computed({
  get: () => filterStore.filters.exact.title || '',
  set: (val) => filterStore.setExactFilter('title', val)
})

// Publication dates
const publicationDateFrom = computed({
  get: () => filterStore.filters.range.publication_date?.after || '',
  set: (val) => {
    if (!filterStore.filters.range.publication_date) {
      filterStore.filters.range.publication_date = { after: null, before: null }
    }
    filterStore.filters.range.publication_date.after = val || null
  }
})

const publicationDateTo = computed({
  get: () => filterStore.filters.range.publication_date?.before || '',
  set: (val) => {
    if (!filterStore.filters.range.publication_date) {
      filterStore.filters.range.publication_date = { after: null, before: null }
    }
    filterStore.filters.range.publication_date.before = val || null
  }
})

// Active filters
const activeFiltersList = computed(() => {
  const filters = []
  
  if (doi.value) {
    filters.push({ key: 'doi', label: 'DOI', value: doi.value })
  }
  
  if (title.value) {
    filters.push({ key: 'title', label: 'Title', value: title.value })
  }
  
  if (publicationDateFrom.value || publicationDateTo.value) {
    const dateRange = `${publicationDateFrom.value || '...'} to ${publicationDateTo.value || '...'}`
    filters.push({ key: 'dates', label: 'Date Range', value: dateRange })
  }
  
  return filters
})

const activeFiltersCount = computed(() => activeFiltersList.value.length)

// Debounced update with histogram reload
const debouncedUpdate = () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  debounceTimer = setTimeout(async () => {
    try {
      await fetchChemicalStore.fetchChemicals()
      await chemicalPropertiesListStore.fetchAllChemicalProperties()
      
      // ✅ Trigger histogram reload in other components
      reloadHistogramTrigger.value *= -1
    } catch (error) {
      console.error('Error applying literature filter:', error)
    }
  }, 800)
}

// Handle date changes with histogram reload
const handleDateChange = async () => {
  try {
    await fetchChemicalStore.fetchChemicals()
    await chemicalPropertiesListStore.fetchAllChemicalProperties()
    
    // ✅ Trigger histogram reload
    reloadHistogramTrigger.value *= -1
  } catch (error) {
    console.error('Error applying date filter:', error)
  }
}

// Clear specific filter
const clearFilter = async (key: string) => {
  if (key === 'doi') {
    doi.value = ''
  } else if (key === 'title') {
    title.value = ''
  } else if (key === 'dates') {
    clearDates()
    return
  }
  
  await fetchChemicalStore.fetchChemicals()
  await chemicalPropertiesListStore.fetchAllChemicalProperties()
  
  // ✅ Trigger histogram reload
  reloadHistogramTrigger.value *= -1
}

// Clear dates
const clearDates = async () => {
  publicationDateFrom.value = ''
  publicationDateTo.value = ''
  
  await fetchChemicalStore.fetchChemicals()
  await chemicalPropertiesListStore.fetchAllChemicalProperties()
  
  // ✅ Trigger histogram reload
  reloadHistogramTrigger.value *= -1
}

// Clear all filters
const clearAllFilters = async () => {
  doi.value = ''
  title.value = ''
  publicationDateFrom.value = ''
  publicationDateTo.value = ''
  
  await fetchChemicalStore.fetchChemicals()
  await chemicalPropertiesListStore.fetchAllChemicalProperties()
  
  // ✅ Trigger histogram reload
  reloadHistogramTrigger.value *= -1 
}

// Export count for parent component
defineExpose({
  activeFiltersCount
})
</script>
