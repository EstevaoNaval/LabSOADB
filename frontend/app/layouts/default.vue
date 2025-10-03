<template>
    <div>
        <Header></Header>
        <main>
            <slot />
        </main>
        <Footer></Footer>
    </div>
</template>

<script setup>
import Header from '~/components/Header.vue';
import Footer from '~/components/Footer.vue';
</script>