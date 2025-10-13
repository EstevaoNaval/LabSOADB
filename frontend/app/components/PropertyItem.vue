<template>
    <div class="flex flex-col items-center text-center p-2 bg-base-200 rounded-lg">
      <div class="flex items-center gap-1 mb-1 text-base-content/70">
        <slot name="icon"></slot>
        <span class="text-xs font-medium">{{ props.label }}</span>
      </div>
      <p v-if="props.isHtml" class="text-sm font-bold" v-html="props.value"></p>
      <p v-else class="text-sm font-bold">{{ props.value }}</p>
    </div>
</template>

<script setup>
    const props = defineProps({
        label: String,
        value: String,
        isHtml: Boolean
    }) 
</script>