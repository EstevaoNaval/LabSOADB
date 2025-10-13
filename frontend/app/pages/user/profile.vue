<template>
    <main class="min-h-screen">
        <section 
            :class="themeStore.isDarkMode 
                ? 'dashboard-buttons-background-dark bg-scroll bg-cover bg-center' 
                : 'dashboard-buttons-background-light bg-scroll bg-cover bg-center'"
        >
            <div 
                :class="themeStore.isDarkMode 
                    ? 'bg-base-300/80 backdrop-blur-sm' 
                    : 'bg-base-100/60 backdrop-blur-sm'"
                class="min-h-screen"
            >
                <!-- Header Section -->
                <div class="container mx-auto px-4 pt-8 pb-6">
                    <div class="text-center mb-2">
                        <h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                            Account Settings
                        </h1>
                        <p class="text-base-content/70 mt-2 text-sm md:text-base">
                            Manage your profile information and security settings
                        </p>
                    </div>
                </div>

                <!-- Content Grid -->
                <div class="container mx-auto px-4 pb-12">
                    <div class="grid lg:grid-cols-2 gap-6 lg:gap-8 max-w-6xl mx-auto">
                        <!-- Profile Card -->
                        <div class="w-full">
                            <div class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow duration-300">
                                <div class="card-body p-6 md:p-8">
                                    <div class="flex items-center gap-3 mb-6">
                                        <div class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                            </svg>
                                        </div>
                                        <h2 class="card-title text-2xl">My Profile</h2>
                                    </div>
                                    <update-user-form />
                                </div>
                            </div>
                        </div>

                        <!-- Password Card -->
                        <div class="w-full">
                            <div class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow duration-300">
                                <div class="card-body p-6 md:p-8">
                                    <div class="flex items-center gap-3 mb-6">
                                        <div class="w-10 h-10 rounded-full bg-secondary/10 flex items-center justify-center">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                            </svg>
                                        </div>
                                        <h2 class="card-title text-2xl">Security</h2>
                                    </div>
                                    <update-password-form />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
</template>

<script setup>
import UpdateUserForm from '~/components/UpdateUserForm.vue'
import UpdatePasswordForm from '~/components/UpdatePasswordForm.vue'
import { useThemeStore } from '~/stores/theme'

const themeStore = useThemeStore()
</script>

<style scoped>
.dashboard-buttons-background-dark {
    background-image: url('~/assets/user_profile_background.png');
}

.dashboard-buttons-background-light {
    background-image: url('~/assets/user_profile_background.png');
}
</style>