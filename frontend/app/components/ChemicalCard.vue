<template>
  <div class="card bg-base-100 shadow-xl hover:shadow-2xl transition-all duration-300">
    <!-- Image -->
    <figure class="bg-base-200 p-4">
      <img
        v-if="props.chemical.chem_depiction_image"
        :src="props.chemical.chem_depiction_image"
        :alt="`Molecular structure of ${props.chemical.identifier.iupac_name}`"
        class="w-full h-48 object-contain"
        loading="lazy"
      />
    </figure>

    <!-- Content -->
    <div class="card-body p-4">
      <!-- Title -->
      <h3 class="card-title text-base font-bold line-clamp-2 min-h-[3rem]" :title="props.chemical.identifier.iupac_name">
        {{ props.chemical.identifier.iupac_name }}
      </h3>
      
      <!-- ID Badge -->
      <div class="badge badge-primary badge-sm">
        {{ props.chemical.api_id }}
      </div>

      <!-- Properties Grid -->
      <div class="grid grid-cols-2 gap-3 mt-4">
        <!-- Molecular Weight -->
        <PropertyItem 
          v-if="props.chemical.physical_property.molecular_weight"
          label="MW"
          :value="`${props.chemical.physical_property.molecular_weight.toFixed(1)} g/mol`"
        >
          <template #icon>
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 485 485" xmlns="http://www.w3.org/2000/svg">
              <path d="M411.097,110H257.5V87.42c17.459-6.192,30-22.865,30-42.42c0-24.813-20.187-45-45-45s-45,20.187-45,45c0,19.555,12.541,36.228,30,42.42V110H73.903L0,272.057v3.259c0,46.068,37.479,83.548,83.548,83.548s83.548-37.479,83.548-83.548v-3.259L106.875,140H227.5v255h-72.241l-30,90h234.481l-30-90H257.5V140h120.625l-60.222,132.057v3.259c0,46.068,37.479,83.548,83.548,83.548S485,321.384,485,275.315v-3.259L411.097,110z M242.5,30c8.271,0,15,6.729,15,15s-6.729,15-15,15s-15-6.729-15-15S234.229,30,242.5,30z M83.548,328.863c-24.321,0-44.894-16.301-51.397-38.548h102.794C128.442,312.562,107.869,328.863,83.548,328.863z M128.77,260.315H38.327l45.222-99.164L128.77,260.315z M318.118,455H166.882l10-30h131.235L318.118,455z M401.452,161.151l45.222,99.164H356.23L401.452,161.151z M401.452,328.863c-24.321,0-44.894-16.301-51.397-38.548h102.794C446.346,312.562,425.772,328.863,401.452,328.863z"/>
            </svg>
          </template>
        </PropertyItem>

        <!-- Melting Point -->
        <PropertyItem 
          v-if="meltingPointDisplay"
          label="MP"
          :value="meltingPointDisplay"
        >
          <template #icon>
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
              <path d="M9.5 12.5a1.5 1.5 0 1 1-2-1.415V6.5a.5.5 0 0 1 1 0v4.585a1.5 1.5 0 0 1 1 1.415"/>
              <path d="M5.5 2.5a2.5 2.5 0 0 1 5 0v7.55a3.5 3.5 0 1 1-5 0zM8 1a1.5 1.5 0 0 0-1.5 1.5v7.987l-.167.15a2.5 2.5 0 1 0 3.333 0l-.166-.15V2.5A1.5 1.5 0 0 0 8 1"/>
            </svg>
          </template>
        </PropertyItem>

        <!-- Formula -->
        <PropertyItem 
          v-if="props.chemical.identifier.chem_formula"
          label="Formula"
          :value="formulaHtml"
          :isHtml="true"
        >
          <template #icon>
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
              <path d="M43.8,41.2,30,17V8h2a2,2,0,0,0,2-2,1.9,1.9,0,0,0-2-2H15.9a2,2,0,1,0,0,4H18v9L4.2,41.2A2,2,0,0,0,6,44H42A2,2,0,0,0,43.8,41.2ZM22,18.1V8h4V18.1L31.7,28H16.3ZM9.5,40,14,32H34l4.5,8Z"/>
            </svg>
          </template>
        </PropertyItem>

        <!-- State of Matter -->
        <PropertyItem 
          v-if="props.chemical.physical_property.state_of_matter"
          label="State"
          :value="stateOfMatterCapitalized"
        >
          <template #icon>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 22a7 7 0 007-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 007 7z"/>
            </svg>
          </template>
        </PropertyItem>
      </div>
    </div>
  </div>
</template>

<script setup>
import PropertyItem from "~/components/PropertyItem.vue"

import utils from "~/utils/util"

const props = defineProps({
  chemical: {
    type: Object,
    required: true
  }
})

// Computed Properties
const meltingPointDisplay = computed(() => {
  const { mp_lower_bound, mp_upper_bound } = props.chemical.physical_property
  
  if (mp_lower_bound && mp_upper_bound) {
    return `${mp_lower_bound}–${mp_upper_bound} °C`
  } else if (mp_lower_bound && !mp_upper_bound) {
    return `≥ ${mp_lower_bound} °C`
  } else if (!mp_lower_bound && mp_upper_bound) {
    return `≤ ${mp_upper_bound} °C`
  }
  return null
})

const formulaHtml = computed(() => {
  return utils.replaceStringNumberBySubscript(props.chemical.identifier.chem_formula)
})

const stateOfMatterCapitalized = computed(() => {
  return props.chemical.physical_property.state_of_matter
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
})
</script>