<template>
    <main>
        <div class="join">
            <div class="w-full relative">
                <input class="input input-bordered join-item pr-12 text-md md:text-lg w-full" type="text" placeholder="Search Chemical" v-model="querySearchByRepr" @keydown.enter="handleSearchByRepresentation" required>
                <button type="submit" class="absolute inset-y-0 right-0 flex items-center px-2 btn btn-ghost m-auto mr-2" @click="clearInput">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 md:size-8">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                  </svg>
                </button>
            </div>
            
            <div class="indicator">
              <button type="submit" class="btn btn-primary join-item" @click="handleSearchByRepresentation">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="size-6 m-auto">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                </svg>
              </button>
            </div>
        </div>
    </main>
</template>

<script setup>
    import { useRouter } from 'vue-router'
    import { useFilterStore } from '~/stores/filterStore'
    import { useFetchChemicalStore } from '~/stores/fetchChemicalStore'
    import { useHistogramRangeSliderStore } from '~/stores/histogramRangeSliderStore';
    import { useSortStore } from '~/stores/sortingStore';

    const filterStore = useFilterStore() 
    const fetchChemicalStore = useFetchChemicalStore()
    const histogramRangeSliderStore = useHistogramRangeSliderStore()
    const sortStore = useSortStore()

    const router = useRouter()
  
    const querySearchByRepr = ref('')

    function clearInput() {
      querySearchByRepr.value = '';
    }

    const handleSearchByRepresentation = () => {
        if (querySearchByRepr.value !== '') {
            histogramRangeSliderStore.$reset()
            
            filterStore.$reset()
            fetchChemicalStore.$reset()
            sortStore.$reset()

            filterStore.setExactFilter('query', querySearchByRepr.value)
            
            fetchChemicalStore.setType('search')
            fetchChemicalStore.setMode('summary')
            fetchChemicalStore.fetchChemicals()
            
            router.push('/chemicals/search')
        }
    }
</script>

<style>

</style>