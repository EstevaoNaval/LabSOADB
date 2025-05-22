<template>
    <main>
        <div class="space-y-6 text-center p-4 hidden md:flex md:flex-col">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="mx-auto size-28">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
            </svg>

            <h2 class="text-4xl font-semibold">Login Required</h2>
            <div class="text-xl">
              <p>
                You need to be logged in to export the chemicals.
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
                  You need to be logged in to export the chemicals.
                </p>
                <p>
                  Please, click on the button below to be redirected to the login page.
                </p>
            </div>
            <div class="divider w-5/6 mx-auto"></div>
        </div>
        <div class="modal-action">
          <form method="dialog" class="flex gap-2">
            <button class="btn btn-ghost text-lg">Cancelar</button>
            <NuxtLink to="/auth/login" class="btn btn-primary text-lg">Fazer login</NuxtLink>
          </form>
        </div>
    </main>
</template>

<script setup>
const isLocked = ref(true)

function handleLockAnimation() {
  // Simulate login success (e.g., after valid credentials)
  isLocked.value = false;
  // Reset to locked after 2s for demo purposes
  setTimeout(() => {
    isLocked.value = true;
  }, 2000);
}

onMounted(() => {
  // Simula a transição automática após abrir o modal
  handleLockAnimation()
})
</script>

<style>

</style>