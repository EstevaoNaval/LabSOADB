<template>
  <main class="min-h-screen bg-base-200">
    <Head>
      <Title>Search | LabSOADB</Title>
    </Head>

    <!-- Hero Search Section -->
    <section class="relative bg-gradient-to-br from-primary/10 via-base-100 to-secondary/10">
      <div class="container mx-auto px-4 py-12 lg:py-16">
        <div class="max-w-4xl mx-auto text-center mb-8">
          <h1 class="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
            Search Chemicals
          </h1>
          <p class="text-base md:text-lg lg:text-xl text-base-content/70 max-w-3xl mx-auto">
            Explore LabSOADB to find chemicals with ease. Search, filter, and analyze our database 
            using advanced tools to streamline discovery and data insights.
          </p>
        </div>

        <div class="max-w-4xl mx-auto">
          <search-field :typewriterEffect="true" />
        </div>
      </div>
    </section>

    <!-- Results Section -->
    <div class="container mx-auto px-4 py-8 space-y-6">
      <!-- Top Pagination & Controls -->
      <div v-if="pagination.state.totalItems > 0" class="card bg-base-100 shadow-lg">
        <div class="card-body p-4 md:p-6">
          <div class="flex flex-col lg:flex-row items-center justify-between gap-4">
            <!-- Results Count -->
            <div class="text-sm text-base-content/70 order-2 lg:order-1">
              Showing 
              <span class="font-semibold">{{ 1 + pagination.state.pageSize * (pagination.state.page - 1) }}</span>
              to 
              <span class="font-semibold">{{ Math.min(pagination.state.pageSize * pagination.state.page, pagination.state.totalItems) }}</span>
              of 
              <span class="font-semibold">{{ pagination.state.totalItems }}</span>
              results
            </div>

            <!-- Pagination -->
            <div class="order-1 lg:order-2" v-if="pagination.getTotalPages() > 1">
              <Pagination :pagination="pagination" />
            </div>
          </div>
        </div>
      </div>

    <!-- Controls Bar -->
    <div class="card bg-base-100 shadow-lg border border-base-300">
      <div class="card-body p-4 md:p-6">
        <!-- Desktop Layout -->
        <div class="hidden md:flex items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <h2 class="text-xl lg:text-2xl font-bold text-base-content">Search Results</h2>
            <div class="badge badge-primary badge-lg" v-if="totalResults">
              {{ totalResults.toLocaleString() }}
            </div>
          </div>

          <div class="flex items-center gap-2">
            <button 
              type="button" 
              class="btn btn-outline btn-primary gap-2"
              @click="openFilterModal"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z" />
              </svg>
              <span>Filter</span>
              <div class="badge badge-sm badge-secondary" v-if="activeFiltersCount">
                {{ activeFiltersCount }}
              </div>
            </button>
          
            <Sorting />

            <Export />
          </div>
        </div>
      
        <!-- Mobile Layout -->
        <div class="flex md:hidden flex-col gap-3">
          <!-- Title Row -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <h2 class="text-lg font-bold text-base-content">Search Results</h2>
              <div class="badge badge-primary" v-if="totalResults">
                {{ totalResults > 999 ? `${(totalResults / 1000).toFixed(1)}k` : totalResults }}
              </div>
            </div>


          </div>
        
          <!-- Actions Row -->
          <div class="flex items-center gap-2">
            <button 
              type="button" 
              class="btn btn-sm btn-outline btn-primary gap-2 flex-shrink-0"
              @click="openFilterModal"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z" />
              </svg>
              <span class="hidden sm:inline">Filter</span>
              <div class="badge badge-xs badge-secondary" v-if="activeFiltersCount">
                {{ activeFiltersCount }}
              </div>
            </button>
          
            <Sorting />
          
            <Export />
          </div>
        </div>
      </div>
    </div>

      <!-- Loading State -->
      <div v-if="fetchChemicalStore.loading" class="flex items-center justify-center py-20">
        <div class="text-center space-y-4">
          <span class="loading loading-spinner loading-lg text-primary"></span>
          <p class="text-base-content/70">Searching chemicals...</p>
        </div>
      </div>

      <!-- Results Grid -->
      <div 
        v-else-if="fetchChemicalStore.chemicals.length > 0" 
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
      >
        <ChemicalCard 
          v-for="chemical in fetchChemicalStore.chemicals" 
          :key="chemical.api_id" 
          :chemical="chemical"
          @click="routeToSelectedChemicalDetailPage(chemical.api_id)"
          class="cursor-pointer hover:scale-105 transition-transform duration-300"
        />
      </div>

      <!-- Empty State -->
      <div 
        v-else-if="!fetchChemicalStore.loading && fetchChemicalStore.chemicals.length === 0" 
        class="card bg-base-100 shadow-lg"
      >
        <div class="card-body items-center text-center py-16">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-24 h-24 text-base-content/30 mb-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607ZM10.5 7.5v6m3-3h-6" />
          </svg>
          <h3 class="text-2xl font-bold mb-2">No results found</h3>
          <p class="text-base-content/70 max-w-md">
            No chemicals matched your criteria. Try adjusting your search or filters.
          </p>
        </div>
      </div>

      <!-- Bottom Pagination -->
      <div v-if="pagination.state.totalItems > 0 && pagination.getTotalPages() > 1" class="card bg-base-100 shadow-lg">
        <div class="card-body p-4 md:p-6">
          <div class="flex flex-col lg:flex-row items-center justify-between gap-4">
            <div class="text-sm text-base-content/70 order-2 lg:order-1">
              Showing 
              <span class="font-semibold">{{ 1 + pagination.state.pageSize * (pagination.state.page - 1) }}</span>
              to 
              <span class="font-semibold">{{ Math.min(pagination.state.pageSize * pagination.state.page, pagination.state.totalItems) }}</span>
              of 
              <span class="font-semibold">{{ pagination.state.totalItems }}</span>
              results
            </div>

            <div class="order-1 lg:order-2">
              <Pagination :pagination="pagination" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filter Modal -->
    <Modal ref="filterModalRef">
      <FilterComponent />
    </Modal>
  </main>
