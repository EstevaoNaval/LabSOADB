<template>
<form
    :action="registerAPIUrl" 
    @submit.prevent="handleUserRegistration"
>
    <p 
        :class="themeStore.isDarkMode ? 'p-2 text-lg mx-auto text-error font-semibold text-center' : 'p-2 text-lg mx-auto text-red-700 font-semibold text-center'" 
        v-if="userStore.error && userStore.error.connection"
    >
        {{ userStore.error.connection }}
    </p>

    <div class="mb-6 grid grid-cols-2 gap-4">
        <div class="flex flex-col">
            <div class="text-md font-bold mb-2" for="first_name">
                First Name*
            </div>
            <input 
                class="shadow appearance-none input outline outline-1 outline-slate-400 rounded-lg w-full py-2 px-3 leading-tight focus:outline-slate-400" 
                name="first_name" 
                id="first_name" 
                type="text" 
                placeholder="John"
                v-model="first_name" 
                required
            >
            <p 
                :class="themeStore.isDarkMode ? 'text-error font-semibold mt-1' : 'text-red-700 font-semibold mt-1'" 
                v-if="userStore.error && userStore.error.first_name"
            >
                {{ userStore.error.first_name }}
            </p>
        </div>
        <div class="flex flex-col">
            <div class="text-md font-bold mb-2" for="last_name">
                Last Name*
            </div>
            <input 
                class="shadow appearance-none input outline outline-1 outline-slate-400 rounded-lg w-full py-2 px-3 leading-tight focus:outline-slate-400" 
                name="last_name" 
                id="last_name" 
                type="text" 
                placeholder="Snow" 
                v-model="last_name"
                required
            >
            <p 
                :class="themeStore.isDarkMode ? 'text-error font-semibold mt-1' : 'text-red-700 font-semibold mt-1'" 
                v-if="userStore.error && userStore.error.last_name"
            >
                {{ userStore.error.last_name }}
            </p>
        </div>
    </div>
    <div class="mb-6">
        <div class="text-md mb-2 flex gap-1" for="username">
            <p class="font-bold">User Name*</p>
            <div class="dropdown dropdown-hover dropdown-right my-auto">
                <div tabindex="0" role="button" class="m-1">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-question-circle size-4" viewBox="0 0 16 16">
                      <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                      <path d="M5.255 5.786a.237.237 0 0 0 .241.247h.825c.138 0 .248-.113.266-.25.09-.656.54-1.134 1.342-1.134.686 0 1.314.343 1.314 1.168 0 .635-.374.927-.965 1.371-.673.489-1.206 1.06-1.168 1.987l.003.217a.25.25 0 0 0 .25.246h.811a.25.25 0 0 0 .25-.25v-.105c0-.718.273-.927 1.01-1.486.609-.463 1.244-.977 1.244-2.056 0-1.511-1.276-2.241-2.673-2.241-1.267 0-2.655.59-2.75 2.286m1.557 5.763c0 .533.425.927 1.01.927.609 0 1.028-.394 1.028-.927 0-.552-.42-.94-1.029-.94-.584 0-1.009.388-1.009.94"/>
                    </svg>
                </div>
                <ul tabindex="0" class="dropdown-content menu bg-base-100 p-2 w-48 rounded-box z-[1] shadow">
                    <li><p>Valid characters:</p></li>
                    <li class="font-bold"><p>Letters (A-Z, a-z)</p></li>
                    <li class="font-bold"><p>Numbers (0-9)</p></li>
                    <li class="font-bold"><p>Hyphen (-)</p></li>
                    <li class="font-bold"><p>Underscore (_)</p></li>
                </ul>
            </div>
        </div>
        <input 
            v-model.lazy="username" 
            :maxlength="maxUsernameLength" 
            :pattern="usernamePattern"
            @input="clearCustomMessage" 
            @invalid="setCustomMessage" 
            class="shadow appearance-none input outline outline-1 outline-slate-400 rounded-lg w-full py-2 px-3 leading-tight focus:outline-slate-400" 
            name="username" 
            id="username"
            type="text" 
            placeholder="john_snow" 
            required
        >
        <template v-if="userStore.error && userStore.error.username" >
            <p 
                :class="themeStore.isDarkMode ? 'text-error font-semibold mt-1' : 'text-red-700 font-semibold mt-1'" 
                v-for="[index, usernameError] of userStore.error.username.entries()" :key="index"
            >
                {{ usernameError }}
            </p>
        </template>
        
    </div>
    <div class="mb-6">
        <div class="text-md font-bold mb-2" for="email">
            Email*
        </div>
        <input 
            class="shadow appearance-none input outline outline-1 outline-slate-400 rounded-lg w-full py-2 px-3 leading-tight focus:outline-slate-400" 
            name="email" 
            id="email" 
            type="email" 
            placeholder="john.snow@gmail.com" 
            v-model="email"
            required
        >
        <template v-if="userStore.error && userStore.error.email" >
            <p 
                :class="themeStore.isDarkMode ? 'text-error font-semibold mt-1' : 'text-red-700 font-semibold mt-1'" 
                v-for="[index, emailError] of userStore.error.email.entries()" :key="index"
            >
                {{ emailError }}
            </p>
        </template>
    </div>
    <div class="mb-6">
        <div class="text-md font-bold mb-2" for="password">
            Password*
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
        <template v-if="userStore.error && userStore.error.password" >
            <p 
                :class="themeStore.isDarkMode ? 'text-error font-semibold mt-1' : 'text-red-700 font-semibold mt-1'" 
                v-for="[index, passwordError] of userStore.error.password.entries()" :key="index"
            >
                {{ passwordError }}
            </p>
        </template>
    </div>
    <div class="mb-6">
        <div class="text-md font-bold mb-2" for="password_confirmation">
            Confirm Password*
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
        <template v-if="userStore.error && userStore.error.password_confirmation" >
            <p 
                :class="themeStore.isDarkMode ? 'text-error font-semibold mt-1' : 'text-red-700 font-semibold mt-1'" 
                v-for="[index, passwordConfirmationError] of userStore.error.password_confirmation.entries()" :key="index"
            >
                {{ passwordConfirmationError }}
            </p>
        </template>
        
    </div>
    <div class="mb-6">
        
        <label class="label cursor-pointer flex gap-2">
            <input type="checkbox" required class="checkbox checkbox-primary" />
            <span class="label-text text-lg mr-auto ">I am over 18 years old.</span>
        </label>
    </div>
    <div class="grid grid-cols-1 md:hidden items-center justify-between space-y-6">
        <button class="mx-auto btn btn-primary font-bold text-xl py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline w-full" type="input">
            Sign Up
        </button>

        <div class="mx-auto align-baseline">
            Click "Sign Up" to agree to LabSOADB's <a class="link duration-200 font-normal hover:link-secondary hover:underline">Terms of Service</a> 
            and acknowledge that LabSOADB's <a class="link duration-200 font-normal hover:link-secondary hover:underline">Privacy Policy</a> applies to you.
        </div>

        <div class="mx-auto align-baseline text-lg">
            Already a user?
            <NuxtLink to="/auth/login" class=" link duration-200 font-semibold hover:link-secondary hover:underline">
                Log in
            </NuxtLink>
        </div>
        
    </div>
    <div class="hidden md:grid md:grid-cols-1 space-y-6 items-center justify-between">
        <button class="mx-auto w-full btn btn-primary font-bold text-xl py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline" type="input">
            Sign Up
        </button>
        
        <div class="mx-auto align-baseline">
            Click "Sign Up" to agree to LabSOADB's <a class="link duration-200 font-normal hover:link-secondary hover:underline">Terms of Service</a> 
            and acknowledge that LabSOADB's <a class="link duration-200 font-normal hover:link-secondary hover:underline">Privacy Policy</a> applies to you.
        </div>

        <div class="mx-auto align-baseline text-lg">
            Already have a account?
            <NuxtLink to="/auth/login" class="link duration-200 font-semibold hover:link-secondary hover:underline">
                Log in
            </NuxtLink>
        </div>
        
        
    </div>
