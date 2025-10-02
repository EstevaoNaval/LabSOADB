<template>
    <dialog v-if="isOpen" ref="drawStructureModal" class="modal">
        <div class="modal-box p-4 rounded-3xl m-auto max-w-3xl">
            <slot v-if="isComponentModelOpened"></slot>
        </div>
        <form method="dialog" class="modal-backdrop">
            <button @click="toggleComponentModal()">close</button>
        </form>
    </dialog>
</template>

<script setup>
import { ref } from 'vue';

const isOpen = ref(true)
var isComponentModelOpened = ref(false)
var drawStructureModal = ref(null)

const toggleComponentModal = () => {
    isComponentModelOpened.value = !isComponentModelOpened.value

    if (isComponentModelOpened.value) {
        drawStructureModal.value.showModal()
    } 
}

const closeModal = () => {
    isOpen.value = false
    drawStructureModal.value.close()
}

provide('closeModal', closeModal)

defineExpose({
    toggleComponentModal
})
</script>