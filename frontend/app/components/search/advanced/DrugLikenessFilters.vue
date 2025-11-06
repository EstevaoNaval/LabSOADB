<!-- components/advanced-search/DrugLikenessFilters.vue -->
<template>
  <main :key="histogramRangeSliderDiv">
    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-16 space-y-4" role="status">
      <span class="loading loading-spinner loading-lg text-primary"></span>
      <p class="text-base-content/60 text-sm">Loading drug-likeness filters...</p>
    </div>

    <!-- Content -->
    <div v-else class="space-y-6">
      <!-- Active Filters Badges -->
      <div v-if="activeFilters.length > 0" class="flex flex-wrap gap-2" role="list" aria-label="Active filters">
        <div 
          v-for="filter in activeFilters" 
          :key="filter.propName"
          class="badge badge-primary gap-2 px-3 py-2"
          role="listitem"
        >
          <span class="text-xs font-medium">{{ filter.label }}: {{ filter.range }}</span>
          <button 
            type="button" 
            @click="clearFilter(filter.propName, filter.rangeFilter)"
            class="btn btn-ghost btn-xs btn-circle hover:bg-primary-content"
            :aria-label="`Remove ${filter.label} filter`"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="size-3" viewBox="0 0 16 16">
              <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Histograms Grid - Responsivo -->
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <div 
          v-for="data in histogramDataArr" 
          :key="data.id"
          class="card bg-base-200 shadow-sm hover:shadow-md transition-shadow duration-200"
        >
          <template v-if="data.data.length > 1">
            <div class="card-body p-4">
              <!-- Header -->
              <div class="flex items-center justify-between mb-3">
                <h4 class="text-sm font-semibold text-primary line-clamp-1" :title="data.label">
                  {{ data.label }}
                </h4>
                <button 
                  v-if="histogramRangeSliderStore.properties[data.propName]?.filterActivated"
                  type="button"
                  class="btn btn-ghost btn-xs btn-circle hover:btn-error"
                  @click="clearFilter(data.propName, data.rangeFilter)"
                  :aria-label="`Clear ${data.label} filter`"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="size-4" viewBox="0 0 16 16">
                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z" />
                  </svg>
                </button>
              </div>

              <!-- Histogram Component -->
              <HistogramRangeSlider 
                class="w-full" 
                :chemPropArr="data.data" 
                :step="data.step"
                :rangeFilter="data.rangeFilter" 
                :propName="data.propName"
                @reloadHistogramRangeSlider="reloadHistogramRangeSliderDiv" 
              />

              <!-- Active Range Display -->
              <div 
                v-if="histogramRangeSliderStore.properties[data.propName]?.filterActivated"
                class="mt-3 pt-3 border-t border-base-300"
              >
                <p class="text-xs text-base-content/60 text-center">
                  Active: <span class="font-semibold text-primary">{{ formatFilterRange(data.propName) }}</span>
                </p>
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- Info Alert -->
      <div class="alert alert-info shadow-lg">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <div>
          <h4 class="font-bold">Drug-likeness Rules</h4>
          <div class="text-sm mt-2 space-y-1">
            <p>• <strong>Lipinski's Rule of Five:</strong> Predicts oral bioavailability (MW ≤ 500, LogP ≤ 5, H-donors ≤ 5, H-acceptors ≤ 10)</p>
            <p>• <strong>PAINS:</strong> Pan-Assay Interference Compounds - compounds that show activity in multiple assays</p>
            <p>• <strong>JPLogP:</strong> Lipophilicity measure, ideal range: -0.4 to 5.6 for drug-like compounds</p>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="histogramDataArr.length === 0" class="alert alert-warning shadow-lg">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div>
          <h4 class="font-bold">No drug-likeness data available</h4>
          <p class="text-sm">Enter a query in the search field above to load drug-likeness filters.</p>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, inject, watch } from "vue"
