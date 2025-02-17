<template>
    <form
        @submit.prevent="handleLogin"
        autocomplete="on"
    >
        <p 
            :class="themeStore.isDarkMode ? 'p-2 text-lg mx-auto text-error font-semibold text-center' : 'p-2 text-lg mx-auto text-red-700 font-semibold text-center'" 
            v-if="authStore.error && authStore.error.connection"
        >
            {{ authStore.error.connection }}
        </p>

        <p 
            :class="themeStore.isDarkMode ? 'p-2 text-lg mx-auto text-warning font-semibold text-center' : 'p-2 text-lg mx-auto text-yellow-700 font-semibold text-center'" 
            v-if="authStore.error && authStore.error.error"
        >
            {{ authStore.error.error }}
        </p>
        
        <div class="mb-6">
            <div class="text-md font-bold mb-2" for="email">
                Email
            </div>
            <input 
                class="shadow appearance-none input outline outline-1 outline-slate-400 rounded-lg w-full py-2 px-3 leading-tight focus:outline-slate-400" 
                v-model="email"
                name="email" 
                id="email" 
                type="email" 
                placeholder="exemplo@gmail.com" 
                required
            >
            <p 
                :class="themeStore.isDarkMode ? 'text-error font-semibold mt-1' : 'text-red-700 font-semibold mt-1'" 
                v-if="authStore.error && authStore.error.email"
            >
                {{ authStore.error.email }}
            </p>
        </div>
        <div class="mb-10">
            <div class="text-md font-bold mb-2" for="password">
                Password
            </div>
            <input 
                class="shadow appearance-none input outline outline-1 outline-slate-400 rounded-lg w-full py-2 px-3 leading-tight focus:outline-slate-400" 
                v-model="password"
                name="password" 
                id="password" 
                type="text" 
                placeholder="******************" 
                required
            >
            <p 
                :class="themeStore.isDarkMode ? 'text-error font-semibold mt-1' : 'text-red-700 font-semibold mt-1'" 
                v-if="authStore.error && authStore.error.password"
            >
                {{ authStore.error.password }}
            </p>
        </div>
        <div class="flex flex-col items-center justify-between gap-6 mb-8">
            <button class="btn btn-primary font-bold text-xl py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline w-full" type="input">
                Log In
            </button>
            <a class="link text-lg align-baseline font-semibold duration-200 hover:link-secondary hover:underline" href="#">
                Forgot Password?
            </a>
        </div>
    </form>
    <div class="divider">OR</div>
    <div class="flex flex-col items-center justify-between gap-4 pt-4">
        <NuxtLink to="/auth/register" class="btn btn-primary font-bold text-xl py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline w-3/4" type="input">
            Sign Up
        </NuxtLink>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth';
import { useThemeStore } from '~/stores/theme';
import { useUserStore } from '~/stores/user';
import { useToast } from 'vue-toastification';

const router = useRouter()

const authStore = useAuthStore()
const userStore = useUserStore()
const themeStore = useThemeStore()

const toast = useToast();

const email = ref(null)
const password = ref(null)

async function handleLogin() {
    console.log(`${email.value} ${password.value}`)
    
    await authStore.login(email.value, password.value)

    if(authStore.error) {
        return;
    }
    
    await userStore.fetchUserProfile()
    
    toast.success('User logged in successfully')

    router.push('/home')
}

onBeforeMount(() => {
    authStore.clearError();
})

onBeforeUnmount(() => {
    authStore.clearError();
});
</script>