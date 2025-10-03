<template>
    <div class="space-y-6 text-center hidden md:flex md:flex-col">
        <h2 class="text-4xl font-semibold">Congratulations!</h2>
        <div class="text-xl">
            <p>Your email has already been confirmed.</p>
            <p>You can now login to LabSOADB.</p>
        </div>
        <svg class="mx-auto size-24" viewBox="0 0 48 48" version="1" xmlns="http://www.w3.org/2000/svg">
            <circle :fill="themeStore.isDarkMode ? '#38bdf8' : '#0069ff'" cx="24" cy="24" r="21"/>
            <path fill="white" d="M34.6 14.6 21 28.2l-5.6-5.6-2.8 2.8 8.4 8.4 16.4-16.4z"/>
        </svg>
        <p :class="themeStore.isDarkMode ? 'font-medium text-lg text-slate-500' : 'font-medium text-lg text-slate-400'">NOTE: You may leave this page.</p>
    </div>

    <div class="space-y-6 text-center md:hidden">
        <h2 class="text-3xl font-semibold">Congratulations!</h2>
        <div class="text-lg">
            <p>Your email has already been confirmed.</p>
            <p>You can now login to LabSOADB.</p>
        </div>
        <svg class="mx-auto size-20" viewBox="0 0 48 48" version="1" xmlns="http://www.w3.org/2000/svg">
            <circle :fill="themeStore.isDarkMode ? '#38bdf8' : '#0069ff'" cx="24" cy="24" r="21"/>
            <path fill="white" d="M34.6 14.6 21 28.2l-5.6-5.6-2.8 2.8 8.4 8.4 16.4-16.4z"/>
        </svg>
        <p :class="themeStore.isDarkMode ? 'font-medium text-lg text-slate-500' : 'font-medium text-lg text-slate-400'">NOTE: You may leave this page.</p>
    </div>
    
</template>

<script setup>
    import { useUserStore } from "~/stores/user";
    import { useThemeStore } from "~/stores/theme";

    const route = useRoute();
    const queryParams = route.query

    const userStore = useUserStore()
    const themeStore = useThemeStore()

    async function verifyEmail() {
        await userStore.verifyEmail(queryParams.key)
    }

    onBeforeMount(() => {
        verifyEmail()
    })
</script>

<style>

</style>