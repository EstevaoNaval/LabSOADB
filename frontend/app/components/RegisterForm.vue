<template>
    <main>
        <form @submit.prevent="handleUserRegistration" class="space-y-6">
            <!-- Global Error Alerts -->
            <div v-if="userStore.error?.connection" class="alert alert-error">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{{ userStore.error.connection }}</span>
            </div>

            <div v-if="userStore.error?.non_field_errors" class="alert alert-error">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div class="flex flex-col gap-1">
                    <span v-for="(error, index) in userStore.error.non_field_errors" :key="index">{{ error }}</span>
                </div>
            </div>

            <!-- Name Fields -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div class="form-control">
                    <label for="first_name" class="label justify-start px-0">
                        <span class="label-text font-medium">First Name</span>
                        <span class="label-text text-error ml-1">*</span>
                    </label>
                    <input id="first_name" v-model="first_name" type="text" name="first_name" placeholder="John"
                        class="input  w-full focus:input-primary"
                        :class="{ 'input-error': userStore.error?.first_name }" required>
                    <label v-if="userStore.error?.first_name" class="label px-0">
                        <span class="label-text-alt text-error">{{ userStore.error.first_name[0] }}</span>
                    </label>
                </div>

                <div class="form-control">
                    <label for="last_name" class="label justify-start px-0">
                        <span class="label-text font-medium">Last Name</span>
                        <span class="label-text text-error ml-1">*</span>
                    </label>
                    <input id="last_name" v-model="last_name" type="text" name="last_name" placeholder="Snow"
                        class="input  w-full focus:input-primary" :class="{ 'input-error': userStore.error?.last_name }"
                        required>
                    <label v-if="userStore.error?.last_name" class="label px-0">
                        <span class="label-text-alt text-error">{{ userStore.error.last_name[0] }}</span>
                    </label>
                </div>
            </div>

            <!-- Username Field -->
            <div class="form-control">
                <label for="username" class="label justify-start px-0">
                    <span class="label-text font-medium">Username</span>
                    <span class="label-text text-error ml-1">*</span>
                    <span class="label-text-alt ml-auto">
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
                    :class="{ 'input-error': userStore.error?.username || usernameError }" required>
                <label v-if="usernameError || userStore.error?.username" class="label px-0">
                    <span class="label-text-alt text-error">
                        {{ usernameError || userStore.error.username[0] }}
                    </span>
                </label>
            </div>

            <!-- Email Field -->
            <div class="form-control">
                <label for="email" class="label justify-start px-0">
                    <span class="label-text font-medium">Email</span>
                    <span class="label-text text-error ml-1">*</span>
                </label>
                <input id="email" v-model="email" type="email" name="email" placeholder="john.snow@gmail.com"
                    autocomplete="email" class="input  w-full focus:input-primary"
                    :class="{ 'input-error': userStore.error?.email }" required>
                <label v-if="userStore.error?.email" class="label px-0">
                    <span class="label-text-alt text-error">
                        {{ Array.isArray(userStore.error.email) ? userStore.error.email[0] : userStore.error.email }}
                    </span>
                </label>
            </div>

            <!-- Password Field -->
            <div class="form-control">
                <label for="password" class="label justify-start px-0">
                    <span class="label-text font-medium">Password</span>
                    <span class="label-text text-error ml-1">*</span>
                    <span class="label-text-alt ml-auto text-xs">Min. {{ passwordMinLength }} characters</span>
                </label>
                <div class="relative">
                    <input id="password" v-model="password" :type="showPassword ? 'text' : 'password'" name="password"
                        placeholder="Create a strong password" autocomplete="new-password"
                        :minlength="passwordMinLength" :maxlength="passwordMaxLength"
                        class="input  w-full pr-12 focus:input-primary" :class="{
                            'input-error': userStore.error?.password1,
                            'input-success': passwordStrength === 'strong' && password.length >= passwordMinLength
                        }" @input="validatePasswordStrength" required>
                    <button type="button"
                        class="absolute inset-y-0 right-0 flex items-center pr-3 hover:text-primary transition-colors"
                        @click="showPassword = !showPassword" tabindex="-1" aria-label="Toggle password visibility">
                        <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                            stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                            stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                        </svg>
                    </button>
                </div>

                <!-- Password Strength Indicator -->
                <div v-if="password.length > 0" class="mt-2">
                    <div class="grid grid-cols-3 gap-1 mb-1">
                        <div class="h-1 flex-1 rounded-full transition-all"
                            v-if="passwordStrength === 'weak' || passwordStrength === 'medium' || passwordStrength === 'strong'"
                            :class="{
                                'bg-error': passwordStrength === 'weak',
                                'bg-warning': passwordStrength === 'medium',
                                'bg-success': passwordStrength === 'strong'
                            }"></div>
                        <div class="h-1 flex-1 rounded-full transition-all"
                            v-if="passwordStrength === 'medium' || passwordStrength === 'strong'" :class="{
                                'bg-error': passwordStrength === 'weak',
                                'bg-warning': passwordStrength === 'medium',
                                'bg-success': passwordStrength === 'strong'
                            }"></div>
                        <div class="h-1 flex-1 rounded-full transition-all" v-if="passwordStrength === 'strong'" :class="{
                            'bg-error': passwordStrength === 'weak',
                            'bg-warning': passwordStrength === 'medium',
                            'bg-success': passwordStrength === 'strong'
                        }"></div>
                    </div>
                    <p class="text-xs" :class="{
                        'text-error': passwordStrength === 'weak',
                        'text-warning': passwordStrength === 'medium',
                        'text-success': passwordStrength === 'strong'
                    }">
                        Password strength: {{ passwordStrength }}
                    </p>
                </div>

                <label v-if="userStore.error?.password1" class="label px-0">
                    <span class="label-text-alt text-error">
                        {{ Array.isArray(userStore.error.password1) ? userStore.error.password1[0] :
                            userStore.error.password1 }}
                    </span>
                </label>
            </div>

            <!-- Confirm Password Field -->
            <div class="form-control">
                <label for="password_confirmation" class="label justify-start px-0">
                    <span class="label-text font-medium">Confirm Password</span>
                    <span class="label-text text-error ml-1">*</span>
                </label>
                <div class="relative">
                    <input id="password_confirmation" v-model="password_confirmation"
                        :type="showConfirmPassword ? 'text' : 'password'" name="password_confirmation"
                        placeholder="Re-enter your password" autocomplete="new-password" :minlength="passwordMinLength"
                        :maxlength="passwordMaxLength" class="input  w-full pr-12 focus:input-primary" :class="{
                            'input-error': userStore.error?.password2 || passwordMismatch,
                            'input-success': password_confirmation && password === password_confirmation && password.length >= passwordMinLength
                        }" @input="checkPasswordMatch" required>
                    <button type="button"
                        class="absolute inset-y-0 right-0 flex items-center pr-3 hover:text-primary transition-colors"
                        @click="showConfirmPassword = !showConfirmPassword" tabindex="-1"
                        aria-label="Toggle password visibility">
                        <svg v-if="showConfirmPassword" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                            stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                        </svg>
                    </button>
                </div>
                <label v-if="passwordMismatch" class="label px-0">
                    <span class="label-text-alt text-error">Passwords do not match</span>
                </label>
                <label
                    v-else-if="password_confirmation && password === password_confirmation && password.length >= passwordMinLength"
                    class="label px-0">
                    <span class="label-text-alt text-success flex items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                        Passwords match
                    </span>
                </label>
                <label v-else-if="userStore.error?.password2" class="label px-0">
                    <span class="label-text-alt text-error">
                        {{ Array.isArray(userStore.error.password2) ? userStore.error.password2[0] :
                            userStore.error.password2 }}
                    </span>
                </label>
            </div>

            <!-- Age Confirmation -->
            <div class="form-control">
                <label class="label justify-start px-0 cursor-pointer gap-3">
                    <input v-model="ageConfirmed" type="checkbox" class="checkbox checkbox-primary" required />
                    <span class="label-text">I am over 18 years old</span>
                    <span class="label-text text-error">*</span>
                </label>
            </div>

            <!-- Submit Button -->
            <div class="form-control pt-2">
                <button type="submit" class="btn btn-primary btn-lg w-full gap-2" :disabled="isLoading || !isFormValid"
                    :class="{ 'loading': isLoading }">
                    <svg v-if="!isLoading" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                        stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
                    </svg>
                    <span v-if="!isLoading">Sign Up</span>
                    <span v-else>Creating Account...</span>
                </button>
            </div>

            <!-- Terms & Privacy -->
            <div class="text-center text-sm text-base-content/70 px-4">
                By clicking "Sign Up", you agree to LabSOADB's
                <a href="#" class="link link-hover hover:link-primary">Terms of Service</a>
                and acknowledge that our
                <a href="#" class="link link-hover hover:link-primary">Privacy Policy</a>
                applies to you.
            </div>

            <!-- Login Link -->
            <div class="text-center pt-2">
                <span class="text-base-content/70">Already have an account? </span>
                <NuxtLink to="/auth/login" class="link link-hover hover:link-primary font-semibold">
                    Log in
                </NuxtLink>
            </div>
        </form>

        <modal ref="emailConfirmationSentModalRef">
            <email-confirmation-sent-component :confirmationEmail="email"></email-confirmation-sent-component>
        </modal>
    </main>
