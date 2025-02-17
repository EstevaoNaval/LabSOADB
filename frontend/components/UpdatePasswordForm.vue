<template>
    <form
        :action="registerAPIUrl" 
        @submit.prevent="handleUserRegistration"
    >
        <div class="mb-6">
            <div class="text-md font-bold mb-2" for="password">
                Current Password
            </div>
            <div class="relative">
                <input 
                    class="shadow appearance-none input outline outline-1 outline-slate-400 rounded-lg w-full py-2 px-3 leading-tight focus:outline-slate-400" 
                    name="password" 
                    id="password" 
                    :type="passwordType" 
                    placeholder="******************"
                    :minlength="passwordMinLength"
                    :maxlength="passwordMaxLength"
                    v-model="password"
                    required
                >
                <button type="button" class="absolute inset-y-0 right-0 flex items-center px-2 btn btn-ghost m-auto mr-2" @click="togglePasswordVisibility">
                    <svg xmlns="http://www.w3.org/2000/svg" v-if="isPasswordVisible" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    </svg>
                    <svg xmlns="http://www.w3.org/2000/svg" v-else fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>
                </button>
            </div>
        </div>
        <div class="mb-6">
            <div class="text-md font-bold mb-2" for="password">
                Password
            </div>
            <div class="relative">
                <input 
                    class="shadow appearance-none input outline outline-1 outline-slate-400 rounded-lg w-full py-2 px-3 leading-tight focus:outline-slate-400" 
                    name="password" 
                    id="password" 
                    :type="passwordType" 
                    placeholder="******************"
                    :minlength="passwordMinLength"
                    :maxlength="passwordMaxLength"
                    v-model="password"
                    required
                >
                <button type="button" class="absolute inset-y-0 right-0 flex items-center px-2 btn btn-ghost m-auto mr-2" @click="togglePasswordVisibility">
                    <svg xmlns="http://www.w3.org/2000/svg" v-if="isPasswordVisible" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    </svg>
                    <svg xmlns="http://www.w3.org/2000/svg" v-else fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>
                </button>
            </div>

        </div>
        <div class="mb-10">
            <div class="text-md font-bold mb-2" for="password_confirmation">
                Confirm Password
            </div>
            <div class="relative">
                <input 
                    class="shadow appearance-none input outline outline-1 outline-slate-400 rounded-lg w-full py-2 px-3 leading-tight focus:outline-slate-400" 
                    name="password_confirmation" 
                    id="password_confirmation" 
                    :type="passwordType" 
                    placeholder="******************" 
                    :minlength="passwordMinLength"
                    :maxlength="passwordMaxLength"
                    v-model="password_confirmation"
                    required
                >
                <button type="button" class="absolute inset-y-0 right-0 flex items-center px-2 btn btn-ghost m-auto mr-2" @click="togglePasswordVisibility">
                    <svg xmlns="http://www.w3.org/2000/svg" v-if="isPasswordVisible" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    </svg>
                    <svg xmlns="http://www.w3.org/2000/svg" v-else fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>
                </button>
            </div>

        </div>
        <div class="items-center justify-between">
            <button class="btn btn-primary font-bold text-xl py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline w-full" type="input">
                Update
            </button>
        </div>
    </form>
    </template>
    
    <script setup>
    import { useAuthStore } from '~/stores/auth';
    import { useUserStore } from '~/stores/user';
    import { useRouter } from 'vue-router';
    
    const config = useRuntimeConfig()
    
    const router = useRouter()
    
    const userStore = useUserStore()
    const authStore = useAuthStore()
    
    const registerAPIUrl = config.public.apiHost + config.public.registerAPIEndpoint
    
    let isPasswordVisible = ref(false)
    let passwordType = ref("password")
    let passwordMinLength = 12
    let passwordMaxLength = 100
    
    let username = ref(null)
    const maxUsernameLength = 50
    const usernamePattern = "[A-Za-z0-9_\\-]+"
    
    async function handleUserRegistration() {
        let userData = {
            'first_name': first_name.value,
            'last_name': last_name.value,
            'username': username.value,
            'email': email.value,
            'password': password.value,
            'password_confirmation': password_confirmation.value
        }
    
        await userStore.registerUser(userData)
    
        if(userStore.error) {
            return;
        }
    
        await authStore.login(userData.email, userData.password)
    
        if(authStore.error) {
            return;
        }
    
        await userStore.fetchUserProfile()
    
        router.push({
            'path': '/home'
        })
    }
    
    function togglePasswordVisibility() {
        isPasswordVisible.value = !isPasswordVisible.value
        passwordType.value = isPasswordVisible.value ? "text" : "password"
    }
    
    function clearCustomMessage(e) {
        e.target.setCustomValidity("");
    }
    
    function setCustomMessage(e) {
        let usernameErrorMessage = ""
    
        let usernameNotAllowedPattern = /[^A-Za-z0-9_\-]/g
    
        let usernameNotAllowedPatternMatches = [...username.value.matchAll(usernameNotAllowedPattern)].map((x) => x[0])
    
        if (usernameNotAllowedPatternMatches.length > 0) {
            usernameErrorMessage = usernameNotAllowedPatternMatches.length == 1 ? 
            `The character ${usernameNotAllowedPatternMatches.join(' ')} is not allowed` :
            `The characters ${usernameNotAllowedPatternMatches.join(' ')} are not allowed.`
    
            usernameErrorMessage += "\nOnly letters (A-Z, a-z), numbers (0-9), hyphens (-), and underscores (_) are allowed."
    
            e.target.setCustomValidity(usernameErrorMessage)
        } else {
            e.target.setCustomValidity("");
        }
        
    }
    </script>
    
    <style>
    
    </style>