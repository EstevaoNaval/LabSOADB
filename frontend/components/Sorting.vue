<template>
  <div class="hidden lg:flex">
    <button class="flex btn btn-ghost m-auto hover:text-primary" @click="sortStore.toggleSortDirection">
      <svg xmlns="http://www.w3.org/2000/svg" v-if="sortStore.ascDirection" stroke-width="2" fill="currentColor" class="bi bi-sort-up size-8" viewBox="0 0 16 16">
        <path d="M3.5 12.5a.5.5 0 0 1-1 0V3.707L1.354 4.854a.5.5 0 1 1-.708-.708l2-1.999.007-.007a.5.5 0 0 1 .7.006l2 2a.5.5 0 1 1-.707.708L3.5 3.707zm3.5-9a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
      </svg>
      
      <svg xmlns="http://www.w3.org/2000/svg" v-else stroke-width="2" fill="currentColor" class="bi bi-sort-down size-8" viewBox="0 0 16 16">
        <path d="M3.5 2.5a.5.5 0 0 0-1 0v8.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L3.5 11.293zm3.5 1a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
      </svg>
      
      <h1 class="text-xl">
        Sort by
      </h1>
    </button>
    
    <div class="dropdown dropdown-bottom dropdown-end m-auto">
      <div tabindex="0" role="button" class="btn btn-ghost btn-primary text-xl text-primary font-semibold">{{ sortStore.sortOptions[sortStore.currSortOptionId].name }}</div>
      <ul tabindex="0" class="dropdown-content text-lg font-semibold menu bg-base-200 rounded-box z-[1] p-2 shadow w-52 lg:w-64">
        <li @click="sortStore.setCurrSortOptionId(option.id)" class="hover:text-primary" v-for="option in sortStore.sortOptions" :key="option.id"><a>{{ option.name }}</a></li>
      </ul>
    </div>
  </div>
  <div class="flex lg:hidden">
    <button class="btn btn-sm md:btn-md btn-ghost flex m-auto hover:text-primary" @click="sortStore.toggleSortDirection">
      <svg xmlns="http://www.w3.org/2000/svg" v-if="sortStore.ascDirection" stroke-width="2" fill="currentColor" class="bi bi-sort-up size-6 md:size-8" viewBox="0 0 16 16">
        <path d="M3.5 12.5a.5.5 0 0 1-1 0V3.707L1.354 4.854a.5.5 0 1 1-.708-.708l2-1.999.007-.007a.5.5 0 0 1 .7.006l2 2a.5.5 0 1 1-.707.708L3.5 3.707zm3.5-9a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
      </svg>
      
      <svg xmlns="http://www.w3.org/2000/svg" v-else stroke-width="2" fill="currentColor" class="bi bi-sort-down size-6 md:size-8" viewBox="0 0 16 16">
        <path d="M3.5 2.5a.5.5 0 0 0-1 0v8.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L3.5 11.293zm3.5 1a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
      </svg>
    </button>
    
    <details class="dropdown dropdown-end m-auto" ref="sortOptionDropdownDetails">
      <summary class="text-md font-semibold text-center swap swap-rotate hover:text-primary focus:text-primary" @click="toggleSortOptionDropdown">
        <input type="checkbox" v-model="sortOptionsDropdownCheckBox" />

        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="swap-on size-6 md:size-8">
          <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
        </svg>
        
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="swap-off size-6 md:size-8">
          <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5" />
        </svg>
      </summary>
      <ul class="menu dropdown-content md:text-lg bg-base-200 rounded-box z-[1] p-2 shadow w-44">
        <li @click="handleSortOptionChoice(option.id)" class="hover:text-primary" v-for="option in sortStore.sortOptions" :key="option.id"><a>{{ option.name }}</a></li>
      </ul>
    </details>
  </div>
</template>

<script setup>
  import { useSortStore } from '~/stores/sortingStore';
  
  //stores
  const sortStore = useSortStore()

  const sortOptionDropdownDetails = ref(null)
  const sortOptionsDropdownCheckBox = ref(null)

  const handleSortOptionChoice = (optionId) => {
    closeSortOptionDropdown();
    sortStore.setCurrSortOptionId(optionId);
  }

  const toggleSortOptionDropdown = () => {
    sortOptionsDropdownCheckBox.value = !sortOptionsDropdownCheckBox.value
  }

  const closeSortOptionDropdown = () => {
    sortOptionsDropdownCheckBox.value = false
    sortOptionDropdownDetails.value.removeAttribute("open")
  }
</script>
<style scoped>
details > summary {
  list-style: none;
}
details > summary::-webkit-details-marker {
  display: none;
}
</style>