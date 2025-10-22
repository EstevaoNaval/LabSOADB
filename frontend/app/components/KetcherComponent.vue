<template>
  <div class="flex flex-col gap-6 p-6 bg-base-100 rounded-xl">
    <!-- Header Section -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-base-content">Structure Editor</h2>
        <p class="text-sm text-base-content/70 mt-1">Draw or modify your chemical structure</p>
      </div>

      <!-- Quick Actions -->
      <div class="flex gap-2">
        <button @click="clearStructure" class="btn btn-ghost btn-sm gap-2" :disabled="isLoading">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
            class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          Clear
        </button>
      </div>
    </div>

    <!-- Ketcher Editor -->
    <div class="relative">
      <div class="rounded-xl overflow-hidden border-2 border-base-300 shadow-lg bg-white" style="height: 32rem;">
        <iframe class="w-full h-full" ref="ketcherIFrame" v-if="isInView" :src="ketcherSrc" allowfullscreen
          title="Chemical structure editor"></iframe>
      </div>

      <!-- Loading Overlay -->
      <div v-if="isLoading"
        class="absolute inset-0 bg-base-100/80 backdrop-blur-sm rounded-xl flex items-center justify-center">
        <div class="flex flex-col items-center gap-3">
          <span class="loading loading-spinner loading-lg text-primary"></span>
          <p class="text-sm font-medium">Processing structure...</p>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="alert alert-error shadow-lg">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>{{ errorMessage }}</span>
      <button @click="errorMessage = ''" class="btn btn-sm btn-ghost">Dismiss</button>
    </div>

    <!-- Search Controls -->
    <div class="card bg-base-200 shadow-sm">
      <div class="card-body p-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

          <!-- Left Column: Search Type & Similarity -->
          <div class="flex flex-col gap-4">
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Search Type</span>
                <span class="label-text-alt text-xs">Required</span>
              </label>
              <select v-model="searchSelected" class="select select-bordered w-full font-medium"
                :class="{ 'select-primary': searchSelected }" required>
                <option value="" disabled>Choose search method</option>
                <option v-for="option in searchOptions" :key="option.id" :value="option.value">
                  {{ option.text }}
                </option>
              </select>
              <label class="label">
                <span class="label-text-alt text-xs">
                  {{ getSearchTypeDescription() }}
                </span>
              </label>
            </div>

            <!-- Similarity Slider (conditional) -->
            <div v-if="searchSelected === 'similarity'" class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Tanimoto Similarity Threshold</span>
                <span class="label-text-alt font-bold text-primary text-lg">
                  {{ inputSimilarityPercent }}%
                </span>
              </label>
              <input v-model.number="inputSimilarityPercent" type="range" min="0" max="100" class="range range-primary"
                step="5" aria-label="Similarity percentage" />
              <div class="w-full flex justify-between text-xs px-2 mt-2 text-base-content/60">
                <span>0%</span>
                <span>25%</span>
                <span>50%</span>
                <span>75%</span>
                <span>100%</span>
              </div>
              <label class="label">
                <span class="label-text-alt text-xs">
                  Higher values return more similar structures
                </span>
              </label>
            </div>

            <!-- Match Tautomers (conditional) -->
            <div v-if="searchSelected && searchSelected !== 'similarity'" class="form-control">
              <label
                class="label cursor-pointer justify-start gap-3 p-4 bg-base-100 rounded-lg border border-base-300 hover:border-primary transition-colors">
                <input v-model="matchTautomers" type="checkbox" class="checkbox checkbox-primary" />
                <div class="flex flex-col">
                  <span class="label-text font-semibold">Match Tautomers</span>
                  <span class="label-text-alt text-xs">Include tautomeric forms in search</span>
                </div>
              </label>
            </div>
          </div>

          <!-- Right Column: Search Button & Info -->
          <div class="flex flex-col justify-center gap-4">
            <div class="stats shadow bg-base-100">
              <div class="stat px-6 py-4">
                <div class="stat-title text-xs">Selected Method</div>
                <div class="stat-value text-2xl text-primary">
                  {{searchSelected ? searchOptions.find(o => o.value === searchSelected)?.text : 'None'}}
                </div>
                <div class="stat-desc text-xs mt-1">
                  {{ searchSelected ? 'Ready to search' : 'Please select a search type' }}
                </div>
              </div>
            </div>

            <button @click="handleSearchByDrawnStructure"
              class="btn btn-primary btn-lg gap-3 shadow-lg hover:shadow-xl transition-shadow"
              :disabled="!searchSelected || isLoading">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5"
                stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
              </svg>
              <span class="text-lg">Search Structures</span>
            </button>

            <div class="text-xs text-center text-base-content/60">
              Press Search to find matching chemical structures
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useFilterStore } from '~/stores/filterStore';
import { useFetchChemicalStore } from '~/stores/fetchChemicalStore';
import { useSortStore } from '~/stores/sortingStore';
import { useRouter } from 'vue-router';

