<template>
  <main class="flex flex-col items-center justify-center min-h-[400px] px-4 py-8">
    <!-- Icon with subtle animation -->
    <div class="relative mb-6">
      <div class="absolute inset-0 bg-primary/10 rounded-full blur-2xl animate-pulse"></div>
      <div class="relative bg-base-200 rounded-full p-6">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="size-16 md:size-20 text-primary">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
        </svg>
      </div>
    </div>

    <!-- Content -->
    <div class="text-center max-w-md space-y-3 mb-8">
      <h2 class="text-2xl md:text-3xl font-bold text-base-content">
        Authentication Required
      </h2>
      <p class="text-base md:text-lg text-base-content/70 leading-relaxed">
        Please sign in to access <span class="font-semibold text-primary">{{ props.loginRequiredTo }}</span>
      </p>
    </div>

    <!-- Action buttons -->
    <div class="flex flex-col sm:flex-row gap-3 w-full max-w-sm">
      <NuxtLink to="/auth/login" @click="goToLogin"
        class="btn btn-primary sm:flex-1 gap-2 text-base md:text-lg h-12 md:h-14">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
          class="size-5">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15m3-3 3 3m0 0-3 3m3-3H9" />
        </svg>
        Sign In
      </NuxtLink>

      <button @click="closeModal" class="btn btn-ghost sm:flex-1 text-base md:text-lg h-12 md:h-14">
        Cancel
      </button>
    </div>

    <!-- Optional: Additional help text -->
    <p class="text-sm text-base-content/50 mt-6 text-center">
      Don't have an account?
      <NuxtLink to="/auth/register" class="link link-primary font-medium" @click="closeModal">
        Sign up
      </NuxtLink>
    </p>
  </main>
</template>

<script setup>
const props = defineProps({
  loginRequiredTo: {
    type: String,
    required: true
  }
})

const closeModal = inject('closeModal')

const goToLogin = () => {
  closeModal()
  navigateTo('/auth/login')
}
</script>