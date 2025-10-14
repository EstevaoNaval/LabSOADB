<template>
    <form @submit.prevent="handlePasswordUpdate" class="space-y-6">
        <!-- Current Password -->
        <div class="form-control">
            <label for="current_password" class="label">
                <span class="label-text font-medium">Current Password</span>
            </label>
            <div class="relative">
                <input id="current_password" v-model="currentPassword" :type="showCurrentPassword ? 'text' : 'password'"
                    name="current_password" placeholder="Enter current password"
                    class="input  w-full pr-12 focus:input-primary" :class="{ 'input-error': errors.currentPassword }"
                    required>
                <button type="button"
                    class="absolute inset-y-0 right-0 flex items-center pr-3 hover:text-primary transition-colors"
                    @click="showCurrentPassword = !showCurrentPassword" tabindex="-1">
                    <svg v-if="showCurrentPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                        stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-5 h-5">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>
                </button>
            </div>
            <label v-if="passwordComposable.state.error?.old_password" class="label px-0">
                <span class="label-text-alt text-error">
                    {{ Array.isArray(passwordComposable.state.error?.old_password) ?
                        passwordComposable.state.error?.old_password[0] : passwordComposable.state.error?.old_password }}
                </span>
            </label>
        </div>

        <div class="divider my-2"></div>

        <!-- New Password -->
        <div class="form-control">
            <label for="new_password" class="label">
                <span class="label-text font-medium">New Password</span>
                <span class="label-text-alt text-xs">Min. {{ passwordMinLength }} characters</span>
            </label>
            <div class="relative">
                <input id="new_password" v-model="newPassword" :type="showNewPassword ? 'text' : 'password'"
                    name="new_password" placeholder="Enter new password" :minlength="passwordMinLength"
                    :maxlength="passwordMaxLength" class="input  w-full pr-12 focus:input-primary"
                    :class="{ 'input-error': errors.newPassword, 'input-success': passwordStrength === 'strong' && newPassword.length >= passwordMinLength }"
                    @input="validatePasswordStrength" required>
                <button type="button"
                    class="absolute inset-y-0 right-0 flex items-center pr-3 hover:text-primary transition-colors"
                    @click="showNewPassword = !showNewPassword" tabindex="-1">
                    <svg v-if="showNewPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                        stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-5 h-5">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>
                </button>
            </div>

            <!-- Password Strength Indicator -->
            <div v-if="newPassword.length > 0" class="mt-2">
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

            <label v-if="errors.newPassword" class="label">
                <span class="label-text-alt text-error">{{ errors.newPassword }}</span>
            </label>
        </div>

        <!-- Confirm New Password -->
        <div class="form-control">
            <label for="confirm_password" class="label">
                <span class="label-text font-medium">Confirm New Password</span>
            </label>
            <div class="relative">
                <input id="confirm_password" v-model="confirmPassword" :type="showConfirmPassword ? 'text' : 'password'"
                    name="confirm_password" placeholder="Re-enter new password" :minlength="passwordMinLength"
                    :maxlength="passwordMaxLength" class="input  w-full pr-12 focus:input-primary" :class="{
                        'input-error': errors.confirmPassword,
                        'input-success': confirmPassword.length > 0 && newPassword === confirmPassword && newPassword.length >= passwordMinLength
                    }" @input="validatePasswordMatch" required>
                <button type="button"
                    class="absolute inset-y-0 right-0 flex items-center pr-3 hover:text-primary transition-colors"
                    @click="showConfirmPassword = !showConfirmPassword" tabindex="-1">
                    <svg v-if="showConfirmPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                        stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-5 h-5">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>
                </button>
            </div>
            <label v-if="errors.confirmPassword" class="label">
                <span class="label-text-alt text-error">{{ errors.confirmPassword }}</span>
            </label>
            <label
                v-else-if="confirmPassword.length > 0 && newPassword === confirmPassword && newPassword.length >= passwordMinLength"
                class="label">
                <span class="label-text-alt text-success flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    Passwords match
                </span>
            </label>
        </div>

        <!-- Error Alert -->
        <div v-if="updateError" class="alert alert-error">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none"
                viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ updateError }}</span>
        </div>

        <!-- Submit Button -->
        <div class="form-control mt-6">
            <button type="submit" class="btn btn-primary btn-lg w-full" :disabled="isLoading || !isFormValid"
                :class="{ 'loading': isLoading }">
                <span v-if="!isLoading">Change Password</span>
                <span v-else>Changing Password...</span>
            </button>
        </div>
    </form>
