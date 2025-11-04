<!-- components/advanced-search/PharmacokineticsFilters.vue -->
<template>
  <div class="space-y-4">
    <p class="text-sm text-base-content/70">
      Filter by ADME properties and cytochrome P450 inhibition
    </p>

    <!-- Gastrointestinal Absorption -->
    <div class="form-control">
      <label class="label cursor-pointer justify-start gap-3">
        <input
          v-model="gastrointestinalAbsorption"
          type="checkbox"
          class="checkbox checkbox-primary"
        />
        <div>
          <span class="label-text font-medium">Gastrointestinal Absorption</span>
          <p class="text-xs text-base-content/60">Compounds with high GI absorption</p>
        </div>
      </label>
    </div>

    <!-- Blood-Brain Barrier -->
    <div class="form-control">
      <label class="label cursor-pointer justify-start gap-3">
        <input
          v-model="bloodBrainBarrier"
          type="checkbox"
          class="checkbox checkbox-primary"
        />
        <div>
          <span class="label-text font-medium">BBB Permeation</span>
          <p class="text-xs text-base-content/60">Crosses blood-brain barrier</p>
        </div>
      </label>
    </div>

    <div class="divider my-2">CYP450 Inhibition</div>

    <!-- CYP1A2 -->
    <div class="form-control">
      <label class="label cursor-pointer justify-start gap-3">
        <input
          v-model="cyp1a2"
          type="checkbox"
          class="checkbox checkbox-sm"
        />
        <span class="label-text text-sm">CYP1A2 Inhibitor</span>
      </label>
    </div>

    <!-- CYP2C9 -->
    <div class="form-control">
      <label class="label cursor-pointer justify-start gap-3">
        <input
          v-model="cyp2c9"
          type="checkbox"
          class="checkbox checkbox-sm"
        />
        <span class="label-text text-sm">CYP2C9 Inhibitor</span>
      </label>
    </div>

    <!-- CYP2C19 -->
    <div class="form-control">
      <label class="label cursor-pointer justify-start gap-3">
        <input
          v-model="cyp2c19"
          type="checkbox"
          class="checkbox checkbox-sm"
        />
        <span class="label-text text-sm">CYP2C19 Inhibitor</span>
      </label>
    </div>

    <!-- CYP2D6 -->
    <div class="form-control">
      <label class="label cursor-pointer justify-start gap-3">
        <input
          v-model="cyp2d6"
          type="checkbox"
          class="checkbox checkbox-sm"
        />
        <span class="label-text text-sm">CYP2D6 Inhibitor</span>
      </label>
    </div>

    <!-- CYP3A4 -->
    <div class="form-control">
      <label class="label cursor-pointer justify-start gap-3">
        <input
          v-model="cyp3a4"
          type="checkbox"
          class="checkbox checkbox-sm"
        />
        <span class="label-text text-sm">CYP3A4 Inhibitor</span>
      </label>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useFilterStore } from '~/stores/filterStore'

const filterStore = useFilterStore()

// Create a pharmacokinetics section in your filterStore if needed
// For now, using computed properties to sync with store

const gastrointestinalAbsorption = computed({
  get: () => filterStore.filters.exact.gastrointestinal_absorption || false,
  set: (val) => filterStore.setExactFilter('gastrointestinal_absorption', val)
})

const bloodBrainBarrier = computed({
  get: () => filterStore.filters.exact.blood_brain_barrier_permeation || false,
  set: (val) => filterStore.setExactFilter('blood_brain_barrier_permeation', val)
})

const cyp1a2 = computed({
  get: () => filterStore.filters.exact.cyp1a2_inhibitor || false,
  set: (val) => filterStore.setExactFilter('cyp1a2_inhibitor', val)
})

const cyp2c9 = computed({
  get: () => filterStore.filters.exact.cyp2c9_inhibitor || false,
  set: (val) => filterStore.setExactFilter('cyp2c9_inhibitor', val)
})

const cyp2c19 = computed({
  get: () => filterStore.filters.exact.cyp2c19_inhibitor || false,
  set: (val) => filterStore.setExactFilter('cyp2c19_inhibitor', val)
})

const cyp2d6 = computed({
  get: () => filterStore.filters.exact.cyp2d6_inhibitor || false,
  set: (val) => filterStore.setExactFilter('cyp2d6_inhibitor', val)
})

const cyp3a4 = computed({
  get: () => filterStore.filters.exact.cyp3a4_inhibitor || false,
  set: (val) => filterStore.setExactFilter('cyp3a4_inhibitor', val)
})
</script>
