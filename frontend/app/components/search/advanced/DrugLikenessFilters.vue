<!-- components/advanced-search/DrugLikenessFilters.vue -->
<template>
  <main :key="histogramRangeSliderDiv">
    <div v-if="loading" class="flex flex-col items-center justify-center py-16 space-y-4">
      <span class="loading loading-spinner loading-lg text-primary"></span>
      <p class="text-base-content/60 text-sm">Loading drug-likeness filters...</p>
    </div>

    <div v-else class="space-y-6">
      <div 
        v-for="data in histogramDataArr" 
        :key="data.id"
        class="card bg-base-200 shadow-sm hover:shadow-md transition-shadow duration-200"
      >
        <template v-if="data.data.length > 1">
          <div class="card-body p-5">
            <div class="flex items-center justify-between mb-3">
              <h3 class="card-title text-base font-semibold text-primary">
                {{ data.label }}
              </h3>
              <button 
                v-if="histogramRangeSliderStore.properties[data.propName]?.filterActivated"
                type="button"
                class="btn btn-ghost btn-sm btn-circle hover:btn-error"
                @click="clearFilter(data.propName, data.rangeFilter)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="size-5" viewBox="0 0 16 16">
                  <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z" />
                </svg>
              </button>
            </div>

            <HistogramRangeSlider 
              class="w-full" 
              :chemPropArr="data.data" 
              :step="data.step"
              :rangeFilter="data.rangeFilter" 
              :propName="data.propName"
              @reloadHistogramRangeSlider="reloadHistogramRangeSliderDiv" 
            />

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

      <!-- Info Box -->
      <div class="alert alert-info text-sm">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <div>
          <p><strong>Drug-likeness rules:</strong></p>
          <ul class="text-xs list-disc list-inside mt-1 space-y-1">
            <li><strong>Lipinski's Rule of Five:</strong> Predicts oral bioavailability</li>
            <li><strong>PAINS:</strong> Pan-Assay Interference Compounds</li>
            <li><strong>LogP:</strong> Lipophilicity (ideal: -0.4 to 5.6)</li>
          </ul>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
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

const formatFilterRange = (propName: string) => {
  const props = histogramRangeSliderStore.properties[propName]
  if (!props || !props.filterActivated) return ''
  
  return `${props.minSelected ?? props.min} - ${props.maxSelected ?? props.max}`
}

async function reloadHistogramRangeSliderDiv() {
  await loadChemPropsList()
  histogramRangeSliderDiv.value *= -1
}

const loadChemPropsList = async () => {
  loading.value = true

  try {
    await chemicalPropertiesListStore.fetchAllChemicalProperties()

    histogramDataArr.value = [
      {
        id: 1,
        label: "Lipinski's Rule of Five Violations",
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
        label: 'PAINS Alert Count',
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
        step: 1,
        rangeFilter: {
          gte: { name: 'jplogp' },
          lte: { name: 'jplogp' }
        },
        propName: 'jplogp'
      }
    ].filter(item => item.data.length > 1)
  } catch (error) {
    console.error('Error loading drug-likeness properties:', error)
  } finally {
    loading.value = false
  }
}

const clearFilter = async (propName: string, rangeFilter: any) => {
  histogramRangeSliderStore.resetProperty(propName)
  filterStore.clearRangeFilter(rangeFilter.gte.name, 'gte')
  filterStore.clearRangeFilter(rangeFilter.lte.name, 'lte')
  
  await fetchChemicalStore.fetchChemicals()
  await reloadHistogramRangeSliderDiv()
}

onMounted(() => {
  loadChemPropsList()
})
</script>
