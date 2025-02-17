<template>
  <div class="mx-auto join md:hidden">
    <button class="join-item btn" v-if="paginationStore.page > 1" @click="paginationStore.setPage(1)">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-4">
        <path stroke-linecap="round" stroke-linejoin="round" d="m18.75 4.5-7.5 7.5 7.5 7.5m-6-15L5.25 12l7.5 7.5" />
      </svg>
    </button>
    <button class="join-item btn" v-if="paginationStore.page > 1" @click="paginationStore.prevPage()">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-4">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
      </svg>
    </button>
    <button class="join-item btn">
      {{ paginationStore.page }}
    </button>
    <button class="join-item btn" v-if="paginationStore.page < paginationStore.totalPages" @click="paginationStore.nextPage()">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-4">
        <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
      </svg>
    </button>
    <button class="join-item btn" v-if="paginationStore.page < paginationStore.totalPages" @click="paginationStore.setPage(paginationStore.totalPages)">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-4">
        <path stroke-linecap="round" stroke-linejoin="round" d="m5.25 4.5 7.5 7.5-7.5 7.5m6-15 7.5 7.5-7.5 7.5" />
      </svg>
    </button>
  </div>

  <div class="hidden md:join">
    <!-- Botão de página anterior -->
    <button class="join-item btn" v-if="paginationStore.page > 1" @click="paginationStore.prevPage()">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
      </svg>
    </button>
    
    <!-- Primeiras páginas -->
    <button 
      v-for="page in pagesToShow.start" 
      :key="page" 
      @click="paginationStore.setPage(page)" 
      :class="['join-item btn', { 'btn-active': page === paginationStore.page }]"
    >
      {{ page }}
    </button>
    
    <!-- Elipses para páginas intermediárias -->
    <button v-if="pagesToShow.startEllipsis" class="join-item btn btn-disabled">
      <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-three-dots size-5" viewBox="0 0 16 16">
        <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3"/>
      </svg>
    </button>
    
    <!-- Páginas ao redor da página atual -->
    <button 
      v-for="page in pagesToShow.middle" 
      :key="page" 
      @click="paginationStore.setPage(page)" 
      :class="['join-item btn', { 'btn-active': page === paginationStore.page }]"
    >
      {{ page }}
    </button>
    
    <!-- Elipses para as últimas páginas -->
    <button v-if="pagesToShow.endEllipsis" class="join-item btn btn-disabled">
      <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-three-dots size-5" viewBox="0 0 16 16">
        <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3"/>
      </svg>
    </button>
    
    <!-- Últimas páginas -->
    <button 
      v-for="page in pagesToShow.end" 
      :key="page" 
      @click="paginationStore.setPage(page)" 
      :class="['join-item btn', { 'btn-active': page === paginationStore.page }]"
    >
      {{ page }}
    </button>
    
    <!-- Botão de próxima página -->
    <button class="join-item btn" v-if="paginationStore.page < paginationStore.totalPages" @click="paginationStore.nextPage()">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
        <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
      </svg>
    </button>
  </div>
</template>
  
<script setup>
import { usePaginationStore } from '~/stores/paginationStore'

const paginationStore = usePaginationStore()

// Função que calcula quais páginas serão exibidas
const pagesToShow = computed(() => {
  const pages = {
    start: [],
    middle: [],
    end: [],
    startEllipsis: false,
    endEllipsis: false,
  };

  const startPages = 1;
  const endPages = 1;
  const surroundingPages = 2; 

  pages.start = Array.from({ length: Math.min(startPages, paginationStore.totalPages) }, (_, i) => i + 1);
  pages.end = Array.from({ length: endPages }, (_, i) => paginationStore.totalPages - endPages + i + 1).filter(page => page > startPages);

  const startMiddle = Math.max(paginationStore.page - surroundingPages, startPages + 1);
  const endMiddle = Math.min(paginationStore.page + surroundingPages, paginationStore.totalPages - endPages);

  pages.middle = Array.from({ length: endMiddle - startMiddle + 1 }, (_, i) => startMiddle + i);

  if (startMiddle > startPages + 1) pages.startEllipsis = true;
  if (endMiddle < paginationStore.totalPages - endPages) pages.endEllipsis = true;

  return pages;
});
</script>