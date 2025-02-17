<template>
    <form
        :action="registerAPIUrl" 
        @submit.prevent="handlePasswordReset"
    >
        <div class="mb-6">
            <div class="text-md font-bold mb-2" for="password1">
                New Password*
            </div>
            <div class="relative">
                <input 
                    class="shadow appearance-none input outline outline-1 outline-slate-400 rounded-lg w-full py-2 px-3 leading-tight focus:outline-slate-400" 
                    name="password1" 
                    id="password1" 
                    :type="passwordType" 
                    placeholder="******************"
                    :minlength="passwordMinLength"
                    :maxlength="passwordMaxLength"
                    v-model="password1"
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
            <template v-if="authStore.error && authStore.error.password" >
                <p 
                    :class="themeStore.isDarkMode ? 'text-error font-semibold mt-1' : 'text-red-700 font-semibold mt-1'" 
                    v-for="[index, password1Error] of authStore.error.password.entries()" :key="index"
                >
                    {{ password1Error }}
                </p>
            </template>
        </div>
        <div class="mb-10">
            <div class="text-md font-bold mb-2" for="password2">
                Confirm New Password*
            </div>
            <div class="relative">
                <input 
                    class="shadow appearance-none input outline outline-1 outline-slate-400 rounded-lg w-full py-2 px-3 leading-tight focus:outline-slate-400" 
                    name="password2" 
                    id="password2" 
                    :type="passwordType" 
                    placeholder="******************" 
                    :minlength="passwordMinLength"
                    :maxlength="passwordMaxLength"
                    v-model="password2"
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
            <template v-if="authStore.error && authStore.error.password2" >
                <p 
                    :class="themeStore.isDarkMode ? 'text-error font-semibold mt-1' : 'text-red-700 font-semibold mt-1'" 
                    v-for="[index, password2Error] of authStore.error.password2.entries()" :key="index"
                >
                    {{ password2Error }}
                </p>
            </template>
            
        </div>
        <button class="btn btn-primary w-full font-bold text-xl py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline" type="input">
            Reset Password
        </button>
    </form>
</template>

<script setup>
    import { useAuthStore } from "~/stores/auth";
    import { useThemeStore } from "~/stores/theme";

    const route = useRoute();
    const queryParams = route.query

    const authStore = useAuthStore()
    const themeStore = useThemeStore()

    const password1 = ref(null)

    let isPasswordVisible = ref(false)
    let passwordType = ref("password")
    let passwordMinLength = 10
    let passwordMaxLength = 100

    function togglePasswordVisibility() {
        isPasswordVisible.value = !isPasswordVisible.value
        passwordType.value = isPasswordVisible.value ? "text" : "password"
    }

    async function handlePasswordReset() {
        
    }
</script>

<style>

</style>