</template>

<script setup>
import { provide, ref, defineAsyncComponent, watch, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { useFetchChemicalStore } from '~/stores/fetchChemicalStore'
import { useFilterStore } from '~/stores/filterStore'
import { useSortStore } from '~/stores/sortingStore'
import { usePagination } from '~/composables/usePagination'

import Pagination from '~/components/Pagination.vue'
import SearchField from '~/components/SearchField.vue'
import ChemicalCard from '~/components/ChemicalCard.vue'
import Sorting from '~/components/Sorting.vue'
import Export from '~/components/Export.vue'
import Modal from '~/components/Modal.vue'

const FilterComponent = defineAsyncComponent({
  loader: () => import('~/components/FilterComponent.vue')
})

const router = useRouter()

// Stores
const fetchChemicalStore = useFetchChemicalStore()
const filterStore = useFilterStore()
const sortStore = useSortStore()

// Composables
const pagination = usePagination()

// Refs
const filterModalRef = ref(null)
const searchResultsDiv = ref(1)

// Functions
function openFilterModal() {
  if (filterModalRef.value) {
    filterModalRef.value.toggleComponentModal()
  }
}

function reloadSearchResultsDiv() {
  pagination.setPage(1)
  searchResultsDiv.value *= -1
}

function routeToSelectedChemicalDetailPage(labsoadbId) {
  router.push(`/chemicals/${labsoadbId}`)
}

async function fetchChemicals(page) {
  pagination.setPage(page)
  await fetchChemicalStore.fetchChemicals({ page })
  pagination.setTotalItems(fetchChemicalStore.totalChemicals)
}

// Lifecycle
onBeforeMount(() => {
  fetchChemicals(1)
})

// Watchers
watch(() => fetchChemicalStore.totalChemicals, () => {
  pagination.setPage(1)
  pagination.setTotalItems(fetchChemicalStore.totalChemicals)
})

watch(() => pagination.state.page, () => {
  fetchChemicals(pagination.state.page)
})

watch(() => [sortStore.currSortOptionId, sortStore.ascDirection], () => {
  fetchChemicals(1)
})

// Provide
provide('reloadSearchResultsDiv', reloadSearchResultsDiv)
</script>