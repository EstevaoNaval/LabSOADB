<template>
</template>

<script setup>
    import { onBeforeMount } from 'vue';
    import { useRouter, useRoute } from 'vue-router'
    
    
    function refresh() {
        const route = useRoute();
        const router = useRouter()

        const redirectPage = route.query.redirect

        console.log(redirectPage)

        router.push({
            path: redirectPage
        })
    }

    onBeforeMount(() => {
        console.log("Cheguei aqui")
        refresh()
    })
    
</script>