</form>
<modal ref="emailConfirmationSentModalRef">
    <email-confirmation-sent-component :confirmationEmail="email"></email-confirmation-sent-component>
</modal>
</template>

<script setup>
import { useUserStore } from '~/stores/user';
import { useThemeStore } from '~/stores/theme';
import { useToast } from 'vue-toastification';

import Modal from '~/components/Modal.vue';

const EmailConfirmationSentComponent = defineAsyncComponent({
    loader: () => import('~/components/EmailConfirmationSent.vue')
});

const config = useRuntimeConfig()

const userStore = useUserStore()
const themeStore = useThemeStore()

const registerAPIUrl = config.public.apiHost + config.public.registerAPIEndpoint

let isPasswordVisible = ref(false)
let passwordType = ref("password")
let passwordMinLength = 10
let passwordMaxLength = 100

const first_name = ref(null)
const last_name = ref(null)
const username = ref(null)
const email = ref(null)
const password = ref(null)
const password_confirmation = ref(null)

const maxUsernameLength = 50
const usernamePattern = "[A-Za-z0-9_\\-]+"

const toast = useToast();

const emailConfirmationSentModalRef = ref(null)

function openEmailConfirmationSentModal() {
    if(emailConfirmationSentModalRef.value) {
        emailConfirmationSentModalRef.value.toggleComponentModal()
    }
}

async function handleUserRegistration() {
    let userData = {
        'first_name': first_name.value,
        'last_name': last_name.value,
        'username': username.value,
        'email': email.value,
        'password1': password.value,
        'password2': password_confirmation.value
    }

    await userStore.registerUser(userData)

    if(userStore.error) {
        return;
    }

    openEmailConfirmationSentModal()

    toast.success('Registration completed successfully')
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

onBeforeMount(() => {
    userStore.clearError();
})

onBeforeUnmount(() => {
    userStore.clearError();
});
</script>