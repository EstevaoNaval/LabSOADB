<template>
    <form
        :action="registerAPIUrl" 
        @submit.prevent="handleUserRegistration"
    >
        <div class="mb-6 grid grid-cols-2 gap-4">
            <div class="flex flex-col">
                <div class="text-md font-bold mb-2" for="first_name">
                    First Name
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
            </div>
            <div class="flex flex-col">
                <div class="text-md font-bold mb-2" for="last_name">
                    Last Name
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
            </div>
        </div>
        <div class="mb-6">
            <div class="text-md mb-2 flex gap-1" for="username">
                <p class="font-bold">User Name</p>
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
        </div>
        <div class="mb-10">
            <div class="text-md font-bold mb-2" for="email">
                Email
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