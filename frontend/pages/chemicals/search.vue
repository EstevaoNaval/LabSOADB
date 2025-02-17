<template>
    <Head>
        <Title>Search | LabSOADB</Title>
    </Head>
    <div class="h-full flex flex-col items-center justify-center">
        <div class="w-full flex flex-col gap-8" :key="searchResultsDiv">
            <section class="search_bar_background bg-scroll bg-cover bg-center">
                <div class="bg-opacity-80 h-full bg-base-300 py-8 space-y-8">
                    <div class="gap-4 w-3/4 mx-auto hidden xl:flex xl:flex-col">
                        <h1 class="text-4xl font-bold">Search Chemicals</h1>
                        <h1 class="text-2xl w-3/4">
                            Explore LabSOADB to find chemicals with ease. Feel free to search, 
                            filter, and accurately analyze our database, leveraging advanced tools 
                            to streamline discovery and data insights.
                        </h1>
                    </div>
                
                    <div class="gap-4 w-[90%] mx-auto hidden md:flex md:flex-col xl:hidden">
                        <h1 class="text-4xl font-bold">Search Chemicals</h1>
                        <h1 class="text-xl">
                            Explore LabSOADB to find chemicals with ease. Feel free to search, 
                            filter, and accurately analyze our database, leveraging advanced tools 
                            to streamline discovery and data insights.
                        </h1>
                    </div>
                
                    <div class="gap-4 w-[90%] mx-auto flex flex-col md:hidden">
                        <h1 class="text-2xl font-bold">Search Chemicals</h1>
                        <h1 class="text-md mb-4">
                            Explore LabSOADB to find chemicals with ease. Feel free to search, 
                            filter, and accurately analyze our database, leveraging advanced tools 
                            to streamline discovery and data insights.
                        </h1>
                    </div>

                    <div class="mx-auto w-[90%] xl:w-3/4">
                        <search-field :typewriterEffect='true'></search-field>
                    </div>
                </div>
            </section>
            <div class="w-[90%] m-auto hidden xl:flex" v-if="paginationStore.totalItems > 0 && paginationStore.totalPages > 1">
                <p class="text-lg mr-auto">
                    Showing {{ 1 + paginationStore.pageSize * (paginationStore.page - 1)}} to {{ paginationStore.pageSize * paginationStore.page < paginationStore.totalItems ? paginationStore.pageSize * paginationStore.page : paginationStore.totalItems}} of {{ paginationStore.totalItems }} results
                </p>
                <pagination></pagination>
            </div>
            <div class="w-[90%] gap-4 items-center hidden m-auto md:flex md:flex-col xl:hidden" v-if="paginationStore.totalItems > 0 && paginationStore.totalPages > 1">
                <pagination></pagination>
                <p class="text-lg">
                    Showing {{ 1 + paginationStore.pageSize * (paginationStore.page - 1)}} to {{ paginationStore.pageSize * paginationStore.page < paginationStore.totalItems ? paginationStore.pageSize * paginationStore.page : paginationStore.totalItems}} of {{ paginationStore.totalItems }} results
                </p>
            </div>
            <div class="w-[90%] flex flex-col mx-auto md:hidden" v-if="paginationStore.totalItems > 0 && paginationStore.totalPages > 1">
                <div class="flex mx-auto flex-col gap-4">
                    <pagination class="mx-auto"></pagination>
                </div>
            </div>

            <div class="w-[90%] mx-auto">
                
                <div class="mb-6 hidden lg:flex">
                    <h1 class="text-2xl font-semibold mr-auto my-auto">Search Results</h1>
                    <export></export>
                    <button type="button" class="btn btn-ghost my-auto hover:text-primary" @click="openFilterModal">
                        <svg xmlns="http://www.w3.org/2000/svg" stroke-width="1.5" fill="currentColor" class="bi bi-filter size-8" viewBox="0 0 16 16">
                          <path d="M6 10.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5m-2-3a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5m-2-3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5"/>
                        </svg>
                        <h1 class="text-xl">Filter</h1>
                    </button>
                    <sorting class="ml-auto"></sorting>
                    
                </div>
                
                <div class="mb-6 hidden md:flex lg:hidden">
                    <h1 class="text-2xl font-semibold mr-auto my-auto">Search Results</h1>
                    <export></export>
                    <button type="button" class="btn btn-ghost my-auto hover:text-primary" @click="openFilterModal">
                        <svg xmlns="http://www.w3.org/2000/svg" stroke-width="1.5" fill="currentColor" class="bi bi-filter size-8" viewBox="0 0 16 16">
                          <path d="M6 10.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5m-2-3a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5m-2-3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5"/>
                        </svg>
                    </button>
                    <sorting class="ml-auto"></sorting>
                </div>
                
                <div class="mb-4 m-auto flex md:hidden">
                    <h1 class="text-lg font-semibold my-auto mr-auto">Search Results</h1>
                    <export></export>
                    <button type="button" class="btn btn-ghost btn-sm my-auto" @click="openFilterModal">
                        <svg xmlns="http://www.w3.org/2000/svg" stroke-width="1.5" fill="currentColor" class="bi bi-filter size-6" viewBox="0 0 16 16">
                          <path d="M6 10.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5m-2-3a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5m-2-3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5"/>
                        </svg>
                    </button>
                    <sorting class="ml-auto"></sorting>
                </div>
                
                <!-- Mostrar uma mensagem de carregamento ou de erro -->
                <div v-if="fetchChemicalStore.loading" class="text-center">
                    <span class="loading loading-spinner loading-lg"></span>
                </div>
                
                <!-- Renderizar os cards de químicos -->
                <div v-if="!fetchChemicalStore.loading && fetchChemicalStore.chemicals.length > 0" class="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    <chemical-card @click="routeToSelectedChemicalDetailPage(chemical.api_id)" role="button" class="cursor-pointer transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-xl" v-for="chemical in fetchChemicalStore.chemicals" :key="chemical.api_id" :chemical="chemical" />
                </div>
            
                <!-- Exibir uma mensagem se não houver resultados -->
                <div v-if="!fetchChemicalStore.loading && fetchChemicalStore.chemicals.length === 0" class="space-y-2">
                    <NuxtImg src="/images/empty_state_illustration_dark.png" v-if="themeStore.isDarkMode" class="md:h-[36rem] md:w-[36rem] mx-auto" format="png" loading="lazy" />
                    <NuxtImg src="/images/empty_state_illustration_light.png" v-else class="md:h-[36rem] md:w-[36rem] mx-auto" format="png" loading="lazy" />
                    <div class="p-8">
                        <h1 class="text-center text-lg md:text-2xl font-semibold">No results found</h1>
                        <h1 class="text-center md:text-lg">No chemicals matched your criteria. Try searching for something else.</h1>
                    </div>
                </div>
            </div>

            <div class="mb-8 w-[90%] m-auto hidden xl:flex" v-if="paginationStore.totalItems > 0 && paginationStore.totalPages > 1">
                <p class="text-lg mr-auto">
                    Showing {{ 1 + paginationStore.pageSize * (paginationStore.page - 1)}} to {{ paginationStore.pageSize * paginationStore.page < paginationStore.totalItems ? paginationStore.pageSize * paginationStore.page : paginationStore.totalItems}} of {{ paginationStore.totalItems }} results
                </p>
                <pagination></pagination>
            </div>
            <div class="mb-8 w-[90%] gap-4 items-center hidden m-auto md:flex md:flex-col xl:hidden" v-if="paginationStore.totalItems > 0 && paginationStore.totalPages > 1">
                <pagination></pagination>
                <p class="text-lg">
                    Showing {{ 1 + paginationStore.pageSize * (paginationStore.page - 1)}} to {{ paginationStore.pageSize * paginationStore.page < paginationStore.totalItems ? paginationStore.pageSize * paginationStore.page : paginationStore.totalItems}} of {{ paginationStore.totalItems }} results
                </p>
            </div>
            <div class="mb-8 w-[90%] flex flex-col mx-auto md:hidden" v-if="paginationStore.totalItems > 0 && paginationStore.totalPages > 1">
                <div class="flex mx-auto flex-col gap-4">
                    <pagination class="mx-auto"></pagination>
                </div>
            </div>
        </div>
    </div>
    <modal ref="filterModalRef">
        <filter-component></filter-component>
    </modal>