import HistogramRangeSlider from "~/components/HistogramRangeSlider.vue"
import { useChemicalPropertiesListStore } from "~/stores/chemicalPropertiesList"
import { useFetchChemicalStore } from "~/stores/fetchChemicalStore"
import { useFilterStore } from "~/stores/filterStore"
import { useHistogramRangeSliderStore } from "~/stores/histogramRangeSliderStore"

const chemicalPropertiesListStore = useChemicalPropertiesListStore()
const fetchChemicalStore = useFetchChemicalStore()
const filterStore = useFilterStore()
const histogramRangeSliderStore = useHistogramRangeSliderStore()

const histogramRangeSliderDiv = ref(1)
const loading = ref(false)
const reloadHistogramTrigger = inject<Ref<number>>('reloadHistogramTrigger', ref(0))

interface HistogramData {
  id: number
  label: string
  data: number[]
  step: number
  rangeFilter: {
    gte: { name: string }
    lte: { name: string }
  }
  propName: string
}

const histogramDataArr = ref<HistogramData[]>([])

// Computed: Active filters
const activeFilters = computed(() => {
  return histogramDataArr.value
    .filter(data => histogramRangeSliderStore.properties[data.propName]?.filterActivated)
    .map(data => ({
      propName: data.propName,
      label: data.label,
      rangeFilter: data.rangeFilter,
      range: formatFilterRange(data.propName)
    }))
})

// Format filter range for display
const formatFilterRange = (propName: string) => {
  const props = histogramRangeSliderStore.properties[propName]
  if (!props || !props.filterActivated) return ''
  
  const min = props.minSelected ?? props.min
  const max = props.maxSelected ?? props.max
  
  // Format numbers with appropriate precision
  const formatNum = (num: number) => {
    if (propName === 'jplogp') {
      return num.toFixed(1) // JPLogP com 1 decimal
    }
    return Math.round(num)
  }
  
  return `${formatNum(min)} - ${formatNum(max)}`
}

// Reload histogram data
async function reloadHistogramRangeSliderDiv() {
  await loadChemPropsList()
  histogramRangeSliderDiv.value *= -1
}

// Load drug-likeness properties for histograms
const loadChemPropsList = async () => {
  loading.value = true

  try {
    await chemicalPropertiesListStore.fetchAllChemicalProperties()

    histogramDataArr.value = [
      {
        id: 1,
        label: "Lipinski Violations",
        data: chemicalPropertiesListStore.properties.count_lipinski_violation,
        step: 1,
        rangeFilter: {
          gte: { name: 'count_lipinski_violation' },
          lte: { name: 'count_lipinski_violation' }
        },
        propName: 'lipinski_violation'
      },
      {
        id: 2,
        label: 'PAINS Alerts',
        data: chemicalPropertiesListStore.properties.count_pains_alert,
        step: 1,
        rangeFilter: {
          gte: { name: 'count_pains_alert' },
          lte: { name: 'count_pains_alert' }
        },
        propName: 'pains_alert'
      },
      {
        id: 3,
        label: 'JPLogP',
        data: chemicalPropertiesListStore.properties.jplogp,
        step: 0.5,
        rangeFilter: {
          gte: { name: 'jplogp' },
          lte: { name: 'jplogp' }
        },
        propName: 'jplogp'
      }
    ].filter(item => item.data.length > 1) // Only show histograms with data
  } catch (error) {
    console.error('Error loading drug-likeness properties:', error)
  } finally {
    loading.value = false
  }
}

// Clear specific filter
const clearFilter = async (propName: string, rangeFilter: any) => {
  histogramRangeSliderStore.resetProperty(propName)
  filterStore.clearRangeFilter(rangeFilter.gte.name, 'gte')
  filterStore.clearRangeFilter(rangeFilter.lte.name, 'lte')
  
  await fetchChemicalStore.fetchChemicals()
  await reloadHistogramRangeSliderDiv()
}

// Watch for reload trigger from parent
watch(reloadHistogramTrigger, async () => {
  await reloadHistogramRangeSliderDiv()
})

// Lifecycle hooks
onMounted(async () => {
  await loadChemPropsList()
})
</script>
