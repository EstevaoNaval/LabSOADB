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
        <p>Min</p>
        <select @change="handleOptionSelect" v-model="selectedMinRange" class="select select-sm select-bordered font-semibold text-lg">
          <option v-for="[index, value] of minRangeArr.entries()" :key="index" :value="value">{{ value }}</option>
        </select>
      </div>
      <div class="flex flex-col ml-auto">
        <p>Max</p>
        <select @change="handleOptionSelect" v-model="selectedMaxRange" class="select select-sm select-bordered font-semibold text-lg">
          <option v-for="[index, value] of maxRangeArr.entries()" :key="index" :value="value">{{ value }}</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup lang="js">
  import { computed, reactive, watch } from "vue";
  import { useThemeStore } from "~/stores/theme";
  import { useFilterStore } from '~/stores/filterStore'
  import { useFetchChemicalStore } from '~/stores/fetchChemicalStore'
  import { useHistogramRangeSliderStore } from "~/stores/histogramRangeSliderStore";
  import HistogramSlider from "vue3-histogram-slider-v2";
  import "vue3-histogram-slider-v2/dist/histogram-slider.css";

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

  const props = defineProps({
    step: {
      type: Number,
      required: true
    },
    chemPropArr: {
      type: Array,
      required: true
    },
    rangeFilter: {
      type: Object
    },
    propName: {
      type: String
    }
  })

  const triggerHistogramRangeSliderReload = () => {
    emit('reloadHistogramRangeSlider')
  }

  const createArrFromMinToMaxByStep = (min, max, step) => {
    let result = []

    for (let i = min; i <= max; i += step) {
      result.push(i)
    }

    if(result[result.length - 1] != max) {
      result.push(max)
    }

    return result
  }

  const handleOptionSelect = () => {
    selectedRange.from = selectedMinRange.value
    selectedRange.to = selectedMaxRange.value
  }

  const handleRangeSliderSelectChange = (event) => {
    selectedMinRange.value = event.from
    selectedMaxRange.value = event.to
  }

  const handleRangeSliderSelectFinish = (event) => {
    selectedRange.from = event.from
    selectedRange.to = event.to
  }

  histogramRangeSliderStore.setInitialProperty(props.propName, props.chemPropArr)

  var minRangeArr = ref(
    createArrFromMinToMaxByStep(
      histogramRangeSliderStore.properties[props.propName].min, 
      histogramRangeSliderStore.properties[props.propName].maxSelected, 
      props.step
    )
  )
  var maxRangeArr = ref(
    createArrFromMinToMaxByStep(
      histogramRangeSliderStore.properties[props.propName].minSelected, 
      histogramRangeSliderStore.properties[props.propName].max, 
      props.step
    ).reverse()
  )

  var selectedRange = reactive({
    from: histogramRangeSliderStore.properties[props.propName].minSelected,
    to: histogramRangeSliderStore.properties[props.propName].maxSelected
  }) 

  const selectedMinRange = ref(histogramRangeSliderStore.properties[props.propName].minSelected)
  const selectedMaxRange = ref(histogramRangeSliderStore.properties[props.propName].maxSelected)

  watch(() => selectedRange.from, () => {
    histogramRangeSliderStore.properties[props.propName].minSelected = selectedMinRange.value
    histogramRangeSliderStore.recentFilteredHistogram = props.propName
    histogramRangeSliderStore.setFilterActivated(props.propName, true)
    filterStore.setRangeFilter(props.rangeFilter.gte.name, 'gte', selectedMinRange.value)
    fetchChemicalStore.fetchChemicals()
    triggerHistogramRangeSliderReload()
  })

  watch(() => selectedRange.to, () => {
    histogramRangeSliderStore.properties[props.propName].maxSelected = selectedMaxRange.value
    histogramRangeSliderStore.recentFilteredHistogram = props.propName
    histogramRangeSliderStore.setFilterActivated(props.propName, true)
    filterStore.setRangeFilter(props.rangeFilter.lte.name, 'lte', selectedMaxRange.value)
    fetchChemicalStore.fetchChemicals()
    triggerHistogramRangeSliderReload()
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
  .irs-bar,.irs-line {
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