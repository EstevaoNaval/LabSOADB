<template>
    <table class="ml-auto table table-auto table-zebra table-pin-rows">
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
                <td>{{ chemical.identifier.chem_formula }}</td>
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
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8 mx-auto">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                    </svg>
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