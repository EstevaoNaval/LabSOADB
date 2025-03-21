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
            <tr class="hover">
                <td>LSOA54875455</td>
                <td>
                    <div class="md:max-w-xs max-w-full whitespace-normal break-words lg:tooltip lg:tooltip-up" :data-tip="iupac">
                        <span>Methyl benzyl((4-chlorophenyl)...</span>
                    </div>
                </td>
                <td>C26H22N4O6</td>
                <td class="md:max-w-xs max-w-full whitespace-normal break-words">
                    <a 
                      href="https://www.doi.org/10.2174/1568026618666181002110116" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      class="link-lg link-sm"
                    >
                        10.2174/1568026618666181002110116
                    </a>
                </td>
                <td>2024-05-01, 15:07 PM</td>
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

</script>

<style scoped>
.link-sm {
  @apply link link-secondary;
}

.link-lg {
  @apply lg:link-primary duration-200 lg:hover:text-secondary;
}
</style>