<template>
    <table class="ml-auto text-center table table-auto table-zebra table-pin-rows">
        <!-- head -->
        <thead class="text-sm md:text-lg">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Formula</th>
                <th>Reference</th>
                <th>Created At</th>
                <th></th>
            </tr>
        </thead>
        <tbody class="text-sm md:text-lg font-normal">
            <tr v-for="chemical in userChemicalsStore.chemicals" :key="chemical.api_id" class="hover">
                <td>{{ chemical.api_id }}</td>
                <td>
                    <div class="md:max-w-xs max-w-full whitespace-normal break-words lg:tooltip lg:tooltip-up" :data-tip="iupac">
                        <span>{{ utils.truncateString(chemical.identifier.iupac_name) }}</span>
                    </div>
                </td>
                <td v-html="utils.replaceStringNumberBySubscript(chemical.identifier.chem_formula)"></td>
                <td class="md:max-w-xs max-w-full whitespace-normal break-words">
                    <a 
                      href="https://www.doi.org/10.2174/1568026618666181002110116" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      class="link-lg link-sm"
                    >
                        {{ chemical.literature[0].doi }}
                    </a>
                </td>
                <td>{{ utils.formatTimestamp(chemical.created_at) }}</td>
                <td>
                    <NuxtLink :to="`/chemicals/${chemical.api_id}`" class="flex cursor-pointer transition-transform duration-150 hover:scale-110 active:scale-90">
                        <!--<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 md:size-8 mx-auto">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                        </svg>-->
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 md:size-8 mx-auto">
                            <title>More details</title>
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                        </svg>

                    </NuxtLink>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script setup>
    import utils from '~/utils/util'
    import { onBeforeMount, onUnmounted } from 'vue';
    import { useUserChemicalsStore } from '~/stores/userChemicals';
    
    const userChemicalsStore = useUserChemicalsStore()

    async function fetchUserChemicals(page) {
        await userChemicalsStore.fetchChemicalsPerUser({ page: page })
    }

    onBeforeMount(() => {
        fetchUserChemicals(1)
    })

    onUnmounted(() => {
        userChemicalsStore.$reset()
    })
</script>

<style scoped>
.link-sm {
  @apply link link-secondary;
}

.link-lg {
  @apply lg:link-primary duration-200 lg:hover:text-secondary;
}
</style>