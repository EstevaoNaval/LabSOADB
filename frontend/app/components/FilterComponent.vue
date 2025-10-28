<template>
    <main class="container mx-auto px-4 py-6 max-w-screen-2xl">
        <!-- Filter Header Section -->
        <section :key="histogramRangeSliderDiv" aria-label="Chemical properties filters">

            <!-- Results Count & Clear All - Improved Responsive Layout -->
            <div class="flex flex-col sm:flex-row items-center justify-between gap-3 mb-1">
                <p class="text-base md:text-lg font-medium text-base-content/80" aria-live="polite" aria-atomic="true">
                    <span class="font-semibold text-primary">{{ fetchChemicalStore.totalChemicals }}</span>
                    {{ fetchChemicalStore.totalChemicals === 1 ? 'result' : 'results' }} found
                </p>

                <button class="btn btn-sm md:btn-md btn-ghost hover:btn-error gap-2" @click="clearAllFilter"
                    :disabled="loading" :aria-label="`Clear all ${activeFilterCount} active filters`">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-5">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                    </svg>
                    <span class="hidden sm:inline">Clear All</span>
                </button>
            </div>

            <!-- Active Filter Chips for Better Clarity -->
            <div v-if="activeFilters.length > 0" class="flex flex-wrap gap-2 mt-3 mb-4" role="list"
                aria-label="Active filters">
                <div v-for="filter in activeFilters" :key="filter.propName"
                    class="badge badge-primary badge-lg gap-2 px-3 py-3" role="listitem">
                    <span class="text-sm font-medium">{{ filter.label }}: {{ filter.range }}</span>
                    <button type="button" @click="clearFilter(filter.propName, filter.rangeFilter)"
                        class="btn btn-ghost btn-xs btn-circle hover:bg-primary-content"
                        :aria-label="`Remove ${filter.label} filter`">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="size-4" viewBox="0 0 16 16">
                            <path
                                d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z" />
                        </svg>
                    </button>
                </div>
            </div>

            <div class="divider my-4"></div>

            <!-- Loading State with Better UX -->
            <div v-if="loading" class="flex flex-col items-center justify-center py-16 space-y-4" role="status"
                aria-live="polite" aria-busy="true">
                <span class="loading loading-spinner loading-lg text-primary"></span>
                <p class="text-base-content/60 text-sm">Loading filter options...</p>
            </div>

            <!-- Filter Grid with Improved Cards -->
            <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div v-for="data in histogramDataArr" :key="data.id"
                    class="card bg-base-200 shadow-sm hover:shadow-md transition-shadow duration-200">
                    <template v-if="data.data.length > 1">
                        <div class="card-body p-5">
                            <!-- Filter Header with Clear Button -->
                            <div class="flex items-center justify-between mb-3">
                                <h3 class="card-title text-base md:text-lg font-semibold text-primary">
                                    {{ data.label }}
                                </h3>
                                <button v-if="histogramRangeSliderStore.properties[data.propName].filterActivated"
                                    type="button"
                                    class="btn btn-ghost btn-sm btn-circle hover:btn-error tooltip tooltip-left"
                                    data-tip="Clear this filter" @click="clearFilter(data.propName, data.rangeFilter)"
                                    :aria-label="`Clear ${data.label} filter`">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="size-5"
                                        viewBox="0 0 16 16">
                                        <path
                                            d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z" />
                                    </svg>
                                </button>
                            </div>

                            <!-- Histogram Range Slider Component -->
                            <HistogramRangeSlider class="w-full" :chemPropArr="data.data" :step="data.step"
                                :rangeFilter="data.rangeFilter" :propName="data.propName"
                                @reloadHistogramRangeSlider="reloadHistogramRangeSliderDiv" />

                            <!-- Optional: Show current range values -->
                            <div v-if="histogramRangeSliderStore.properties[data.propName].filterActivated"
                                class="mt-3 pt-3 border-t border-base-300">
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
            </div>
        </section>

        <!-- Empty State with Better UX -->
        <section v-if="fetchChemicalStore.chemicals.length === 0"
            class="flex flex-col items-center justify-center text-center py-16 px-4 space-y-4" role="alert">
            <div class="text-6xl">🔍</div>
            <h2 class="text-2xl font-bold text-base-content">No Results Found</h2>
            <p class="text-base-content/70 max-w-md">
                We couldn't find any chemicals matching your current filters.
                Try adjusting your filter criteria or clearing all filters to see more results.
            </p>
            <div class="flex gap-3 mt-6">
                <button class="btn btn-primary" @click="clearAllFilter"
                    aria-label="Reset all filters and show all results">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-5">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
                    </svg>
                    Reset All Filters
                </button>
            </div>
        </section>
    </main>
