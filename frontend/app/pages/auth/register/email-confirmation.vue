<template>
    <div class="hero min-h-screen email-confirmation-page-art-dark">
        <div class="hero-overlay bg-opacity-60 bg-base-200"></div>
        <div class="hero-content ">
            <div class="mx-auto rounded-lg items-center bg-base-300 p-16">
                <email-confirmation></email-confirmation>
            </div>
        </div>
    </div>
</template>

<script setup>
    import EmailConfirmation from "~/components/EmailConfirmation.vue";
</script>

<style setup>
    .email-confirmation-page-art-dark {
        background-image: url('~/assets/email_confirmation_background_dark.webp');
    }
</style>