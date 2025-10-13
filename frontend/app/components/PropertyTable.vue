<!-- components/PropertyTable.vue -->
<template>
  <section :id="id" class="card bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title text-2xl mb-4">
        <slot name="icon"></slot>
        {{ title }}
      </h2>
      <div class="overflow-x-auto">
        <table class="table table-zebra">
          <thead>
            <tr>
              <th v-for="(header, idx) in headers" :key="idx" class="font-semibold">
                {{ header }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="(row, idx) in rows" 
              :key="idx" 
              class="hover"
            >
              <td 
                v-for="(cell, cellIdx) in row" 
                :key="cellIdx" 
                v-html="cell"
                class="whitespace-normal"
              ></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  id: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  headers: {
    type: Array,
    required: true
  },
  rows: {
    type: Array,
    required: true
  }
})
</script>