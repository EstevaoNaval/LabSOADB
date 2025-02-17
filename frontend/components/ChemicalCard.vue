<template>
    <div class="card bg-base-300">
        <figure>
            <NuxtImg
                v-if="props.chemical.chem_depiction_image"
                :src="props.chemical.chem_depiction_image"
                alt="Molecular Structure"
                class="mx-auto"
                format="svg"
                loading="lazy"
            />
        </figure>
        <div class="card-body">
            <h2 class="card-title text-lg font-bold">{{ truncatedName }}</h2>
            
            <div class="flex justify-between items-center">
                <p class="text-lg font-semibold text-slate-500 text-opacity-75">{{ props.chemical.api_id }}</p>
            </div>
           
            <div class="grid grid-cols-2 gap-4">
                <div class="flex flex-col mx-auto" v-if="props.chemical.identifier.chem_formula">
                    <div class="flex mx-auto gap-1">
                        <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="size-5 m-auto" fill="currentColor"
                            viewBox="0 0 485 485" style="enable-background:new 0 0 485 485;" xml:space="preserve">
                            <path d="M411.097,110H257.5V87.42c17.459-6.192,30-22.865,30-42.42c0-24.813-20.187-45-45-45s-45,20.187-45,45
                            	c0,19.555,12.541,36.228,30,42.42V110H73.903L0,272.057v3.259c0,46.068,37.479,83.548,83.548,83.548s83.548-37.479,83.548-83.548
                            	v-3.259L106.875,140H227.5v255h-72.241l-30,90h234.481l-30-90H257.5V140h120.625l-60.222,132.057v3.259
                            	c0,46.068,37.479,83.548,83.548,83.548S485,321.384,485,275.315v-3.259L411.097,110z M242.5,30c8.271,0,15,6.729,15,15
                            	s-6.729,15-15,15s-15-6.729-15-15S234.229,30,242.5,30z M83.548,328.863c-24.321,0-44.894-16.301-51.397-38.548h102.794
                            	C128.442,312.562,107.869,328.863,83.548,328.863z M128.77,260.315H38.327l45.222-99.164L128.77,260.315z M318.118,455H166.882
                            	l10-30h131.235L318.118,455z M401.452,161.151l45.222,99.164H356.23L401.452,161.151z M401.452,328.863
                            	c-24.321,0-44.894-16.301-51.397-38.548h102.794C446.346,312.562,425.772,328.863,401.452,328.863z"
                            />
                        </svg>

                        <p>MW</p>
                    </div>
                    
                    <p class="mx-auto text-center font-bold">{{ props.chemical.physical_property.molecular_weight.toFixed(1) }} g/mol</p>
                </div>
                <div class="flex flex-col" v-if="chemical.physical_property.mp_lower_bound && chemical.physical_property.mp_upper_bound">
                    <div class="flex mx-auto">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-thermometer-half size-6 m-auto" viewBox="0 0 16 16">
                          <path d="M9.5 12.5a1.5 1.5 0 1 1-2-1.415V6.5a.5.5 0 0 1 1 0v4.585a1.5 1.5 0 0 1 1 1.415"/>
                          <path d="M5.5 2.5a2.5 2.5 0 0 1 5 0v7.55a3.5 3.5 0 1 1-5 0zM8 1a1.5 1.5 0 0 0-1.5 1.5v7.987l-.167.15a2.5 2.5 0 1 0 3.333 0l-.166-.15V2.5A1.5 1.5 0 0 0 8 1"/>
                        </svg>
                        <p >MP</p>
                    </div>
                    
                    <p class="mx-auto text-center font-bold">{{ chemical.physical_property.mp_lower_bound }} – {{ chemical.physical_property.mp_upper_bound }} °C</p>
                </div>
                <div class="flex flex-col" v-if="chemical.physical_property.mp_lower_bound && !chemical.physical_property.mp_upper_bound">
                    <div class="flex mx-auto">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-thermometer-half size-6 m-auto" viewBox="0 0 16 16">
                          <path d="M9.5 12.5a1.5 1.5 0 1 1-2-1.415V6.5a.5.5 0 0 1 1 0v4.585a1.5 1.5 0 0 1 1 1.415"/>
                          <path d="M5.5 2.5a2.5 2.5 0 0 1 5 0v7.55a3.5 3.5 0 1 1-5 0zM8 1a1.5 1.5 0 0 0-1.5 1.5v7.987l-.167.15a2.5 2.5 0 1 0 3.333 0l-.166-.15V2.5A1.5 1.5 0 0 0 8 1"/>
                        </svg>
                        <p>MP</p>
                    </div>
                    <p class="mx-auto text-center font-bold">≥ {{ chemical.physical_property.mp_lower_bound }} °C</p>
                </div>
                <div class="flex flex-col" v-if="!chemical.physical_property.mp_lower_bound && chemical.physical_property.mp_upper_bound">
                    <div class="flex mx-auto">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-thermometer-half size-6 m-auto" viewBox="0 0 16 16">
                          <path d="M9.5 12.5a1.5 1.5 0 1 1-2-1.415V6.5a.5.5 0 0 1 1 0v4.585a1.5 1.5 0 0 1 1 1.415"/>
                          <path d="M5.5 2.5a2.5 2.5 0 0 1 5 0v7.55a3.5 3.5 0 1 1-5 0zM8 1a1.5 1.5 0 0 0-1.5 1.5v7.987l-.167.15a2.5 2.5 0 1 0 3.333 0l-.166-.15V2.5A1.5 1.5 0 0 0 8 1"/>
                        </svg>
                        <p>MP</p>
                    </div>
                    <p class="mx-auto text-center font-bold">≤ {{ chemical.physical_property.mp_lower_bound }} °C</p>
                </div>
                <div class="flex flex-col mx-auto" v-if="props.chemical.identifier.chem_formula">
                    <div class="flex mx-auto gap-1">
                        <svg class="size-5 m-auto" fill="currentColor" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                            <g id="Layer_2" data-name="Layer 2">
                              <g id="invisible_box" data-name="invisible box">
                                <rect width="48" height="48" fill="none"/>
                              </g>
                              <g id="Layer_6" data-name="Layer 6">
                                <path d="M43.8,41.2,30,17V8h2a2,2,0,0,0,2-2,1.9,1.9,0,0,0-2-2H15.9a2,2,0,1,0,0,4H18v9L4.2,41.2A2,2,0,0,0,6,44H42A2,2,0,0,0,43.8,41.2ZM22,18.1V8h4V18.1L31.7,28H16.3ZM9.5,40,14,32H34l4.5,8Z"/>
                              </g>
                            </g>
                        </svg>

                        <p>Formula</p>
                    </div>
                    
                    <p class="mx-auto font-bold">{{ truncatedFormula }}</p>
                </div>
                <div class="flex flex-col mx-auto" v-if="chemical.physical_property.state_of_matter">
                    <div class="flex mx-auto gap-1">
                        <svg 
                            xmlns="http://www.w3.org/2000/svg"
                            class="size-5 m-auto"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        >
                            <path d="M12 22a7 7 0 007-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 007 7z" />
                        </svg>

                        <p>State</p>
                    </div>
                    
                    <p class="mx-auto text-center font-bold">{{ state_of_matter_capitalized }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>

const props = defineProps({
    chemical: {
        type: Object,
        required: true
    }
})

const nameMaxLength = 30;  // Define o limite de caracteres
const formulaMaxLength = 11;

const state_of_matter_capitalized = capitalizeFirstLetter(props.chemical.physical_property.state_of_matter) 

// Função para truncar o nome IUPAC
const truncatedName = computed(() => {
  return props.chemical.identifier.iupac_name.length > nameMaxLength
    ? props.chemical.identifier.iupac_name.slice(0, nameMaxLength) + '...'
    : props.chemical.identifier.iupac_name;
});

const truncatedFormula = computed(() => {
    return props.chemical.identifier.chem_formula.length > formulaMaxLength
    ? props.chemical.identifier.chem_formula.slice(0, formulaMaxLength) + '...'
    : props.chemical.identifier.chem_formula
})

function capitalizeFirstLetter(str) {
    return str.split(' ').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ');
}

</script>