const router = useRouter();
const closeModal = inject('closeModal');

// State
const inputSimilarityPercent = ref(90);
const searchSelected = ref('exact');
const matchTautomers = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');

const searchOptions = ref([
  { id: 0, value: 'exact', text: 'Exact Match' },
  { id: 1, value: 'similarity', text: 'Similarity Search' },
  { id: 2, value: 'substructure', text: 'Substructure Search' }
]);

const isInView = ref(true);
const ketcherSrc = ref('/Ketcher/index.html');

const ketcherIFrame = ref(null);
let ketcherContentWindow = null;

onMounted(() => {
  ketcherContentWindow = ketcherIFrame.value.contentWindow;
});

// Helper function for search type descriptions
const getSearchTypeDescription = () => {
  const descriptions = {
    exact: 'Find structures that match exactly',
    similarity: 'Find structures with similar properties',
    substructure: 'Find structures containing this fragment'
  };
  return searchSelected.value ? descriptions[searchSelected.value] : 'Select a method above';
};

// Get SMILES from Ketcher
const getSmiles = () => {
  return ketcherContentWindow.ketcher
    .getSmiles()
    .then((smiles) => smiles)
    .catch((err) => {
      console.error(err);
      throw new Error('Failed to get structure from editor');
    });
};

// Clear structure in Ketcher
const clearStructure = () => {
  if (ketcherContentWindow?.ketcher) {
    ketcherContentWindow.ketcher.editor.clear();
  }
};

// Handle search
const handleSearchByDrawnStructure = async () => {
  if (!searchSelected.value) {
    errorMessage.value = 'Please select a search type';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    const smiles = await getSmiles();

    if (!smiles || smiles.trim() === '') {
      errorMessage.value = 'Please draw a chemical structure before searching';
      return;
    }

    const fetchChemicalStore = useFetchChemicalStore();
    const filterStore = useFilterStore();
    const sortStore = useSortStore();

    // Reset stores
    filterStore.$reset();
    fetchChemicalStore.$reset();
    sortStore.$reset();

    // Set similarity threshold if applicable
    if (searchSelected.value === 'similarity') {
      const similarity_threshold = inputSimilarityPercent.value * 0.01;
      filterStore.setExactFilter('similarity_threshold', similarity_threshold);
    }

    // Set filters
    filterStore.setExactFilter('query', smiles);
    filterStore.setExactFilter('representation_type', 'smiles');
    filterStore.setExactFilter('search_type', searchSelected.value);

    if (matchTautomers.value && searchSelected.value !== 'similarity') {
      filterStore.setExactFilter('match_tautomers', true);
    }

    // Fetch chemicals
    fetchChemicalStore.setMode('summary');
    fetchChemicalStore.setType('search');
    await fetchChemicalStore.fetchChemicals();

    closeModal();
    router.push('/chemicals/search');

  } catch (error) {
    console.error('Error searching:', error);
    errorMessage.value = error.message || 'An error occurred while searching. Please try again.';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Remove number input spinners */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
}
</style>