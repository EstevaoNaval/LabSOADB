<template>
  <main>
    <!-- Desktop View -->
    <div class="hidden lg:flex items-center gap-3">
      <!-- Sort Direction Toggle -->
      <button 
        @click="sortStore.toggleSortDirection"
        class="btn btn-outline btn-primary gap-2"
        :aria-label="sortStore.ascDirection ? 'Sort ascending' : 'Sort descending'"
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          v-if="sortStore.ascDirection" 
          fill="currentColor" 
          class="w-5 h-5" 
          viewBox="0 0 16 16"
        >
          <path d="M3.5 12.5a.5.5 0 0 1-1 0V3.707L1.354 4.854a.5.5 0 1 1-.708-.708l2-1.999.007-.007a.5.5 0 0 1 .7.006l2 2a.5.5 0 1 1-.707.708L3.5 3.707zm3.5-9a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
        </svg>
        
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          v-else 
          fill="currentColor" 
          class="w-5 h-5" 
          viewBox="0 0 16 16"
        >
          <path d="M3.5 2.5a.5.5 0 0 0-1 0v8.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L3.5 11.293zm3.5 1a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
        </svg>
        
        <span class="hidden xl:inline">
          {{ sortStore.ascDirection ? 'Ascending' : 'Descending' }}
        </span>
      </button>
      
      <!-- Sort Options Dropdown -->
      <div class="dropdown dropdown-bottom dropdown-end">
        <div 
          tabindex="0" 
          role="button" 
          class="btn btn-outline btn-primary gap-2"
          aria-label="Select sort option"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 7.5 7.5 3m0 0L12 7.5M7.5 3v13.5m13.5 0L16.5 21m0 0L12 16.5m4.5 4.5V7.5" />
          </svg>
          <span class="font-medium">{{ sortStore.sortOptions[sortStore.currSortOptionId].name }}</span>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
          </svg>
        </div>

        <ul 
          tabindex="0" 
          class="dropdown-content menu bg-base-100 rounded-box z-10 mt-2 p-2 shadow-xl border border-base-300 w-56"
        >
          <!-- Header -->
          <div class="px-3 py-2 border-b border-base-300 mb-1">
            <p class="font-semibold text-sm">Sort By</p>
          </div>

          <!-- Sort Options -->
          <li 
            v-for="option in sortStore.sortOptions" 
            :key="option.id"
            @click="sortStore.setCurrSortOptionId(option.id)"
          >
            <button 
              class="flex items-center justify-between"
              :class="{ 'bg-primary/10 text-primary': sortStore.currSortOptionId === option.id }"
            >
              <span class="font-medium">{{ option.name }}</span>
              <svg 
                v-if="sortStore.currSortOptionId === option.id"
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke-width="2" 
                stroke="currentColor" 
                class="w-4 h-4"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
              </svg>
            </button>
          </li>
        </ul>
      </div>
    </div>

    <!-- Mobile/Tablet View -->
    <div class="flex lg:hidden items-center">
      <div class="dropdown dropdown-bottom dropdown-start">
        <div 
          ref="sortButton"
          tabindex="0" 
          role="button" 
          class="btn btn-sm md:btn-md btn-outline btn-primary gap-2"
          aria-label="Sort options"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 md:w-5 md:h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 7.5 7.5 3m0 0L12 7.5M7.5 3v13.5m13.5 0L16.5 21m0 0L12 16.5m4.5 4.5V7.5" />
          </svg>
          <span class="hidden md:inline font-medium text-xs md:text-sm truncate">
            {{ sortStore.sortOptions[sortStore.currSortOptionId].name }}
          </span>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 flex-shrink-0">
            <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
          </svg>
        </div>

        <ul 
          tabindex="0" 
          class="dropdown-content menu bg-base-100 rounded-box z-10 mt-2 p-2 shadow-xl border border-base-300 w-52"
        >
          <!-- Sort Direction Toggle -->
          <li @click="handleToggleDirection">
            <button 
              class="flex items-center gap-2"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                v-if="sortStore.ascDirection" 
                fill="currentColor" 
                class="w-5 h-5" 
                viewBox="0 0 16 16"
              >
                <path d="M3.5 12.5a.5.5 0 0 1-1 0V3.707L1.354 4.854a.5.5 0 1 1-.708-.708l2-1.999.007-.007a.5.5 0 0 1 .7.006l2 2a.5.5 0 1 1-.707.708L3.5 3.707zm3.5-9a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
              </svg>
              
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                v-else 
                fill="currentColor" 
                class="w-5 h-5" 
                viewBox="0 0 16 16"
              >
                <path d="M3.5 2.5a.5.5 0 0 0-1 0v8.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L3.5 11.293zm3.5 1a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
              </svg>
              
              {{ sortStore.ascDirection ? 'Ascending' : 'Descending' }}
            </button>
          </li>

          <div class="divider my-1"></div>

          <!-- Header -->
          <div class="px-3 py-2 border-b border-base-300 mb-1">
            <p class="font-semibold text-sm">Sort By</p>
          </div>

          <!-- Sort Options -->
          <li 
            v-for="option in sortStore.sortOptions" 
            :key="option.id"
            @click="handleSortOptionChoice(option.id)"
          >
            <button 
              class="flex items-center justify-between text-sm md:text-base"
              :class="{ 'bg-primary/10 text-primary': sortStore.currSortOptionId === option.id }"
            >
              <span class="font-medium">{{ option.name }}</span>
              <svg 
                v-if="sortStore.currSortOptionId === option.id"
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke-width="2" 
                stroke="currentColor" 
                class="w-4 h-4"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
              </svg>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useSortStore } from '~/stores/sortingStore'

// Stores
const sortStore = useSortStore()

// Refs
const sortButton = ref(null)

// Functions
const handleToggleDirection = () => {
  sortStore.toggleSortDirection()
  if (sortButton.value) {
    sortButton.value.blur()
  }
}

const handleSortOptionChoice = (optionId) => {
  sortStore.setCurrSortOptionId(optionId)
  if (sortButton.value) {
    sortButton.value.blur()
  }
}
</script>