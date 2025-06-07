<template>
    <main>
        <NuxtImg src="/images/under_maintenance_dark.png" v-if="themeStore.isDarkMode" class="md:h-[42rem] md:w-[48rem] mx-auto" format="png" loading="lazy" />
        <NuxtImg src="/images/under_maintenance_light.png" v-else class="md:h-[42rem] md:w-[48rem] mt-4 mx-auto" format="png" loading="lazy" />
        <div class="p-8">
            <h1 class="text-center text-2xl md:text-4xl font-semibold">We'll be back soon. Hold it!</h1>
        </div>
    </main>    
</template>

<script setup>
import { useThemeStore } from "~/stores/theme";

const themeStore = useThemeStore()
</script>