<!-- pages/chemicals/search/advanced.vue -->
<template>
  <main class="min-h-screen bg-base-200">
    <Head>
      <Title>Advanced Search | LabSOADB</Title>
    </Head>

    <!-- Hero Search Section -->
    <section class="relative bg-gradient-to-br from-primary/10 via-base-100 to-secondary/10">
      <div class="container mx-auto px-4 py-12 lg:py-16">
        <div class="max-w-4xl mx-auto text-center mb-8">
          <h1 class="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
            Advanced Chemical Search
          </h1>
          <p class="text-base md:text-lg lg:text-xl text-base-content/70 max-w-3xl mx-auto">
            Refine your search with detailed molecular properties, drug-likeness parameters, and literature filters
          </p>
        </div>

        <!-- Main Search Field -->
        <div class="max-w-4xl mx-auto">
          <SearchField :typewriterEffect="true" />
        </div>
      </div>
    </section>

    <!-- Advanced Filters Section -->
    <div class="container mx-auto px-4 py-8">
      <!-- Active Filters Summary -->
      <div v-if="activeFiltersCount > 0" class="alert mb-6 shadow-lg">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-info shrink-0 w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <div class="flex-1">
          <span class="font-semibold">{{ activeFiltersCount }} active filter{{ activeFiltersCount > 1 ? 's' : '' }}</span>
        </div>
        <button @click="handleClearAllFilters" class="btn btn-sm btn-ghost gap-2">
          <XMarkIcon class="h-5 w-5" />
          Clear all
        </button>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Filters Sidebar -->
        <aside class="lg:col-span-1 space-y-4">
          <!-- Literature Filters -->
          <LiteratureFilters />
          
          <!-- Molecular Properties -->
          <div class="collapse collapse-arrow bg-base-100 shadow-lg border border-base-300">
            <input type="checkbox" v-model="sectionsExpanded.molecular" />
            <div class="collapse-title text-lg font-semibold flex items-center gap-2">
              <BeakerIcon class="h-5 w-5" />
              Molecular Properties
              <span v-if="getMolecularFiltersCount > 0" class="badge badge-primary badge-sm ml-auto">
                {{ getMolecularFiltersCount }}
              </span>
            </div>
            <div class="collapse-content">
              <MolecularPropertiesFilters />
            </div>
          </div>

          <!-- Drug-Likeness -->
          <div class="collapse collapse-arrow bg-base-100 shadow-lg border border-base-300">
            <input type="checkbox" v-model="sectionsExpanded.drugLikeness" />
            <div class="collapse-title text-lg font-semibold flex items-center gap-2">
              <CubeIcon class="h-5 w-5" />
              Drug-Likeness
              <span v-if="getDrugLikenessFiltersCount > 0" class="badge badge-primary badge-sm ml-auto">
                {{ getDrugLikenessFiltersCount }}
              </span>
            </div>
            <div class="collapse-content">
              <DrugLikenessFilters />
            </div>
          </div>

          <!-- Pharmacokinetics -->
          <div class="collapse collapse-arrow bg-base-100 shadow-lg border border-base-300">
            <input type="checkbox" v-model="sectionsExpanded.pharmacokinetics" />
            <div class="collapse-title text-lg font-semibold flex items-center gap-2">
              <ChartBarIcon class="h-5 w-5" />
              Pharmacokinetics
              <span v-if="getPharmacokineticsFiltersCount > 0" class="badge badge-primary badge-sm ml-auto">
                {{ getPharmacokineticsFiltersCount }}
              </span>
            </div>
            <div class="collapse-content">
              <PharmacokineticsFilters />
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="sticky bottom-4 flex flex-col gap-2 bg-base-200 p-4 rounded-lg shadow-lg border border-base-300">
            <button @click="handleSearch" class="btn btn-primary w-full gap-2" :disabled="isSearching">
              <MagnifyingGlassIcon class="h-5 w-5" />
              {{ isSearching ? 'Searching...' : 'Search' }}
              <span v-if="isSearching" class="loading loading-spinner loading-sm"></span>
            </button>
            <button @click="handleClearAllFilters" class="btn btn-outline w-full gap-2">
              <ArrowPathIcon class="h-5 w-5" />
              Reset All Filters
            </button>
          </div>
        </aside>

        <!-- Preview/Info Panel -->
        <main class="lg:col-span-3">
          <div class="card bg-base-100 shadow-lg border border-base-300">
            <div class="card-body">
              <h2 class="card-title text-2xl mb-4">Search Tips</h2>
              
              <div class="space-y-6">
                <!-- Query Types -->
                <div>
                  <h3 class="font-semibold text-lg mb-3 flex items-center gap-2">
                    <DocumentTextIcon class="h-5 w-5 text-primary" />
                    Supported Query Types
                  </h3>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div class="group rounded-lg bg-base-200/100 hover:bg-base-200 border border-base-300 hover:border-primary/50 flex flex-col p-4 md:p-6 h-auto transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
                      <p class="font-medium mb-1">SMILES</p>
                      <code class="text-sm">C1=CC=C(C=C1)C=O</code>
                      <p class="text-xs text-base-content/70 mt-2">Simplified Molecular Input Line Entry System</p>
                    </div>
                    <div class="group rounded-lg bg-base-200/100 hover:bg-base-200 border border-base-300 hover:border-primary/50 flex flex-col p-4 md:p-6 h-auto transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
                      <p class="font-medium mb-1">SMARTS</p>
                      <code class="text-sm">[X3&H0]</code>
                      <p class="text-xs text-base-content/70 mt-2">Substructure search pattern</p>
                    </div>
                    <div class="group rounded-lg bg-base-200/100 hover:bg-base-200 border border-base-300 hover:border-primary/50 flex flex-col p-4 md:p-6 h-auto transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
                      <p class="font-medium mb-1">InChI</p>
                      <code class="text-sm text-xs">InChI=1S/C3H6O/c1-3(2)4...</code>
                      <p class="text-xs text-base-content/70 mt-2">International Chemical Identifier</p>
                    </div>
                    <div class="group rounded-lg bg-base-200/100 hover:bg-base-200 border border-base-300 hover:border-primary/50 flex flex-col p-4 md:p-6 h-auto transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
                      <p class="font-medium mb-1">Formula</p>
                      <code class="text-sm">C25H20O4</code>
                      <p class="text-xs text-base-content/70 mt-2">Molecular formula</p>
                    </div>
                  </div>
                </div>

                <!-- Filter Categories -->
                <div>
                  <h3 class="font-semibold text-lg mb-3 flex items-center gap-2">
                    <FunnelIcon class="h-5 w-5 text-primary" />
                    Available Filter Categories
                  </h3>
                  <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <div class="group rounded-lg bg-base-200/100 hover:bg-base-200 border border-base-300 hover:border-primary/50 flex flex-col p-4 md:p-6 h-auto transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
                      <div class="stat-title">Physical Properties</div>
                      <div class="stat-value text-2xl">15+</div>
                      <div class="stat-desc">MW, atoms, bonds, rings</div>
                    </div>
                    <div class="group rounded-lg bg-base-200/100 hover:bg-base-200 border border-base-300 hover:border-primary/50 flex flex-col p-4 md:p-6 h-auto transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
                      <div class="stat-title">Drug-Likeness</div>
                      <div class="stat-value text-2xl">12+</div>
                      <div class="stat-desc">Lipinski, QED, SA Score</div>
                    </div>
                    <div class="group rounded-lg bg-base-200/100 hover:bg-base-200 border border-base-300 hover:border-primary/50 flex flex-col p-4 md:p-6 h-auto transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
                      <div class="stat-title">Pharmacokinetics</div>
                      <div class="stat-value text-2xl">7+</div>
                      <div class="stat-desc">ADME, CYP inhibition</div>
                    </div>
                  </div>
                </div>

                <!-- Quick Start -->
                <div class="alert alert-info">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <div>
                    <h4 class="font-bold">Quick Start</h4>
                    <p class="text-sm">Start with a query in the search box above, then refine results using filters on the left. Click "Search" to view results.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed, provide } from 'vue'
