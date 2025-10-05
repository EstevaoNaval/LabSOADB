<template>
</template>

<script setup>
    import { onMounted } from 'vue';
    import { useRouter, useRoute } from 'vue-router'
    
    
    function refresh() {
        const route = useRoute();
        const router = useRouter()

        const redirectPage = route.query.redirect

        console.log(redirectPage)
        console.log(route.query)

        router.replace({
            path: redirectPage
        })
    }

    onMounted(() => {
        refresh()
    })
    
</script>