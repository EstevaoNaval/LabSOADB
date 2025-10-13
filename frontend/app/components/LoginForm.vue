<template>
    <main>
        <form @submit.prevent="handleLogin" autocomplete="on" class="space-y-6">
            <!-- Global Error Alert -->
            <div v-if="authStore.error && authStore.error.length > 0" class="alert alert-error">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div class="flex flex-col gap-1">
                    <span v-for="(err, idx) in authStore.error" :key="idx">{{ err }}</span>
                </div>
            </div>

            <!-- Email Field -->
            <div class="form-control">
                <label for="email" class="label justify-start px-0">
                    <span class="label-text font-medium">Email</span>
                </label>
                <input 
                    id="email"
                    v-model="email"
                    type="email" 
                    name="email"
                    placeholder="exemplo@gmail.com"
                    autocomplete="email"
                    class="input input-bordered w-full focus:input-primary"
                    :class="{ 'input-error': authStore.error?.email }"
                    required
                >
                <label v-if="authStore.error?.email" class="label px-0">
                    <span class="label-text-alt text-error">{{ authStore.error.email }}</span>
                </label>
            </div>

            <!-- Password Field -->
            <div class="form-control">
                <label for="password" class="label justify-start px-0">
                    <span class="label-text font-medium">Password</span>
                </label>
                <div class="relative">
                    <input 
                        id="password"
                        v-model="password"
                        :type="showPassword ? 'text' : 'password'"
                        name="password"
                        placeholder="Enter your password"
                        autocomplete="current-password"
                        class="input input-bordered w-full pr-12 focus:input-primary"
                        :class="{ 'input-error': authStore.error?.password }"
                        required
                    >
                    <button 
                        type="button" 
                        class="absolute inset-y-0 right-0 flex items-center pr-3 hover:text-primary transition-colors"
                        @click="showPassword = !showPassword"
                        tabindex="-1"
                        aria-label="Toggle password visibility"
                    >
                        <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                        </svg>
                    </button>
                </div>
                <label v-if="authStore.error?.password" class="label px-0">
                    <span class="label-text-alt text-error">{{ authStore.error.password }}</span>
                </label>
            </div>

            <!-- Forgot Password Link -->
            <div class="text-right -mt-2">
                <NuxtLink 
                    to="/auth/forgot-password" 
                    class="link link-hover text-sm font-medium hover:link-primary"
                >
                    Forgot your password?
                </NuxtLink>
            </div>

            <!-- Login Button -->
            <div class="form-control pt-2">
                <button 
                    type="submit" 
                    class="btn btn-primary btn-lg w-full gap-2"
                    :disabled="isLoading"
                    :class="{ 'loading': isLoading }"
                >
                    <svg v-if="!isLoading" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75" />
                    </svg>
                    <span v-if="!isLoading">Log In</span>
                    <span v-else>Logging in...</span>
                </button>
            </div>
        </form>

        <!-- Divider -->
        <div class="divider my-8">OR</div>

        <!-- Sign Up Section -->
        <div class="text-center space-y-4">
            <p class="text-base-content/70">Don't have an account?</p>
            <NuxtLink 
                to="/auth/register" 
                class="btn btn-outline btn-primary btn-lg w-full gap-2"
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
                </svg>
                Create Account
            </NuxtLink>
        </div>
    </main>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'
import { useUserStore } from '~/stores/user'
import { useToast } from 'vue-toastification'

const router = useRouter()
const authStore = useAuthStore()
const userStore = useUserStore()
const toast = useToast()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const isLoading = ref(false)

async function handleLogin() {
    // Clear previous errors
    authStore.clearError()
    isLoading.value = true

    try {
        await authStore.login(email.value, password.value)

        if (authStore.error && authStore.error.length > 0) {
            return
        }
        
        await userStore.fetchUserProfile()
        
        // Show toast before redirect
        toast.success('Welcome back!')
        
        // Small delay for better UX
        await new Promise(resolve => setTimeout(resolve, 500))
        
        router.push('/dashboard')
    } catch (error) {
        console.error('Login error:', error)
    } finally {
        isLoading.value = false
    }
}

onBeforeMount(() => {
    authStore.clearError()
})

onBeforeUnmount(() => {
    authStore.clearError()
})
</script>