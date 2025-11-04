<!-- components/advanced-search/LiteratureFilters.vue -->
<template>
  <div class="card bg-base-100 shadow-lg border border-base-300">
    <div class="card-body p-4">
      <h3 class="card-title text-base mb-4 flex items-center gap-2">
        <DocumentTextIcon class="h-5 w-5" />
        Literature Filters
      </h3>
      
      <div class="space-y-4">
        <!-- DOI -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">DOI</span>
          </label>
          <input
            v-model="filterStore.filters.exact.doi"
            type="text"
            placeholder="10.1000/example"
            class="input input-bordered input-sm w-full"
          />
        </div>

        <!-- Title -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">Title</span>
          </label>
          <input
            v-model="filterStore.filters.exact.title"
            type="text"
            placeholder="Article title"
            class="input input-bordered input-sm w-full"
          />
        </div>

        <!-- Publication Date Range -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">Publication Date</span>
          </label>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="label py-1">
                <span class="label-text text-xs">From</span>
              </label>
              <input
                v-model="filterStore.filters.range.publication_date.after"
                type="date"
                class="input input-bordered input-sm w-full"
              />
            </div>
            <div>
              <label class="label py-1">
                <span class="label-text text-xs">To</span>
              </label>
              <input
                v-model="filterStore.filters.range.publication_date.before"
                type="date"
                class="input input-bordered input-sm w-full"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useFilterStore } from '~/stores/filterStore'
import { DocumentTextIcon } from '@heroicons/vue/24/outline'

const filterStore = useFilterStore()
</script>