</template>

<script setup>
import { useUserStore } from '~/stores/user'
import { useToast } from 'vue-toastification'
import Modal from '~/components/Modal.vue'

const EmailConfirmationSentComponent = defineAsyncComponent({
    loader: () => import('~/components/EmailConfirmationSent.vue')
})

const config = useRuntimeConfig()
const userStore = useUserStore()
const toast = useToast()

const first_name = ref('')
const last_name = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const password_confirmation = ref('')
const ageConfirmed = ref(false)

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isLoading = ref(false)

const passwordMinLength = 10
const passwordMaxLength = 100
const maxUsernameLength = 50
const usernamePattern = "[A-Za-z0-9_\\-]+"

const passwordStrength = ref('')
const usernameError = ref('')
const passwordMismatch = ref(false)

const emailConfirmationSentModalRef = ref(null)

const isFormValid = computed(() => {
    return first_name.value &&
        last_name.value &&
        username.value &&
        email.value &&
        password.value.length >= passwordMinLength &&
        password_confirmation.value === password.value &&
        ageConfirmed.value &&
        passwordStrength.value !== 'weak'
})

function validatePasswordStrength() {
    const pwd = password.value

    if (pwd.length < passwordMinLength) {
        passwordStrength.value = 'weak'
        return
    }

    let score = 0
    if (/[a-z]/.test(pwd)) score++
    if (/[A-Z]/.test(pwd)) score++
    if (/[0-9]/.test(pwd)) score++
    if (/[^a-zA-Z0-9]/.test(pwd)) score++
    if (pwd.length >= 16) score++

    if (score <= 2) {
        passwordStrength.value = 'weak'
    } else if (score === 3) {
        passwordStrength.value = 'medium'
    } else {
        passwordStrength.value = 'strong'
    }

    checkPasswordMatch()
}

function checkPasswordMatch() {
    if (password_confirmation.value) {
        passwordMismatch.value = password.value !== password_confirmation.value
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

function openEmailConfirmationSentModal() {
    if (emailConfirmationSentModalRef.value) {
        emailConfirmationSentModalRef.value.toggleComponentModal()
    }
}

async function handleUserRegistration() {
    userStore.clearError()
    isLoading.value = true

    try {
        const userData = {
            first_name: first_name.value,
            last_name: last_name.value,
            username: username.value,
            email: email.value,
            password1: password.value,
            password2: password_confirmation.value
        }

        await userStore.registerUser(userData)

        if (userStore.error) {
            return
        }

        openEmailConfirmationSentModal()
        toast.success('Registration completed successfully')
    } catch (error) {
        console.error('Registration error:', error)
    } finally {
        isLoading.value = false
    }
}

onBeforeMount(() => {
    userStore.clearError()
})

onBeforeUnmount(() => {
    userStore.clearError()
})
</script>