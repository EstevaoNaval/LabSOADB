<!-- components/HistogramRangeSlider.vue -->
<template>
  <div class="flex flex-col gap-6">
    <HistogramSlider 
      class="range-slider" 
      :style="rangeSliderStyle" 
      :width="300" 
      :barWidth="8"
      :data="histogramRangeSliderStore.properties[props.propName].arr" 
      :drag-interval="false" 
      :force-edges="false"
      :grid="false" 
      :hideFromTo="true" 
      :primaryColor="primaryColor" 
      :holderColor="holderColor"
      :handleSize="mediumHandleSize" 
      :barRadius="mediumRoundRadius"
      :min="histogramRangeSliderStore.properties[props.propName].min"
      :max="histogramRangeSliderStore.properties[props.propName].max" 
      :from="selectedRange.from" 
      :to="selectedRange.to"
      :step="props.step" 
      :clip="false" 
      :histSliderGap="6" 
      :lineHeight="24" 
      @finish="handleRangeSliderSelectFinish"
      @change="handleRangeSliderSelectChange" 
    />
    
    <div class="flex">
      <div class="flex flex-col mr-auto">
        <p class="text-sm text-base-content/70 mb-1">Min</p>
        <select 
          v-model="selectedMinRange" 
          @change="handleOptionSelect" 
          class="select select-sm select-bordered font-semibold text-lg"
        >
          <option v-for="[index, value] of minRangeArr.entries()" :key="index" :value="value">
            {{ value }}
          </option>
        </select>
      </div>
      
      <div class="flex flex-col ml-auto">
        <p class="text-sm text-base-content/70 mb-1">Max</p>
        <select 
          v-model="selectedMaxRange" 
          @change="handleOptionSelect" 
          class="select select-sm select-bordered font-semibold text-lg"
        >
          <option v-for="[index, value] of maxRangeArr.entries()" :key="index" :value="value">
            {{ value }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch, onBeforeUnmount } from "vue"
import { useThemeStore } from "~/stores/theme"
import { useFilterStore } from '~/stores/filterStore'
import { useFetchChemicalStore } from '~/stores/fetchChemicalStore'
import { useHistogramRangeSliderStore } from "~/stores/histogramRangeSliderStore"
import HistogramSlider from "vue3-histogram-slider-v2"
import "vue3-histogram-slider-v2/dist/histogram-slider.css"

const themeStore = useThemeStore()
const filterStore = useFilterStore()
const fetchChemicalStore = useFetchChemicalStore()
const histogramRangeSliderStore = useHistogramRangeSliderStore()

const mediumHandleSize = 24
const mediumRoundRadius = 2
const primaryColor = themeStore.isDarkMode ? "#38bdf8" : '#0069ff'
const holderColor = themeStore.isDarkMode ? "#21293b" : '#ebedf0'
const rangeSliderStyle = computed(() => ({
  '--range-slider-handle-border': themeStore.isDarkMode ? '3px solid #38bdf8' : '3px solid #0069ff',
  '--range-slider-handle-background-color': themeStore.isDarkMode ? '#0f172a' : '#ffffff'
}))

const emit = defineEmits(['reloadHistogramRangeSlider'])

interface Props {
  step: number
  chemPropArr: number[]
  rangeFilter: {
    gte: { name: string }
    lte: { name: string }
  }
  propName: string
}

const props = defineProps<Props>()

// Debounce timer
let debounceTimer: ReturnType<typeof setTimeout> | null = null

const triggerHistogramRangeSliderReload = () => {
  emit('reloadHistogramRangeSlider')
}

const createArrFromMinToMaxByStep = (min: number, max: number, step: number) => {
  const result: number[] = []
  
  for (let i = min; i <= max; i += step) {
    result.push(i)
  }
  
  if (result[result.length - 1] !== max) {
    result.push(max)
  }
  
  return result
}

const handleOptionSelect = () => {
  selectedRange.from = selectedMinRange.value
  selectedRange.to = selectedMaxRange.value
}

const handleRangeSliderSelectChange = (event: { from: number; to: number }) => {
  selectedMinRange.value = event.from
  selectedMaxRange.value = event.to
}

const handleRangeSliderSelectFinish = (event: { from: number; to: number }) => {
  selectedRange.from = event.from
  selectedRange.to = event.to
}

// Initialize histogram data
histogramRangeSliderStore.setInitialProperty(props.propName, props.chemPropArr)

const minRangeArr = ref(
  createArrFromMinToMaxByStep(
    histogramRangeSliderStore.properties[props.propName].min,
    histogramRangeSliderStore.properties[props.propName].maxSelected,
    props.step
  )
)

const maxRangeArr = ref(
  createArrFromMinToMaxByStep(
    histogramRangeSliderStore.properties[props.propName].minSelected,
    histogramRangeSliderStore.properties[props.propName].max,
    props.step
  ).reverse()
)

const selectedRange = reactive({
  from: histogramRangeSliderStore.properties[props.propName].minSelected,
  to: histogramRangeSliderStore.properties[props.propName].maxSelected
})

const selectedMinRange = ref(histogramRangeSliderStore.properties[props.propName].minSelected)
const selectedMaxRange = ref(histogramRangeSliderStore.properties[props.propName].maxSelected)

// Flag to prevent circular updates
let isUpdating = false

// Debounced update function
const debouncedUpdate = (filterType: 'gte' | 'lte', value: number, filterName: string) => {
  // Clear existing timer
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  // Set new timer
  debounceTimer = setTimeout(async () => {
    if (isUpdating) return
    
    try {
      isUpdating = true
      
      // Update filter store
      filterStore.setRangeFilter(filterName, filterType, value)
      
      // Mark as activated
      histogramRangeSliderStore.setFilterActivated(props.propName, true)
      histogramRangeSliderStore.recentFilteredHistogram = props.propName
      
      // Fetch new data
      await fetchChemicalStore.fetchChemicals()
      
      // Reload histogram
      triggerHistogramRangeSliderReload()
    } finally {
      isUpdating = false
    }
  }, 500) // 500ms debounce
}

// Watch for min range changes
watch(() => selectedRange.from, (newValue) => {
  if (isUpdating) return
  
  histogramRangeSliderStore.properties[props.propName].minSelected = newValue
  debouncedUpdate('gte', newValue, props.rangeFilter.gte.name)
})

// Watch for max range changes
watch(() => selectedRange.to, (newValue) => {
  if (isUpdating) return
  
  histogramRangeSliderStore.properties[props.propName].maxSelected = newValue
  debouncedUpdate('lte', newValue, props.rangeFilter.lte.name)
})

// Cleanup on unmount
onBeforeUnmount(() => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
})
</script>

<style>
.irs-handle {
  -webkit-appearance: none;
  appearance: none;
  border: var(--range-slider-handle-border);
  transform: translateY(1.1rem);
  background-color: var(--range-slider-handle-background-color) !important;
}

.irs-bar,
.irs-line {
  -webkit-appearance: none;
  appearance: none;
}

.irs-line {
  -webkit-appearance: none;
  appearance: none;
  height: .5rem !important;
  transform: translateY(.5rem);
}
</style>
