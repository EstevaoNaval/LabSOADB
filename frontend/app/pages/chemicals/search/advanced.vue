<!-- pages/chemicals/search/advanced.vue -->
<template>
  <main class="min-h-screen bg-gradient-to-br from-base-200 via-base-100 to-base-200 pb-20 sm:pb-0">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-primary/5 via-base-100 to-secondary/5 border-b border-base-300">
      <div class="container mx-auto px-4 py-6 lg:py-10">
        <div class="max-w-6xl mx-auto">
          <!-- Breadcrumbs -->
          <div class="breadcrumbs text-sm mb-4">
            <ul>
              <li><a href="/" class="link link-hover">Home</a></li>
              <li><a href="/chemicals" class="link link-hover">Chemicals</a></li>
              <li class="font-semibold">Advanced Search</li>
            </ul>
          </div>

          <div class="text-center mb-6">
            <!-- Badge -->
            <div class="inline-flex items-center gap-2 badge badge-lg badge-primary badge-outline mb-3">
              <ShieldCheckIcon class="h-4 w-4" />
              Advanced Filtering
            </div>
            
            <h1 class="text-2xl md:text-3xl lg:text-4xl font-bold mb-2 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              Advanced Chemical Search
            </h1>
            <p class="text-sm md:text-base text-base-content/70 max-w-2xl mx-auto">
              Refine your molecular search with powerful filters before querying our database
            </p>
          </div>

          <!-- Search Field -->
          <SearchField :typewriterEffect="true" />
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-6 max-w-7xl">
      
      <!-- Stats & Action Bar -->
      <div class="card bg-base-100 shadow-xl border border-base-300 mb-6">
        <div class="card-body p-4">
          <div class="flex flex-col gap-4">
            <!-- Stats Row -->
            <div class="flex flex-wrap items-center gap-3">
              <!-- Active Filters -->
              <div class="stats stats-horizontal shadow-sm bg-base-200 border border-base-300">
                <div class="stat p-3 min-w-[120px]">
                  <div class="stat-figure text-primary">
                    <FunnelIcon class="h-6 w-6" />
                  </div>
                  <div class="stat-title text-xs">Filters</div>
                  <div class="stat-value text-primary text-xl">{{ activeFiltersCount }}</div>
                </div>
              </div>

              <!-- Categories -->
              <div class="stats stats-horizontal shadow-sm bg-base-200 border border-base-300">
                <div class="stat p-3 min-w-[120px]">
                  <div class="stat-figure text-secondary">
                    <Squares2X2Icon class="h-6 w-6" />
                  </div>
                  <div class="stat-title text-xs">Categories</div>
                  <div class="stat-value text-secondary text-xl">{{ availableCategoriesCount }}</div>
                </div>
              </div>

              <!-- Results -->
              <div v-if="fetchChemicalStore.totalChemicals > 0" class="stats stats-horizontal shadow-sm bg-base-200 border border-base-300">
                <div class="stat p-3 min-w-[120px]">
                  <div class="stat-figure text-success">
                    <CheckCircleIcon class="h-6 w-6" />
                  </div>
                  <div class="stat-title text-xs">Results</div>
                  <div class="stat-value text-success text-xl">{{ formatNumber(fetchChemicalStore.totalChemicals) }}</div>
                </div>
              </div>

              <!-- Action Buttons Row - Desktop Only -->
              <div class="hidden sm:flex flex-wrap gap-2 ml-auto">
                <button 
                  @click="handleSearch" 
                  class="btn btn-primary gap-2"
                  :disabled="isSearching"
                >
                  <MagnifyingGlassIcon class="h-5 w-5" />
                  <span>{{ isSearching ? 'Searching...' : 'Search Now' }}</span>
                  <span v-if="isSearching" class="loading loading-spinner loading-sm"></span>
                </button>

                <button 
                  @click="handleClearAllFilters" 
                  class="btn btn-outline btn-error gap-2"
                  :disabled="activeFiltersCount === 0 || isSearching"
                >
                  <ArrowPathIcon class="h-5 w-5" />
                  <span>Reset All</span>
                </button>

                <!-- Info Dropdown -->
                <div class="dropdown dropdown-end">
                  <label tabindex="0" class="btn btn-ghost btn-circle">
                    <InformationCircleIcon class="h-6 w-6" />
                  </label>
                  <div tabindex="0" class="dropdown-content z-[1] card compact w-80 shadow-2xl bg-base-100 border border-base-300 mt-2">
                    <div class="card-body">
                      <h3 class="font-bold flex items-center gap-2 text-sm mb-3">
                        <InformationCircleIcon class="h-5 w-5 text-info" />
                        Quick Guide
                      </h3>
                      <div class="space-y-2 text-sm">
                        <div class="flex gap-2">
                          <div class="badge badge-sm badge-primary shrink-0">1</div>
                          <span>Enter query (SMILES, InChI, formula, DOI)</span>
                        </div>
                        <div class="flex gap-2">
                          <div class="badge badge-sm badge-primary shrink-0">2</div>
                          <span>Adjust histogram sliders to set ranges</span>
                        </div>
                        <div class="flex gap-2">
                          <div class="badge badge-sm badge-primary shrink-0">3</div>
                          <span>Combine filters across categories</span>
                        </div>
                        <div class="flex gap-2">
                          <div class="badge badge-sm badge-primary shrink-0">4</div>
                          <span>Click "Search Now" to view results</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Active Badge -->
              <div v-if="activeFiltersCount > 0" class="hidden sm:block ml-auto">
                <div class="badge badge-primary badge-lg gap-2">
                  <BoltIcon class="h-4 w-4" />
                  <span class="font-semibold">{{ activeFiltersCount }} active</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs Navigation -->
      <div class="mb-6">
        <div role="tablist" class="tabs tabs-boxed bg-base-100 shadow-lg border border-base-300 p-1.5">
          <a role="tab" class="tab gap-2 relative" @click="activeTab = 'literature'">
            <DocumentTextIcon class="h-5 w-5" />
            <span class="hidden sm:inline font-medium">Literature</span>
            <span class="sm:hidden font-medium">Lit</span>
            <span v-if="getLiteratureFiltersCount > 0" 
                  class="absolute -top-1 -right-1 badge badge-xs badge-primary w-5 h-5 p-0">
              {{ getLiteratureFiltersCount }}
            </span>
          </a>
          
          <a 
            role="tab" 
            class="tab gap-2 relative"
            :class="{ 'tab-active': activeTab === 'molecular' }"
            @click="activeTab = 'molecular'"
          >
            <BeakerIcon class="h-5 w-5" />
            <span class="hidden sm:inline font-medium">Molecular</span>
            <span class="sm:hidden font-medium">Mol</span>
            <span v-if="getMolecularFiltersCount > 0" 
                  class="absolute -top-1 -right-1 badge badge-xs badge-primary w-5 h-5 p-0 flex items-center justify-center">
              {{ getMolecularFiltersCount }}
            </span>
          </a>
          
          <a 
            role="tab" 
            class="tab gap-2 relative"
            :class="{ 'tab-active': activeTab === 'druglike' }"
            @click="activeTab = 'druglike'"
          >
            <CubeIcon class="h-5 w-5" />
            <span class="hidden sm:inline font-medium">Drug-Like</span>
            <span class="sm:hidden font-medium">Drug</span>
            <span v-if="getDrugLikenessFiltersCount > 0" 
                  class="absolute -top-1 -right-1 badge badge-xs badge-primary w-5 h-5 p-0 flex items-center justify-center">
              {{ getDrugLikenessFiltersCount }}
            </span>
          </a>
          
          <a role="tab" class="tab gap-2 relative" @click="activeTab = 'pharmaco'">
            <ChartBarIcon class="h-5 w-5" />
            <span class="hidden sm:inline font-medium">Pharmacokinetics</span>
            <span class="sm:hidden font-medium">PK</span>
            <span v-if="getPharmacokineticsFiltersCount > 0" 
                  class="absolute -top-1 -right-1 badge badge-xs badge-primary w-5 h-5 p-0">
              {{ getPharmacokineticsFiltersCount }}
            </span>
          </a>
        </div>
      </div>

      <!-- Tab Content -->
      <div class="card bg-base-100 shadow-xl border border-base-300">
        <div class="card-body p-6 min-h-[500px]">
          <!-- Tab Header -->
          <div class="flex items-center gap-3 mb-6 pb-4 border-b border-base-300">
            <div class="w-1 h-8 bg-gradient-to-b from-primary to-secondary rounded-full"></div>
            <div>
              <h2 class="text-lg font-bold flex items-center gap-2">
                <DocumentTextIcon v-if="activeTab === 'literature'" class="h-5 w-5 text-primary" />
                <BeakerIcon v-if="activeTab === 'molecular'" class="h-5 w-5 text-primary" />
                <CubeIcon v-if="activeTab === 'druglike'" class="h-5 w-5 text-primary" />
                <ChartBarIcon v-if="activeTab === 'pharmaco'" class="h-5 w-5 text-primary" />
                
                <span v-if="activeTab === 'literature'">Literature Filters</span>
                <span v-if="activeTab === 'molecular'">Molecular Properties</span>
                <span v-if="activeTab === 'druglike'">Drug-Likeness Criteria</span>
                <span v-if="activeTab === 'pharmaco'">Pharmacokinetics Parameters</span>
              </h2>
              <p class="text-xs text-base-content/60">
                <span v-if="activeTab === 'literature'">Filter by publication metadata</span>
                <span v-if="activeTab === 'molecular'">Refine by physicochemical properties</span>
                <span v-if="activeTab === 'druglike'">Apply Lipinski and ADMET rules</span>
                <span v-if="activeTab === 'pharmaco'">Filter by ADME parameters</span>
              </p>
            </div>
          </div>

          <!-- Tab Content Panels -->
          <div v-show="activeTab === 'literature'">
            <div class="max-w-4xl mx-auto">
              <LiteratureFilters />
            </div>
          </div>

          <div v-show="activeTab === 'molecular'">
            <MolecularPropertiesFilters />
          </div>

          <div v-show="activeTab === 'druglike'">
            <DrugLikenessFilters />
          </div>

          <div v-show="activeTab === 'pharmaco'">
            <PharmacokineticsFilters />
          </div>
        </div>
      </div>

      <!-- Bottom Info Cards - Compact -->
      <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-3">
        <!-- Query Types -->
        <div class="alert shadow-lg">
          <BeakerIcon class="h-6 w-6 text-primary shrink-0" />
          <div>
            <h4 class="font-semibold text-sm">Query Types</h4>
            <div class="text-xs text-base-content/70 mt-1 space-y-0.5">
              <div><strong>SMILES:</strong> <code class="badge badge-xs">C1=CC=CC=C1</code></div>
              <div><strong>InChI:</strong> <code class="badge badge-xs">InChI=1S/...</code></div>
              <div><strong>Formula:</strong> <code class="badge badge-xs">C6H6</code></div>
            </div>
          </div>
        </div>

        <!-- Categories -->
        <div class="alert shadow-lg">
          <FunnelIcon class="h-6 w-6 text-secondary shrink-0" />
          <div>
            <h4 class="font-semibold text-sm">Filter Categories</h4>
            <div class="text-xs text-base-content/70 mt-1 space-y-0.5">
              <div><strong>Molecular:</strong> MW, TPSA, bonds</div>
              <div><strong>Drug-Like:</strong> Lipinski, PAINS</div>
              <div><strong>Literature:</strong> DOI, dates</div>
            </div>
          </div>
        </div>

        <!-- Tips -->
        <div class="alert shadow-lg">
          <LightBulbIcon class="h-6 w-6 text-warning shrink-0" />
          <div>
            <h4 class="font-semibold text-sm">Pro Tips</h4>
            <div class="text-xs text-base-content/70 mt-1 space-y-0.5">
              <div>• Drag histogram sliders for ranges</div>
              <div>• Combine multiple categories</div>
              <div>• Monitor active filter count</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sticky Action Bar - Mobile Only -->
    <div class="fixed bottom-0 left-0 right-0 z-50 sm:hidden bg-base-100 border-t border-base-300 shadow-2xl">
      <div class="container mx-auto px-4 py-3">
        <div class="flex items-center gap-2">
          <!-- Active Filters Badge -->
          <div v-if="activeFiltersCount > 0" class="badge badge-primary badge-sm gap-1 shrink-0">
            <BoltIcon class="h-3 w-3" />
            {{ activeFiltersCount }}
          </div>

          <!-- Search Button -->
          <button 
            @click="handleSearch" 
            class="btn btn-primary btn-sm gap-2 flex-1"
            :disabled="isSearching"
          >
            <MagnifyingGlassIcon class="h-4 w-4" />
            <span>{{ isSearching ? 'Searching...' : 'Search' }}</span>
            <span v-if="isSearching" class="loading loading-spinner loading-xs"></span>
          </button>

          <!-- Reset Button -->
          <button 
            @click="handleClearAllFilters" 
            class="btn btn-outline btn-error btn-sm gap-1"
            :disabled="activeFiltersCount === 0 || isSearching"
          >
            <ArrowPathIcon class="h-4 w-4" />
            <span>Reset</span>
          </button>

          <!-- Info Dropdown -->
          <div class="dropdown dropdown-top dropdown-end">
            <label tabindex="0" class="btn btn-ghost btn-sm btn-circle">
              <InformationCircleIcon class="h-5 w-5" />
            </label>
            <div tabindex="0" class="dropdown-content z-[1] card compact w-80 shadow-2xl bg-base-100 border border-base-300 mb-2">
              <div class="card-body">
                <h3 class="font-bold flex items-center gap-2 text-sm mb-3">
                  <InformationCircleIcon class="h-5 w-5 text-info" />
                  Quick Guide
                </h3>
                <div class="space-y-2 text-sm">
                  <div class="flex gap-2">
                    <div class="badge badge-sm badge-primary shrink-0">1</div>
                    <span>Enter query (SMILES, InChI, formula, DOI)</span>
                  </div>
                  <div class="flex gap-2">
                    <div class="badge badge-sm badge-primary shrink-0">2</div>
                    <span>Adjust histogram sliders to set ranges</span>
                  </div>
                  <div class="flex gap-2">
                    <div class="badge badge-sm badge-primary shrink-0">3</div>
                    <span>Combine filters across categories</span>
                  </div>
                  <div class="flex gap-2">
                    <div class="badge badge-sm badge-primary shrink-0">4</div>
                    <span>Click "Search Now" to view results</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
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
  BeakerIcon,
  CubeIcon,
  ChartBarIcon,
  DocumentTextIcon,
  InformationCircleIcon,
  FunnelIcon,
  LightBulbIcon,
  ShieldCheckIcon,
  Squares2X2Icon,
  CheckCircleIcon,
  BoltIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const filterStore = useFilterStore()
