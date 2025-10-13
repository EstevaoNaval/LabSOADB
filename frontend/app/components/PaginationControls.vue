<template>
    <div class="flex flex-col lg:flex-row items-center justify-between gap-4">
        <p class="text-sm text-base-content/70 order-2 lg:order-1">
            Showing {{ 1 + props.pagination.state.pageSize * (props.pagination.state.page - 1) }} 
            to {{ Math.min(props.pagination.state.pageSize * props.pagination.state.page, props.pagination.state.totalItems) }} 
            of {{ props.pagination.state.totalItems }} results
        </p>
        <div class="order-1 lg:order-2">
            <Pagination :pagination="pagination" />
        </div>
    </div>
</template>

<script setup>
    import Pagination from '~/components/Pagination.vue';

    const props = defineProps({
        pagination: {
          type: Object,
          required: true
        }
    })
</script>

<style>

</style>