<!-- components/advanced-search/PharmacokineticsFilters.vue -->
<template>
  <div class="space-y-6">
    <!-- Header Description -->
    <div class="alert alert-info">
      <InformationCircleIcon class="h-6 w-6 shrink-0" />
      <div>
        <h4 class="font-semibold text-sm">Pharmacokinetics Filters</h4>
        <p class="text-xs mt-1">Filter by ADME properties and cytochrome P450 inhibition</p>
      </div>
    </div>

    <!-- Active Filters Badges -->
    <div v-if="activeFiltersCount > 0" class="flex flex-wrap gap-2">
      <div 
        v-for="(filter, key) in activeFilters" 
        :key="key"
        class="badge badge-primary gap-2 px-3 py-2"
      >
        <span class="text-xs font-medium">{{ filter }}</span>
        <button 
          type="button" 
          @click="clearFilter(key)"
          class="btn btn-ghost btn-xs btn-circle hover:bg-primary-content"
        >
          <XMarkIcon class="h-3 w-3" />
        </button>
      </div>
    </div>

    <!-- ADME Properties -->
    <div class="card bg-base-200 shadow-sm">
      <div class="card-body p-4">
        <h4 class="font-semibold text-sm mb-3 flex items-center gap-2">
          <BeakerIcon class="h-5 w-5 text-primary" />
          ADME Properties
        </h4>

        <!-- Gastrointestinal Absorption -->
        <div class="form-control">
          <label class="label cursor-pointer justify-start gap-3">
            <input
              v-model="gastrointestinalAbsorption"
              @change="handleFilterChange"
              type="checkbox"
              class="checkbox checkbox-primary"
            />
            <div>
              <span class="label-text font-medium">Gastrointestinal Absorption</span>
              <p class="text-xs text-base-content/60">High GI absorption compounds</p>
            </div>
          </label>
        </div>

        <!-- Blood-Brain Barrier -->
        <div class="form-control">
          <label class="label cursor-pointer justify-start gap-3">
            <input
              v-model="bloodBrainBarrier"
              @change="handleFilterChange"
              type="checkbox"
              class="checkbox checkbox-primary"
            />
            <div>
              <span class="label-text font-medium">BBB Permeation</span>
              <p class="text-xs text-base-content/60">Crosses blood-brain barrier</p>
            </div>
          </label>
        </div>
      </div>
    </div>

    <!-- CYP450 Inhibition -->
    <div class="card bg-base-200 shadow-sm">
      <div class="card-body p-4">
        <h4 class="font-semibold text-sm mb-3 flex items-center gap-2">
          <CubeIcon class="h-5 w-5 text-secondary" />
          CYP450 Inhibition
        </h4>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <!-- CYP1A2 -->
          <div class="form-control">
            <label class="label cursor-pointer justify-start gap-3 py-2">
              <input
                v-model="cyp1a2"
                @change="handleFilterChange"
                type="checkbox"
                class="checkbox checkbox-sm checkbox-primary"
              />
              <span class="label-text text-sm">CYP1A2 Inhibitor</span>
            </label>
          </div>

          <!-- CYP2C9 -->
          <div class="form-control">
            <label class="label cursor-pointer justify-start gap-3 py-2">
              <input
                v-model="cyp2c9"
                @change="handleFilterChange"
                type="checkbox"
                class="checkbox checkbox-sm checkbox-primary"
              />
              <span class="label-text text-sm">CYP2C9 Inhibitor</span>
            </label>
          </div>

          <!-- CYP2C19 -->
          <div class="form-control">
            <label class="label cursor-pointer justify-start gap-3 py-2">
              <input
                v-model="cyp2c19"
                @change="handleFilterChange"
                type="checkbox"
                class="checkbox checkbox-sm checkbox-primary"
              />
              <span class="label-text text-sm">CYP2C19 Inhibitor</span>
            </label>
          </div>

          <!-- CYP2D6 -->
          <div class="form-control">
            <label class="label cursor-pointer justify-start gap-3 py-2">
              <input
                v-model="cyp2d6"
                @change="handleFilterChange"
                type="checkbox"
                class="checkbox checkbox-sm checkbox-primary"
              />
              <span class="label-text text-sm">CYP2D6 Inhibitor</span>
            </label>
          </div>

          <!-- CYP3A4 -->
          <div class="form-control">
            <label class="label cursor-pointer justify-start gap-3 py-2">
              <input
                v-model="cyp3a4"
                @change="handleFilterChange"
                type="checkbox"
                class="checkbox checkbox-sm checkbox-primary"
              />
              <span class="label-text text-sm">CYP3A4 Inhibitor</span>
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- Clear All Button -->
    <div v-if="activeFiltersCount > 0" class="flex justify-end gap-2">
      <button 
        @click="clearAllFilters"
        class="btn btn-outline btn-sm gap-2"
      >
        <XMarkIcon class="h-4 w-4" />
        Clear All
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, inject, ref } from 'vue'
import { useFilterStore } from '~/stores/filterStore'
import { useFetchChemicalStore } from '~/stores/fetchChemicalStore'
import { useChemicalPropertiesListStore } from '~/stores/chemicalPropertiesList'
import { 
  BeakerIcon, 
  CubeIcon, 
  InformationCircleIcon,
  XMarkIcon 
} from '@heroicons/vue/24/outline'

