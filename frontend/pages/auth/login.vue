<template>
    <section class="h-screen bg-base-200 hidden md:flex">
        <div v-if="themeStore.isDarkMode" class="hidden md:flex md:flex-col w-1/2 p-12  justify-center bg-base-100 login-form-page-art-dark image-container"></div>
        <div v-else class="hidden md:flex md:flex-col w-1/2 p-12 justify-center bg-base-100 login-form-page-art-light image-container"></div>

        <div class="w-full md:w-1/2 flex flex-col pt-4 items-center md:justify-center gap-8">
            <div class="mx-auto rounded-lg p-8 w-[90%] lg:w-3/4 max-w-md items-center bg-base-300">
                <login-form></login-form>
            </div>
        </div>
    </section>

    <div :class="themeStore.isDarkMode ? 'hero min-h-screen login-form-page-art-dark md:hidden' : 'hero min-h-screen login-form-page-art-light md:hidden'">
        <div class="hero-overlay bg-opacity-60 bg-base-200"></div>
        <div class="hero-content w-full flex flex-col">
            <div class="mx-auto w-full rounded-lg p-8 items-center bg-base-300">
                <login-form></login-form>
            </div>
        </div>
    </div>
</template>
  
<script setup>
    import { useThemeStore } from '~/stores/theme';
    import LoginForm from '~/components/LoginForm.vue';

    const themeStore = useThemeStore()
</script>

<style scoped>
    .login-form-page-art-dark {
        background-image: url('~/assets/login_form_page_art_dark.webp');
    }

    .login-form-page-art-light {
        background-image: url('~/assets/login_form_page_art_light.webp');
    }

    .image-container {
      background-size: cover;
      background-position: center;
    }
</style>