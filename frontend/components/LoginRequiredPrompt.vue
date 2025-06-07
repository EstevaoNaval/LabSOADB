<template>
    <main>
        <div class="space-y-6 text-center p-4 hidden md:flex md:flex-col">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="mx-auto size-28">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
            </svg>

            <h2 class="text-4xl font-semibold">Login Required</h2>
            <div class="text-xl">
              <p>
                You need to be logged in to use {{ props.loginRequiredTo }}.
              </p>
              <p>
                Please, click on the button below to be redirected to the login page.
              </p>
            </div>
            <div class="divider w-3/4 mx-auto"></div>
        </div>

        <div class="space-y-6 text-center p-4 flex flex-col md:hidden">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="mx-auto size-20">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
            </svg>
            <h2 class="text-3xl font-semibold">Login Required</h2>
            <div class="text-lg space-y-4">
                <p>
                  You need to be logged in to use {{ props.loginRequiredTo }}.
                </p>
            </div>
            <div class="divider w-5/6 mx-auto"></div>
        </div>
        <div class="modal-action">
          <form method="dialog" class="flex flex-col sm:flex-row gap-3 w-full max-w-sm mx-auto">
            <button class="btn btn-ghost order-2 text-lg md:text-xl sm:order-1 flex-1 transition-all duration-200">
              Cancel
            </button>
            <NuxtLink 
              to="/auth/login"
              @click="goToLogin" 
              class="btn btn-primary order-1 text-lg md:text-xl sm:order-2  flex-1 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 md:size-8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75" />
              </svg>

              Log In
            </NuxtLink>
          </form>
        </div>
    </main>
</template>

<script setup>
const props = defineProps({
    loginRequiredTo:  {
      type: String,
      required: true
    },
})

const emit = defineEmits(['close']);

const goToLogin = () => {
  emit('close');
  navigateTo('/auth/login');
};
</script>


