<template>
    <div :key="histogramRangeSliderDiv">
        <div class="text-lg grid grid-cols-2">
            <p class="my-auto mr-auto md:mx-auto">Showing {{ paginationStore.totalItems }} results</p>
            <button class="btn btn-md btn-ghost hover:text-primary ml-auto md:mx-auto my-auto" @click="clearAllFilter">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                </svg>
                <p class="text-lg hidden md:flex">Clear All</p>
            </button>
        </div>
        <div class="divider"></div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <template v-for="data in histogramDataArr" :key="data.id">
                <div class="mx-auto" v-if="data.data.length > 1">
                    <div class="flex">
                        <p class="mr-auto text-lg font-semibold text-center md:text-left my-auto">{{ data.label }}</p>
                        <button type="button" class="btn btn-ghost btn-sm text-lg ml-auto my-auto" v-if="histogramRangeSliderStore.properties[data.propName].filterActivated" @click="clearFilter(data.propName, data.rangeFilter)">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-x-lg size-6" viewBox="0 0 16 16">
                              <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
                            </svg>
                        </button>
                    </div>
                    <div class="divider"></div>
                    <histogram-range-slider 
                        class="mx-auto" 
                        :chemPropArr="data.data" 
                        :step="data.step"
                        :rangeFilter="data.rangeFilter"
                        :propName="data.propName"
                        @reloadHistogramRangeSlider="reloadHistogramRangeSliderDiv"
                    />
                </div>
            </template>
        </div>
    </div>
    
    <div v-if="fetchChemicalStore.chemicals.length === 0" class="space-y-2 mx-auto p-8">
        <h1 class="text-xl font-semibold text-center">No results available to filter</h1>
        <h1 class="text-lg  text-center">Maybe you could remove some filters or do a new search</h1>
    </div>
</template>

<script setup>
import HistogramRangeSlider from "~/components/HistogramRangeSlider.vue"
import { useChemicalPropertiesListStore } from "~/stores/chemicalPropertiesList"
import { useFetchChemicalStore } from "~/stores/fetchChemicalStore";
import { usePaginationStore } from "~/stores/paginationStore";
import { useFilterStore } from "~/stores/filterStore";
import { useHistogramRangeSliderStore } from "~/stores/histogramRangeSliderStore";

const chemicalPropertiesListStore = useChemicalPropertiesListStore()
const fetchChemicalStore = useFetchChemicalStore()
const paginationStore = usePaginationStore()
const filterStore = useFilterStore()
const histogramRangeSliderStore = useHistogramRangeSliderStore()

const histogramRangeSliderDiv = ref(1)

var histogramDataArr = ref([])

const emit = defineEmits(['closeModal'])

async function reloadHistogramRangeSliderDiv() {
    await loadChemPropsList()
    histogramRangeSliderDiv.value *= -1 
}

function closeModal() {
    emit('closeModal')
}

const loadChemPropsList = async () => {
    await chemicalPropertiesListStore.fetchAllChemicalProperties()

    histogramDataArr.value = [
        {
            id: 1,
            label: 'Molecular Weight, g/mol',
            data: chemicalPropertiesListStore.properties.molecular_weight,
            step: 25,
            rangeFilter: {
                gte: {
                    name: 'molecular_weight',
                    
                },
                lte: {
                    name: 'molecular_weight',
                }
                
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
                gte: {
                    name: 'mp_lower_bound',
                    
                },
                lte: {
                    name: 'mp_upper_bound',
                    
                }
                
            },
            propName: 'melting_point'
        },
        {
            id: 3,
            label: "Lipinski's Rule of Five Count",
            data: chemicalPropertiesListStore.properties.count_lipinski_violation,
            step: 1,
            rangeFilter: {
                gte: {
                    name: 'count_lipinski_violation',
                    
                },
                lte: {
                    name: 'count_lipinski_violation',
                    
                }
                
            },
            propName: 'lipinski_violation'
        },
        
        {
            id: 4,
            label: 'Rotatable Bond Count',
            data: chemicalPropertiesListStore.properties.rotatable_bond,
            step: 1,
            rangeFilter: {
                gte: {
                    name: 'count_rotatable_bond',
                    
                },
                lte: {
                    name: 'count_rotatable_bond',
                    
                }
                
            },
            propName: 'rotatable_bond'
        },
        {
            id: 5,
            label: 'H-Bond Donor Count',
            data: chemicalPropertiesListStore.properties.h_bond_donor,
            step: 1,
            rangeFilter: {
                gte: {
                    name: 'count_h_bond_donor',
                    
                },
                lte: {
                    name: 'count_h_bond_donor',
                    
                }
            },
            propName: 'h_bond_donor'
        },
        {
            id: 6,
            label: 'H-Bond Acceptor Count',
            data: chemicalPropertiesListStore.properties.h_bond_acceptor,
            step: 1,
            rangeFilter: {
                gte: {
                    name: 'count_h_bond_acceptor',
                },
                lte: {
                    name: 'count_h_bond_acceptor',
                    
                }
            },
            propName: 'h_bond_acceptor'
        },
        {
            id: 7,
            label: 'JPLogP',
            data: chemicalPropertiesListStore.properties.jplogp,
            step: 1,
            rangeFilter: {
                gte: {
                    name: 'jplogp',
                    
                },
                lte: {
                    name: 'jplogp',
                    
                }
            },
            propName: 'jplogp'
        },
        {
            id: 8,
            label: 'Heavy Atom Count',
            data: chemicalPropertiesListStore.properties.heavy_atom,
            step: 5,
            rangeFilter: {
                gte: {
                    name: 'count_heavy_atom',
                    
                },
                lte: {
                    name: 'count_heavy_atom',
                    
                }
            },
            propName: 'heavy_atom'
        },
        {
            id: 9,
            label: 'Polar Area, Å²',
            data: chemicalPropertiesListStore.properties.tpsa,
            step: 10,
            rangeFilter: {
                gte: {
                    name: 'tpsa',
                    
                },
                lte: {
                    name: 'tpsa',
                    
                }
            },
            propName: 'tpsa'
        },
        {
            id: 10,
            label: "PAINS Alert Count",
            data: chemicalPropertiesListStore.properties.count_pains_alert,
            step: 1,
            rangeFilter: {
                gte: {
                    name: 'count_pains_alert',
                    
                },
                lte: {
                    name: 'count_pains_alert',
                    
                }
                
            },
            propName: 'pains_alert'
        },
    ]
}

const clearAllFilter = () => {
    histogramRangeSliderStore.resetProperties()
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
    if(fetchChemicalStore.chemicals.length !== 0) {
        loadChemPropsList()
    }
})
</script>