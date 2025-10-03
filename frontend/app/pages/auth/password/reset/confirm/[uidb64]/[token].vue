<template>
    <div :class="themeStore.isDarkMode ? 'login-form-page-art-dark hero min-h-screen hidden md:grid md:grid-col-1' : 'login-form-page-art-light hero min-h-screen hidden md:grid md:grid-col-1'">
        <div class="hero-overlay bg-opacity-60 bg-base-200"></div>
        <div class="hero-content w-full flex flex-col">
            
            <div class="w-1/2 rounded-lg p-8 items-center bg-base-300 space-y-6">
                <NuxtLink to="/home" class="text-2xl text-primary">
                    <img src="~/assets/labsodb_logo_dark.webp" v-if="themeStore.isDarkMode" class="m-auto w-52" />
                    <img src="~/assets/labsodb_logo_light.webp" v-else class="m-auto w-52" />
                </NuxtLink>
                <h2 class="text-center text-4xl font-semibold">Password Reset</h2>
                <password-reset></password-reset>
            </div>
        </div>
    </div>

    <div :class="themeStore.isDarkMode ? 'hero min-h-screen login-form-page-art-dark md:hidden' : 'hero min-h-screen login-form-page-art-light md:hidden'">
        <div class="hero-overlay bg-opacity-60 bg-base-200"></div>
        <div class="hero-content w-full flex flex-col">
            <NuxtLink to="/home" class="text-lg text-primary md:hidden">
                <img src="~/assets/labsodb_logo_dark.webp" v-if="themeStore.isDarkMode" class="my-auto w-52" />
                <img src="~/assets/labsodb_logo_light.webp" v-else class="my-auto w-52" />
            </NuxtLink>
            <div class="mx-auto w-full rounded-lg p-8 items-center bg-base-300">
                <password-reset></password-reset>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { useThemeStore } from "~/stores/theme.js"

    import PasswordReset from "~/components/PasswordReset.vue";

    const themeStore = useThemeStore()

</script>

<style scoped>
    .email-confirmation-page-art-dark {
        background-image: url('~/assets/email_confirmation_background_dark.webp');
    }

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