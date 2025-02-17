<template>
<div class="grid lg:grid-cols-2">
    
    <div class="w-full flex flex-col pt-4 items-center md:justify-center gap-8">
        <p class="text-4xl font-bold hidden md:flex">
            Update Profile Information
        </p>
        <p class="text-3xl font-bold md:hidden">
            Update Profile Information
        </p>
        <div class="mx-auto rounded-lg p-8 w-[90%] lg:w-3/4 max-w-md items-center bg-base-300">
            <update-user-form></update-user-form>
        </div>
    </div>
    <div class="w-full flex flex-col pt-4 items-center md:justify-center gap-8">
        <p class="text-4xl font-bold hidden md:flex">
            Update Password
        </p>
        <p class="text-3xl font-bold md:hidden">
            Update Password
        </p>
        <div class="mx-auto rounded-lg p-8 w-[90%] lg:w-3/4 max-w-md items-center bg-base-300">
            <update-password-form></update-password-form>
        </div>
    </div>
</div>

</template>

<script setup>
import UpdateUserForm from '~/components/UpdateUserForm.vue'
import UpdatePasswordForm from '~/components/UpdatePasswordForm.vue'
import { useThemeStore } from '~/stores/theme';

const themeStore = useThemeStore()
</script>

<style>

</style>