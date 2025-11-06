<!-- components/HistogramRangeSlider.vue -->
<template>
  <div class="flex flex-col gap-3">
    <!-- Histogram Container com espaçamento extra -->
    <div ref="containerRef" class="w-full pb-8">
      <HistogramSlider 
        v-if="containerWidth > 0"
        class="range-slider" 
        :style="rangeSliderStyle" 
        :width="containerWidth" 
        :barWidth="8"
        :data="histogramRangeSliderStore.properties[props.propName].arr" 
        :drag-interval="false" 
        :force-edges="false"
        :grid="false" 
        :hideFromTo="true" 
        :primaryColor="primaryColor" 
        :holderColor="holderColor"
        :handleSize="handleSize" 
        :barRadius="barRadius"
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
    </div>
    
    <!-- Min/Max Selectors -->
    <div class="flex flex-col sm:flex-row gap-3 sm:gap-0">
      <div class="flex flex-col sm:mr-auto w-full sm:w-auto">
        <label class="label py-1">
          <span class="label-text text-xs font-medium text-base-content/70">Min</span>
        </label>
        <select 
          v-model="selectedMinRange" 
          @change="handleOptionSelect" 
          class="select select-sm select-bordered font-semibold text-base w-full"
        >
          <option v-for="[index, value] of minRangeArr.entries()" :key="index" :value="value">
            {{ formatValue(value) }}
          </option>
        </select>
      </div>
      
      <div class="flex flex-col sm:ml-auto w-full sm:w-auto">
        <label class="label py-1">
          <span class="label-text text-xs font-medium text-base-content/70">Max</span>
        </label>
        <select 
          v-model="selectedMaxRange" 
          @change="handleOptionSelect" 
          class="select select-sm select-bordered font-semibold text-base w-full"
        >
          <option v-for="[index, value] of maxRangeArr.entries()" :key="index" :value="value">
            {{ formatValue(value) }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch, onBeforeUnmount, onMounted, nextTick } from "vue"
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

// ✅ Container reference for responsive width measurement
const containerRef = ref<HTMLElement | null>(null)
const containerWidth = ref(300)

// ✅ Histogram styling constants
const handleSize = 24
const barRadius = 2
const primaryColor = computed(() => themeStore.isDarkMode ? "#38bdf8" : '#0069ff')
const holderColor = computed(() => themeStore.isDarkMode ? "#21293b" : '#ebedf0')

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

let resizeObserver: ResizeObserver | null = null

const updateContainerWidth = () => {
  if (containerRef.value) {
    const rect = containerRef.value.getBoundingClientRect()
    containerWidth.value = Math.floor(rect.width - 20)
  }
}

onMounted(async () => {
  await nextTick()
  updateContainerWidth()
  
  if (containerRef.value && typeof ResizeObserver !== 'undefined') {
    resizeObserver = new ResizeObserver(() => {
      updateContainerWidth()
    })
    resizeObserver.observe(containerRef.value)
  }
  
  window.addEventListener('resize', updateContainerWidth)
})

onBeforeUnmount(() => {
  if (resizeObserver && containerRef.value) {
    resizeObserver.unobserve(containerRef.value)
    resizeObserver.disconnect()
  }
  window.removeEventListener('resize', updateContainerWidth)
  
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
})

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

const formatValue = (value: number) => {
  if (props.step < 1) {
    return value.toFixed(1)
  }
  
  if (Math.abs(value) >= 1000) {
    return value.toLocaleString()
  }
  
  return value
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

let isUpdating = false

const debouncedUpdate = (filterType: 'gte' | 'lte', value: number, filterName: string) => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  debounceTimer = setTimeout(async () => {
    if (isUpdating) return
    
    try {
      isUpdating = true
      
      filterStore.setRangeFilter(filterName, filterType, value)
      histogramRangeSliderStore.setFilterActivated(props.propName, true)
      histogramRangeSliderStore.recentFilteredHistogram = props.propName
      
      await fetchChemicalStore.fetchChemicals()
      
      triggerHistogramRangeSliderReload()
    } finally {
      isUpdating = false
    }
  }, 500)
}

watch(() => selectedRange.from, (newValue) => {
  if (isUpdating) return
  
  histogramRangeSliderStore.properties[props.propName].minSelected = newValue
  debouncedUpdate('gte', newValue, props.rangeFilter.gte.name)
})

watch(() => selectedRange.to, (newValue) => {
  if (isUpdating) return
  
  histogramRangeSliderStore.properties[props.propName].maxSelected = newValue
  debouncedUpdate('lte', newValue, props.rangeFilter.lte.name)
})
</script>

<style >
/* ✅ Handles (círculos do slider) */
.irs-handle {
  -webkit-appearance: none;
  appearance: none;
  border: var(--range-slider-handle-border);
  transform: translateY(1.1rem);
  background-color: var(--range-slider-handle-background-color) !important;
  z-index: 10;
  cursor: pointer;
}

/* ✅ Linha e barra do slider */
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

/* ✅ Container do slider - SEM overflow hidden */
.range-slider {
  width: 100%;
  max-width: 100%;
  overflow: visible !important; /* ← CRÍTICO: permite handles serem visíveis */
  position: relative;
}

/* ✅ Wrapper interno - garante espaço para handles */
:deep(.histogram-slider) {
  overflow: visible !important;
  padding-bottom: 2rem;
}

/* ✅ Container do histograma */
:deep(.irs) {
  position: relative;
  overflow: visible !important;
}

/* ✅ Área do histograma */
:deep(.irs-line) {
  overflow: visible !important;
}

/* ✅ Labels */
.label {
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
}

.label-text {
  font-size: 0.75rem;
  line-height: 1rem;
}

/* ✅ Select dropdowns */
.select-sm {
  min-height: 2rem;
  height: 2rem;
  font-size: 0.875rem;
  line-height: 1.25rem;
}

/* ✅ Responsive select width on mobile */
@media (max-width: 640px) {
  .select {
    width: 100%;
  }
}
</style>
