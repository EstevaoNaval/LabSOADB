<template>
  <div class="hidden md:flex md:flex-col gap-4">
    <div role="tablist" class="tabs tabs-bordered mx-auto tabs-lg w-full">
      <input type="radio" name="my_tabs_1" role="tab" class="tab tabs-bordered" aria-label="Chemical" checked="checked" />
      <div role="tabpanel" class="border-t-2 border-t-gray-100 border-opacity-30 tab-content p-10">
        <div class="join w-full">
          <div class="relative w-full">
            <input class="input input-bordered join-item text-2xl w-full py-8 pr-10" v-model="querySearchByRepr" @keydown.enter="handleSearchByRepresentation" data-typewriter="LSOA5108276818...;N-(2-Aminoethyl)-D-gluconamide...;C1=CC=C(C=C1)C=O...;[X3&H0]...;C25H20O4...;InChI=1S/C3H6O/c1-3(2)4/h1-2H3..." type="text" required>
            <button type="submit" class="absolute inset-y-0 right-0 flex items-center px-2 btn btn-ghost  m-auto mr-2" @click="clearInput">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-10">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div class="indicator">
            <button type="submit" class="btn btn-primary h-full join-item" @click="handleSearchByRepresentation">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="size-10">
                <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      <input type="radio" name="my_tabs_1" role="tab" class="tab tabs-bordered" aria-label="Citation" />
      <div role="tabpanel" class="border-t-2 border-t-gray-100 border-opacity-30 tab-content p-10">
          <div class="join w-full">
            <div class="relative w-full">
              <input class="input input-bordered join-item text-2xl w-full py-8 pr-10" v-model="querySearchByCitation" @keydown.enter="handleSearchByCitation" data-typewriter="Search DOI or Title...;10.1016/j.bioorg.2020.103984..." type="text" required>
              <button type="submit" class="absolute inset-y-0 right-0 flex items-center px-2 btn btn-ghost m-auto mr-2" @click="clearInput">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-10">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div class="indicator">
              <button type="submit" class="btn btn-primary h-full join-item" @click="handleSearchByCitation">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="h-10 w-10">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                </svg>
              </button>
            </div>
          </div>
      </div>
    </div>
  </div>

  <div class="flex flex-col md:hidden gap-2">
    <select v-model="searchFieldSelected" class="select select-bordered text-lg w-full">
      <option v-for="option in searchFieldOptions" :key="option.id" :value="option.value">{{ option.text }}</option>
    </select>
    <div class="join w-full" v-if="searchFieldSelected === searchFieldOptions[0]['value']">
      <div class="relative w-full">
        <input class="input input-bordered join-item text-lg w-full pr-10" type="text" placeholder="Search Chemical" required v-model="querySearchByRepr" @keydown.enter="handleSearchByRepresentation">
        <button type="submit" class="absolute inset-y-0 right-0 flex items-center px-2 m-auto btn btn-ghost" @click="clearInput">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="indicator">
        <button type="submit" class="btn btn-primary join-item" @click="handleSearchByRepresentation">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="h-7 w-7">
            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>
        </button>
      </div>
    </div>
    <div class="join w-full" v-if="searchFieldSelected === searchFieldOptions[1]['value']">
      <div class="relative w-full">
        <input class="input input-bordered join-item text-lg w-full pr-10" type="text" v-model="querySearchByCitation" @keydown.enter="handleSearchByCitation" placeholder="Search DOI or Title" required>
        <button type="submit" class="absolute inset-y-0 right-0 flex items-center px-2 m-auto btn btn-ghost" @click="clearInput">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="indicator">
        <button type="submit" class="btn btn-primary join-item" @click="handleSearchByCitation">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="h-7 w-7">
            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { useRouter } from 'vue-router'
  import { usePaginationStore } from '~/stores/paginationStore';
  import { useFilterStore } from '~/stores/filterStore'
  import { useFetchChemicalStore } from '~/stores/fetchChemicalStore'
  import { useHistogramRangeSliderStore } from '~/stores/histogramRangeSliderStore';
  
  const filterStore = useFilterStore() 
  const fetchChemicalStore = useFetchChemicalStore()
  const paginationStore = usePaginationStore()
  const histogramRangeSliderStore = useHistogramRangeSliderStore()

  const router = useRouter()
  
  const querySearchByRepr = ref('')
  const querySearchByCitation = ref('')

  function clearInput() {
    querySearchByRepr.value = '';
    querySearchByCitation.value = '';
  }

  const handleSearchByRepresentation = () => {
    if (querySearchByRepr.value !== '') {
      paginationStore.setPage(1)

      histogramRangeSliderStore.resetProperties()

      filterStore.clearFilter()
      filterStore.setExactFilter('query', querySearchByRepr.value)

      fetchChemicalStore.setType('search')
      fetchChemicalStore.setMode('summary')
      fetchChemicalStore.fetchChemicals()

      router.push({
        path: '/chemicals/search'
      })
    }
  }

  const handleSearchByCitation = () => {
    if (querySearchByCitation.value !== '') {
      paginationStore.setPage(1)

      histogramRangeSliderStore.resetProperties()

      filterStore.clearFilter()
      filterStore.setExactFilter('citation', querySearchByCitation.value)

      fetchChemicalStore.setType('search')
      fetchChemicalStore.setMode('summary')
      fetchChemicalStore.fetchChemicals()

      router.push({
        path: '/chemicals/search'
      })
    }
  }
  
  const searchFieldOptions = ref([
    {
      id: 0, 
      value: "chemicalsSearchFieldOption", 
      text: "Chemical" 
    },
    { 
      id: 1, 
      value: "citationSearchFieldOption", 
      text: "Citation" 
    },
  ])
  
  const searchFieldSelected = defineModel("searchFieldSelected")
  // Select the first search field option
  searchFieldSelected.value = searchFieldOptions.value[0]['value']
  
  
  defineProps({
    typewriterEffect: Boolean
  })
  
  class Typerwriter {
    constructor(el, options){
      this.el = el;
      this.words = [...this.el.dataset.typewriter.split(';')];
      this.speed = options?.speed || 100;
      this.delay = options?.delay || 1500;
      this.repeat = options?.repeat;
      this.initTyping();
    }
  
    wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))
  
    toggleTyping = () => this.el.classList.toggle('typing');
  
    async typewrite(word){
      await this.wait(this.delay);
      this.toggleTyping();
      let result = '|';
      for (const letter of word.split('')) {
        result = result.slice(0, result.length - 1) + letter + result.slice(result.length - 1, result.length);
        this.el.placeholder = result
        await this.wait(this.speed)
      }
      this.toggleTyping();
      await this.wait(this.delay);
      this.toggleTyping();
      while (this.el.placeholder.length !== 0){
        this.el.placeholder = this.el.placeholder.slice(0, -1);
        await this.wait(this.speed)
      }
      this.toggleTyping();
    }
    async initTyping() {
      for (const word of this.words){
        await this.typewrite(word);
      }
      if(this.repeat){
        await this.initTyping();
      } else {
        this.el.style.animation = 'none';
      }
    }
  }
  
  onMounted(() => {
    document.querySelectorAll('[data-typewriter]').forEach(el => {
      new Typerwriter(el, {
        repeat: true,
        speed: 50,
        delay: 1000
      })
    })
  })
</script>
<style scoped>
input {
  padding-right: 2.5rem; /* Adjust based on the icon size */
}
</style>