</template>

<script setup>
import HistogramRangeSlider from "~/components/HistogramRangeSlider.vue"
import { useChemicalPropertiesListStore } from "~/stores/chemicalPropertiesList"
import { useFetchChemicalStore } from "~/stores/fetchChemicalStore"
import { useFilterStore } from "~/stores/filterStore"
import { useHistogramRangeSliderStore } from "~/stores/histogramRangeSliderStore"
import { onUnmounted, onMounted, computed } from "vue"

const chemicalPropertiesListStore = useChemicalPropertiesListStore()
const fetchChemicalStore = useFetchChemicalStore()
const filterStore = useFilterStore()
const histogramRangeSliderStore = useHistogramRangeSliderStore()

const histogramRangeSliderDiv = ref(1)
const loading = ref(false)
const histogramDataArr = ref([])

// Computed property to track active filters
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

// Computed property for active filter count
const activeFilterCount = computed(() => activeFilters.value.length)

// Format filter range for display
const formatFilterRange = (propName) => {
    const props = histogramRangeSliderStore.properties[propName]
    if (!props || !props.filterActivated) return ''

    // This is a placeholder - adjust based on your actual store structure
    return `${props.min ?? 'N/A'} - ${props.max ?? 'N/A'}`
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
                label: 'Melting Point, ºC',
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
            },
            {
                id: 3,
                label: "Lipinski's Rule of Five",
                data: chemicalPropertiesListStore.properties.count_lipinski_violation,
                step: 1,
                rangeFilter: {
                    gte: { name: 'count_lipinski_violation' },
                    lte: { name: 'count_lipinski_violation' }
                },
                propName: 'lipinski_violation'
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
                label: 'JPLogP',
                data: chemicalPropertiesListStore.properties.jplogp,
                step: 1,
                rangeFilter: {
                    gte: { name: 'jplogp' },
                    lte: { name: 'jplogp' }
                },
                propName: 'jplogp'
            },
            {
                id: 8,
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
                id: 9,
                label: 'Polar Area, Å²',
                data: chemicalPropertiesListStore.properties.tpsa,
                step: 10,
                rangeFilter: {
                    gte: { name: 'tpsa' },
                    lte: { name: 'tpsa' }
                },
                propName: 'tpsa'
            },
            {
                id: 10,
                label: "PAINS Alert Count",
                data: chemicalPropertiesListStore.properties.count_pains_alert,
                step: 1,
                rangeFilter: {
                    gte: { name: 'count_pains_alert' },
                    lte: { name: 'count_pains_alert' }
                },
                propName: 'pains_alert'
            }
        ]
    } catch (error) {
        console.error('Error loading chemical properties:', error)
        // Consider adding user-facing error handling here
    } finally {
        loading.value = false
    }
}

const clearAllFilter = () => {
    histogramRangeSliderStore.$reset()
    filterStore.clearAllRangeFilter()
    fetchChemicalStore.fetchChemicals()
    reloadHistogramRangeSliderDiv()
}

const clearFilter = (propName, rangeFilter) => {
    histogramRangeSliderStore.resetProperty(propName)
    filterStore.clearRangeFilter(rangeFilter.gte.name, 'gte')
    filterStore.clearRangeFilter(rangeFilter.lte.name, 'lte')
    reloadHistogramRangeSliderDiv()
    fetchChemicalStore.fetchChemicals()
}

onMounted(() => {
    if (fetchChemicalStore.chemicals.length !== 0) {
        loadChemPropsList()
    }
})

onUnmounted(() => {
    chemicalPropertiesListStore.$reset()
})
</script>