import { useRouter } from 'vue-router'
import { useFilterStore } from '~/stores/filterStore'
import { useFetchChemicalStore } from '~/stores/fetchChemicalStore'
import { useHistogramRangeSliderStore } from '~/stores/histogramRangeSliderStore'
import { useChemicalPropertiesListStore } from '~/stores/chemicalPropertiesList'
import { useSortStore } from '~/stores/sortingStore'

import SearchField from '~/components/SearchField.vue'
import LiteratureFilters from '~/components/search/advanced/LiteratureFilters.vue'
import MolecularPropertiesFilters from '~/components/search/advanced/MolecularPropertiesFilters.vue'
import DrugLikenessFilters from '~/components/search/advanced/DrugLikenessFilters.vue'
import PharmacokineticsFilters from '~/components/search/advanced/PharmacokineticsFilters.vue'

import {
  MagnifyingGlassIcon,
  ArrowPathIcon,
  XMarkIcon,
  BeakerIcon,
  CubeIcon,
  ChartBarIcon,
  DocumentTextIcon,
  FunnelIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const filterStore = useFilterStore()
const fetchChemicalStore = useFetchChemicalStore()
const chemicalPropertiesListStore = useChemicalPropertiesListStore()
const histogramRangeSliderStore = useHistogramRangeSliderStore()
const sortStore = useSortStore()

const isSearching = ref(false)
const sectionsExpanded = ref({
  molecular: false,
  drugLikeness: false,
  pharmacokinetics: false
})

// Computed
const activeFiltersCount = computed(() => {
  let count = 0
  
  // Count exact filters
  Object.entries(filterStore.filters.exact).forEach(([key, value]) => {
    if (value && value !== '') count++
  })
  
  // Count range filters
  Object.entries(filterStore.filters.range).forEach(([key, range]) => {
    if (range.gte != null || range.lte != null) count++
  })
  
  return count
})

const getMolecularFiltersCount = computed(() => {
  let count = 0
  const molecularProps = [
    'molecular_weight', 'tpsa', 'count_heavy_atom', 
    'count_rotatable_bond', 'count_h_bond_donor', 'count_h_bond_acceptor',
    'mp_lower_bound', 'mp_upper_bound'
  ]
  
  molecularProps.forEach(prop => {
    const range = filterStore.filters.range[prop]
    if (range && (range.gte != null || range.lte != null)) count++
  })
  
  return count
})

const getDrugLikenessFiltersCount = computed(() => {
  let count = 0
  const drugLikeProps = ['count_lipinski_violation', 'count_pains_alert', 'jplogp']
  
  drugLikeProps.forEach(prop => {
    const range = filterStore.filters.range[prop]
    if (range && (range.gte != null || range.lte != null)) count++
  })
  
  return count
})

const getPharmacokineticsFiltersCount = computed(() => {
  let count = 0
  // Add logic for pharmacokinetics filters when implemented
  return count
})

// Methods
const handleSearch = async () => {
  isSearching.value = true
  
  try {
    fetchChemicalStore.setType('search')
    fetchChemicalStore.setMode('summary')
    await fetchChemicalStore.fetchChemicals()
    
    router.push('/chemicals/search')
  } catch (error) {
    console.error('Search error:', error)
  } finally {
    isSearching.value = false
  }
}

const handleClearAllFilters = async () => {
  // Reseta as stores
  histogramRangeSliderStore.$reset()
  filterStore.$reset()  // ✅ Usando $reset() ao invés de método customizado
  sortStore.$reset()

  // Busca novos dados
  await fetchChemicalStore.fetchChemicals()

  // ✅ Recarrega histogramas (FALTAVA ISSO!)
  await chemicalPropertiesListStore.fetchAllChemicalProperties()

  // ✅ Força reload visual dos histogramas nos componentes filhos
  // Trigger para MolecularPropertiesFilters e DrugLikenessFilters
  reloadHistogramTrigger.value *= -1
}

// Provide para os componentes filhos
const reloadHistogramTrigger = ref(1)
provide('reloadHistogramTrigger', reloadHistogramTrigger)
</script>