</template>

<script setup>
import { provide, ref, defineAsyncComponent } from 'vue';
import { usePaginationStore } from '~/stores/paginationStore';
import { useThemeStore } from '~/stores/theme';
import { useSortStore } from '~/stores/sortingStore'
import { useRouter } from 'vue-router'
import { useFetchChemicalStore } from '~/stores/fetchChemicalStore'

import Pagination from '~/components/Pagination.vue';
import SearchField from '~/components/SearchField.vue'
import ChemicalCard from '~/components/ChemicalCard.vue';
import Sorting from '~/components/Sorting.vue'
import Export from '~/components/Export.vue'
import Modal from '~/components/Modal.vue';

const FilterComponent = defineAsyncComponent({
    loader: () => import('~/components/FilterComponent.vue')
});

const filterModalRef = ref(null)

var router = useRouter()

// Stores
const themeStore = useThemeStore()
const paginationStore = usePaginationStore()
const sortStore = useSortStore();
const fetchChemicalStore = useFetchChemicalStore()

const searchResultsDiv = ref(1)

paginationStore.setPageSize(10)
paginationStore.calcTotalPages()


function openFilterModal() {
    if(filterModalRef.value) {
        filterModalRef.value.toggleComponentModal()
    }
}

function reloadSearchResultsDiv() {
    paginationStore.setPage(1);
    searchResultsDiv.value *= -1
}

function routeToSelectedChemicalDetailPage(labsoadbId) {
    router.push({
        path: `/chemicals/${labsoadbId}`,
    })
} 

onMounted(() => {
    paginationStore.setPage(1);
    fetchChemicalStore.fetchChemicals()
})

watch(() => paginationStore.page, () => {
    fetchChemicalStore.fetchChemicals();
});

watch(() => [sortStore.currSortOptionId, sortStore.ascDirection], () => {
    paginationStore.setPage(1);
    fetchChemicalStore.fetchChemicals();
})

provide('reloadSearchResultsDiv', reloadSearchResultsDiv);
</script>

<style scoped>
    .search_bar_background {
        background-image: url('~/assets/search_page_search_bar_background.webp');
    }

    html[data-theme='winter'] .feature-section-border {
        border-top-width: 1px;
        border-bottom-width: 1px;
        border-top-color: #e2e8f0;
        border-bottom-color: #e2e8f0;
    }

    html[data-theme='night'] .feature-section-border {
        border-top-width: 1px;
        border-bottom-width: 1px;
        border-top-color: #1e293b;
        border-bottom-color:#1e293b;
    }
</style>