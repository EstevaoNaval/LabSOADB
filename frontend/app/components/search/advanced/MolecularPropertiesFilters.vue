<!-- components/advanced-search/MolecularPropertiesFilters.vue -->
<template>
  <main :key="histogramRangeSliderDiv">
    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-16 space-y-4" role="status">
      <span class="loading loading-spinner loading-lg text-primary"></span>
      <p class="text-base-content/60 text-sm">Loading filter options...</p>
    </div>

    <!-- Filters Grid -->
    <div v-else class="space-y-6">
      <!-- Active Filters Summary -->
      <div v-if="activeFilters.length > 0" class="flex flex-wrap gap-2 mb-4">
        <div 
          v-for="filter in activeFilters" 
          :key="filter.propName"
          class="badge badge-primary badge-lg gap-2 px-3 py-3"
        >
          <span class="text-sm font-medium">{{ filter.label }}: {{ filter.range }}</span>
          <button 
            type="button" 
            @click="clearFilter(filter.propName, filter.rangeFilter)"
            class="btn btn-ghost btn-xs btn-circle hover:bg-primary-content"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="size-4" viewBox="0 0 16 16">
              <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Histogram Cards -->
      <div 
        v-for="data in histogramDataArr" 
        :key="data.id"
        class="card bg-base-200 shadow-sm hover:shadow-md transition-shadow duration-200"
      >
        <template v-if="data.data.length > 1">
          <div class="card-body p-5">
            <!-- Filter Header -->
            <div class="flex items-center justify-between mb-3">
              <h3 class="card-title text-base font-semibold text-primary">
                {{ data.label }}
              </h3>
              <button 
                v-if="histogramRangeSliderStore.properties[data.propName]?.filterActivated"
                type="button"
                class="btn btn-ghost btn-sm btn-circle hover:btn-error tooltip tooltip-left"
                data-tip="Clear this filter" 
                @click="clearFilter(data.propName, data.rangeFilter)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="size-5" viewBox="0 0 16 16">
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

            <!-- Current Range Display -->
            <div 
              v-if="histogramRangeSliderStore.properties[data.propName]?.filterActivated"
              class="mt-3 pt-3 border-t border-base-300"
            >
              <p class="text-xs text-base-content/60 text-center">
                Active range:
                <span class="font-semibold text-primary">
                  {{ formatFilterRange(data.propName) }}
                </span>
              </p>
            </div>
          </div>
        </template>
      </div>

      <!-- Empty State -->
      <div v-if="histogramDataArr.length === 0" class="alert alert-warning">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div>
          <h4 class="font-bold">No histogram data available</h4>
          <p class="text-sm">Perform a search to enable histogram filters.</p>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from "vue"
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
  
  return `${props.minSelected ?? props.min} - ${props.maxSelected ?? props.max}`
}

// Reload histogram data
async function reloadHistogramRangeSliderDiv() {
  await loadChemPropsList()
  histogramRangeSliderDiv.value *= -1
}

// Load chemical properties for histograms
const loadChemPropsList = async () => {
  loading.value = true

  try {
    await chemicalPropertiesListStore.fetchAllChemicalProperties()

    histogramDataArr.value = [
      {
        id: 1,
        label: 'Molecular Weight, g/mol',
        data: chemicalPropertiesListStore.properties.molecular_weight,
        step: 25,
        rangeFilter: {
          gte: { name: 'molecular_weight' },
          lte: { name: 'molecular_weight' }
        },
        propName: 'molecular_weight'
      },
      {
        id: 2,
        label: 'Polar Surface Area (TPSA), Ų',
        data: chemicalPropertiesListStore.properties.tpsa,
        step: 10,
        rangeFilter: {
          gte: { name: 'tpsa' },
          lte: { name: 'tpsa' }
        },
        propName: 'tpsa'
      },
      {
        id: 3,
        label: 'Heavy Atom Count',
        data: chemicalPropertiesListStore.properties.heavy_atom,
        step: 5,
        rangeFilter: {
          gte: { name: 'count_heavy_atom' },
          lte: { name: 'count_heavy_atom' }
        },
        propName: 'heavy_atom'
      },
      {
        id: 4,
        label: 'Rotatable Bond Count',
        data: chemicalPropertiesListStore.properties.rotatable_bond,
        step: 1,
        rangeFilter: {
          gte: { name: 'count_rotatable_bond' },
          lte: { name: 'count_rotatable_bond' }
        },
        propName: 'rotatable_bond'
      },
      {
        id: 5,
        label: 'H-Bond Donor Count',
        data: chemicalPropertiesListStore.properties.h_bond_donor,
        step: 1,
        rangeFilter: {
          gte: { name: 'count_h_bond_donor' },
          lte: { name: 'count_h_bond_donor' }
        },
        propName: 'h_bond_donor'
      },
      {
        id: 6,
        label: 'H-Bond Acceptor Count',
        data: chemicalPropertiesListStore.properties.h_bond_acceptor,
        step: 1,
        rangeFilter: {
          gte: { name: 'count_h_bond_acceptor' },
          lte: { name: 'count_h_bond_acceptor' }
        },
        propName: 'h_bond_acceptor'
      },
      {
        id: 7,
        label: 'Melting Point, °C',
        data: [
          ...chemicalPropertiesListStore.properties.mp_lower_bound,
          ...chemicalPropertiesListStore.properties.mp_upper_bound
        ],
        step: 10,
        rangeFilter: {
          gte: { name: 'mp_lower_bound' },
          lte: { name: 'mp_upper_bound' }
        },
        propName: 'melting_point'
      }
    ].filter(item => item.data.length > 1) // Only show histograms with data
  } catch (error) {
    console.error('Error loading chemical properties:', error)
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

// Lifecycle hooks
onMounted(() => {
  loadChemPropsList()
})

onBeforeUnmount(() => {
  // Don't reset on unmount - preserve filters
  // chemicalPropertiesListStore.$reset()
})
</script>