</template>

<script setup>
import { useToast } from 'vue-toastification'

import { usePassword } from '~/composables/usePassword'
import { useRouter } from 'vue-router'
import { useUserStore } from '~/stores/user'
import { useAuthStore } from '~/stores/auth'

const router = useRouter()

// stores
const authStore = useAuthStore()
const userStore = useUserStore()

// composables
const passwordComposable = usePassword()

const toast = useToast()

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const passwordMinLength = 12
const passwordMaxLength = 100

const passwordStrength = ref('')
const errors = ref({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
})

const updateError = ref('')
const isLoading = ref(false)

const isFormValid = computed(() => {
    return currentPassword.value.length >= passwordMinLength &&
        newPassword.value.length >= passwordMinLength &&
        confirmPassword.value.length >= passwordMinLength &&
        newPassword.value === confirmPassword.value &&
        passwordStrength.value !== 'weak'
})

function validatePasswordStrength() {
    errors.value.newPassword = ''
    const pwd = newPassword.value

    if (pwd.length < passwordMinLength) {
        passwordStrength.value = 'weak'
        return
    }

    let score = 0

    // Check for different character types
    if (/[a-z]/.test(pwd)) score++
    if (/[A-Z]/.test(pwd)) score++
    if (/[0-9]/.test(pwd)) score++
    if (/[^a-zA-Z0-9]/.test(pwd)) score++

    // Check length
    if (pwd.length >= 16) score++

    if (score <= 2) {
        passwordStrength.value = 'weak'
    } else if (score === 3) {
        passwordStrength.value = 'medium'
    } else {
        passwordStrength.value = 'strong'
    }

    // Validate match if confirm password is filled
    if (confirmPassword.value) {
        validatePasswordMatch()
    }
}

function validatePasswordMatch() {
    errors.value.confirmPassword = ''

    if (confirmPassword.value && newPassword.value !== confirmPassword.value) {
        errors.value.confirmPassword = 'Passwords do not match'
    }
}

async function handlePasswordUpdate() {
    // Reset states
    updateError.value = ''
    errors.value = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
    }

    // Validate
    if (newPassword.value !== confirmPassword.value) {
        errors.value.confirmPassword = 'Passwords do not match'
        return
    }

    if (newPassword.value.length < passwordMinLength) {
        errors.value.newPassword = `Password must be at least ${passwordMinLength} characters`
        return
    }

    if (passwordStrength.value === 'weak') {
        errors.value.newPassword = 'Password is too weak. Use a mix of letters, numbers, and symbols.'
        return
    }

    isLoading.value = true

    try {
        const passwordData = {
            old_password: currentPassword.value,
            new_password1: newPassword.value,
            new_password2: confirmPassword.value
        }

        console.log(passwordData)

        await passwordComposable.changePasword(passwordData)

        if (passwordComposable.state.error) {
            errors.value = {
                currentPassword: passwordComposable.state.error.old_password ? passwordComposable.state.error.old_password : '',
                newPassword: passwordComposable.state.error.new_password1 ? passwordComposable.state.error.new_password1 : '',
                confirmPassword: passwordComposable.state.error.new_password2 ? passwordComposable.state.error.new_password2 : ''
            }

            return
        }

        // Clear form
        currentPassword.value = ''
        newPassword.value = ''
        confirmPassword.value = ''
        passwordStrength.value = ''

        // clear errors
        errors.value = {
            currentPassword: '',
            newPassword: '',
            confirmPassword: ''
        }


        await authStore.logout()

        userStore.clearUserProfile()

        // Show toast before redirect
        toast.success('Password changed successfully!')

        await new Promise(resolve => setTimeout(resolve, 500))

        router.replace({
            path: '/home'
        })
    } catch (error) {
        updateError.value = 'An unexpected error occurred'
    } finally {
        isLoading.value = false
    }
}
</script>