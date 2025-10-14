<template>
    <form @submit.prevent="handleUserUpdate" class="space-y-6">
        <!-- Name Fields -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="form-control">
                <label for="first_name" class="label">
                    <span class="label-text font-medium">First Name</span>
                </label>
                <input id="first_name" v-model="first_name" type="text" name="first_name" placeholder="John"
                    class="input  w-full focus:input-primary" required>
            </div>
            <div class="form-control">
                <label for="last_name" class="label">
                    <span class="label-text font-medium">Last Name</span>
                </label>
                <input id="last_name" v-model="last_name" type="text" name="last_name" placeholder="Snow"
                    class="input  w-full focus:input-primary" required>
            </div>
        </div>

        <!-- Username Field -->
        <div class="form-control">
            <label for="username" class="label">
                <span class="label-text font-medium">Username</span>
                <span class="label-text-alt">
                    <div class="tooltip tooltip-left"
                        data-tip="Only letters, numbers, hyphens, and underscores allowed">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor"
                            class="w-4 h-4 opacity-70 hover:opacity-100 transition-opacity cursor-help"
                            viewBox="0 0 16 16">
                            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16" />
                            <path
                                d="M5.255 5.786a.237.237 0 0 0 .241.247h.825c.138 0 .248-.113.266-.25.09-.656.54-1.134 1.342-1.134.686 0 1.314.343 1.314 1.168 0 .635-.374.927-.965 1.371-.673.489-1.206 1.06-1.168 1.987l.003.217a.25.25 0 0 0 .25.246h.811a.25.25 0 0 0 .25-.25v-.105c0-.718.273-.927 1.01-1.486.609-.463 1.244-.977 1.244-2.056 0-1.511-1.276-2.241-2.673-2.241-1.267 0-2.655.59-2.75 2.286m1.557 5.763c0 .533.425.927 1.01.927.609 0 1.028-.394 1.028-.927 0-.552-.42-.94-1.029-.94-.584 0-1.009.388-1.009.94" />
                        </svg>
                    </div>
                </span>
            </label>
            <input id="username" v-model.lazy="username" :maxlength="maxUsernameLength" :pattern="usernamePattern"
                @input="clearCustomMessage" @invalid="setCustomMessage" type="text" name="username"
                placeholder="john_snow" class="input  w-full focus:input-primary"
                :class="{ 'input-error': usernameError }" required>
            <label v-if="usernameError" class="label">
                <span class="label-text-alt text-error">{{ usernameError }}</span>
            </label>
        </div>

        <!-- Email Field -->
        <div class="form-control">
            <label for="email" class="label">
                <span class="label-text font-medium">Email</span>
            </label>
            <input id="email" v-model="email" type="email" name="email" placeholder="john.snow@gmail.com"
                class="input  w-full focus:input-primary" disabled required>
        </div>

        <!-- Error Message -->
        <div v-if="updateError" class="alert alert-error">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none"
                viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ updateError }}</span>
        </div>

        <!-- Success Message -->
        <div v-if="updateSuccess" class="alert alert-success">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none"
                viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Profile updated successfully!</span>
        </div>

        <!-- Submit Button -->
        <div class="form-control mt-6">
            <button type="submit" class="btn btn-primary btn-lg w-full" :class="{ 'loading': isLoading }"
                :disabled="isLoading">
                <span v-if="!isLoading">Update Profile</span>
                <span v-else>Updating...</span>
            </button>
        </div>
    </form>
</template>

<script setup>
import { useUserStore } from '~/stores/user'

const config = useRuntimeConfig()
const userStore = useUserStore()

const first_name = ref('')
const last_name = ref('')
const username = ref('')
const email = ref('')

const usernameError = ref('')
const updateError = ref('')
const updateSuccess = ref(false)
const isLoading = ref(false)

const maxUsernameLength = 50
const usernamePattern = "[A-Za-z0-9_\\-]+"

// Load current user data
onMounted(() => {
    if (userStore.user) {
        first_name.value = userStore.user.first_name || ''
        last_name.value = userStore.user.last_name || ''
        username.value = userStore.user.username || ''
        email.value = userStore.user.email || ''
    }
})

async function handleUserUpdate() {
    updateError.value = ''
    updateSuccess.value = false
    isLoading.value = true

    try {
        const userData = {
            first_name: first_name.value,
            last_name: last_name.value,
            username: username.value,
            email: email.value
        }

        await userStore.updateUser(userData)

        if (userStore.error) {
            updateError.value = userStore.error
        } else {
            updateSuccess.value = true
            setTimeout(() => {
                updateSuccess.value = false
            }, 3000)
        }
    } catch (error) {
        updateError.value = 'An unexpected error occurred'
    } finally {
        isLoading.value = false
    }
}

function clearCustomMessage(e) {
    e.target.setCustomValidity("")
    usernameError.value = ''
}

function setCustomMessage(e) {
    const usernameNotAllowedPattern = /[^A-Za-z0-9_\-]/g
    const matches = [...username.value.matchAll(usernameNotAllowedPattern)].map((x) => x[0])

    if (matches.length > 0) {
        const chars = [...new Set(matches)].join(', ')
        usernameError.value = matches.length === 1
            ? `The character "${chars}" is not allowed`
            : `The characters "${chars}" are not allowed`

        e.target.setCustomValidity(usernameError.value)
    } else {
        e.target.setCustomValidity("")
        usernameError.value = ''
    }
}
</script>