const fetchChemicalStore = useFetchChemicalStore()
const histogramRangeSliderStore = useHistogramRangeSliderStore()
const chemicalPropertiesListStore = useChemicalPropertiesListStore()
const sortStore = useSortStore()

const isSearching = ref(false)
const activeTab = ref('literature')

const formatNumber = (num: number) => {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toString()
}

const activeFiltersCount = computed(() => {
  let count = 0
  
  Object.entries(filterStore.filters.exact).forEach(([key, value]) => {
    if (value && value != '') count++
  })
  
  Object.entries(filterStore.filters.range).forEach(([key, range]) => {
    if (range.gte != null || range.lte != null) count++
  })
  
  return count
})

const availableCategoriesCount = computed(() => 4)

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

const getLiteratureFiltersCount = computed(() => {
  let count = 0
  
  if (filterStore.filters.exact.doi) count++
  if (filterStore.filters.exact.title) count++
  if (filterStore.filters.range.publication_date?.after || 
      filterStore.filters.range.publication_date?.before) count++
  
  return count
})

const getPharmacokineticsFiltersCount = computed(() => {
  let count = 0
  const pharmaProps = [
    'gastrointestinal_absorption',
    'blood_brain_barrier_permeation',
    'cyp1a2_inhibitor',
    'cyp2c9_inhibitor',
    'cyp2c19_inhibitor',
    'cyp2d6_inhibitor',
    'cyp3a4_inhibitor'
  ]
  
  pharmaProps.forEach(prop => {
    if (filterStore.filters.exact[prop] === true) count++
  })
  
  return count
})

const handleSearch = async () => {
  isSearching.value = true
  
  try {
    fetchChemicalStore.setType('search')
    fetchChemicalStore.setMode('summary')
    await fetchChemicalStore.fetchChemicals()
    await chemicalPropertiesListStore.fetchAllChemicalProperties()
    
    router.push('/chemicals/search')
  } catch (error) {
    console.error('Search error:', error)
  } finally {
    isSearching.value = false
  }
}

const handleClearAllFilters = async () => {
  histogramRangeSliderStore.$reset()
  filterStore.$reset()
  sortStore.$reset()
  
  await fetchChemicalStore.fetchChemicals()
  await chemicalPropertiesListStore.fetchAllChemicalProperties()
  
  reloadHistogramTrigger.value++
}

const reloadHistogramTrigger = ref(0)
provide('reloadHistogramTrigger', reloadHistogramTrigger)
</script>