const filterStore = useFilterStore()
const fetchChemicalStore = useFetchChemicalStore()
const chemicalPropertiesListStore = useChemicalPropertiesListStore()

// ✅ Inject reload trigger from parent
const reloadHistogramTrigger = inject<Ref<number>>('reloadHistogramTrigger', ref(1))

// Debounce timer
let debounceTimer: ReturnType<typeof setTimeout> | null = null

// Filter properties
const gastrointestinalAbsorption = computed({
  get: () => filterStore.filters.exact.gastrointestinal_absorption === true,
  set: (val) => filterStore.setExactFilter('gastrointestinal_absorption', val ? true : '')
})

const bloodBrainBarrier = computed({
  get: () => filterStore.filters.exact.blood_brain_barrier_permeation === true,
  set: (val) => filterStore.setExactFilter('blood_brain_barrier_permeation', val ? true : '')
})

const cyp1a2 = computed({
  get: () => filterStore.filters.exact.cyp1a2_inhibitor === true,
  set: (val) => filterStore.setExactFilter('cyp1a2_inhibitor', val ? true : null)
})

const cyp2c9 = computed({
  get: () => filterStore.filters.exact.cyp2c9_inhibitor === true,
  set: (val) => filterStore.setExactFilter('cyp2c9_inhibitor', val ? true : null)
})

const cyp2c19 = computed({
  get: () => filterStore.filters.exact.cyp2c19_inhibitor === true,
  set: (val) => filterStore.setExactFilter('cyp2c19_inhibitor', val ? true : null)
})

const cyp2d6 = computed({
  get: () => filterStore.filters.exact.cyp2d6_inhibitor === true,
  set: (val) => filterStore.setExactFilter('cyp2d6_inhibitor', val ? true : null)
})

const cyp3a4 = computed({
  get: () => filterStore.filters.exact.cyp3a4_inhibitor === true,
  set: (val) => filterStore.setExactFilter('cyp3a4_inhibitor', val ? true : null)
})

// Active filters
const activeFilters = computed(() => {
  const filters: Record<string, string> = {}
  
  if (gastrointestinalAbsorption.value) filters['gastrointestinal_absorption'] = 'GI Absorption'
  if (bloodBrainBarrier.value) filters['blood_brain_barrier_permeation'] = 'BBB Permeation'
  if (cyp1a2.value) filters['cyp1a2_inhibitor'] = 'CYP1A2'
  if (cyp2c9.value) filters['cyp2c9_inhibitor'] = 'CYP2C9'
  if (cyp2c19.value) filters['cyp2c19_inhibitor'] = 'CYP2C19'
  if (cyp2d6.value) filters['cyp2d6_inhibitor'] = 'CYP2D6'
  if (cyp3a4.value) filters['cyp3a4_inhibitor'] = 'CYP3A4'
  
  return filters
})

const activeFiltersCount = computed(() => Object.keys(activeFilters.value).length)

// Handle filter changes with debounce and histogram reload
const handleFilterChange = () => {
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
      console.error('Error applying pharmacokinetics filter:', error)
    }
  }, 500)
}

// Clear specific filter
const clearFilter = async (key: string) => {
  filterStore.setExactFilter(key, '')
  
  await fetchChemicalStore.fetchChemicals()
  await chemicalPropertiesListStore.fetchAllChemicalProperties()
  
  // ✅ Trigger histogram reload
  reloadHistogramTrigger.value *= -1
}

// Clear all filters
const clearAllFilters = async () => {
  filterStore.setExactFilter('gastrointestinal_absorption', '')
  filterStore.setExactFilter('blood_brain_barrier_permeation', '')
  filterStore.setExactFilter('cyp1a2_inhibitor', '')
  filterStore.setExactFilter('cyp2c9_inhibitor', '')
  filterStore.setExactFilter('cyp2c19_inhibitor', '')
  filterStore.setExactFilter('cyp2d6_inhibitor', '')
  filterStore.setExactFilter('cyp3a4_inhibitor', '')
  
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
