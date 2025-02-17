<template>
    <dialog ref="drawStructureModal" class="modal">
        <div class="modal-box p-4 rounded-3xl m-auto max-w-3xl">
            <slot @closeModal="closeModal" v-if="isComponentModelOpened"></slot>
        </div>
        <form method="dialog" class="modal-backdrop">
            <button @click="toggleComponentModal()">close</button>
        </form>
    </dialog>
</template>

<script setup>
import { ref } from 'vue';

var isComponentModelOpened = ref(false)
var drawStructureModal = ref(null)

const toggleComponentModal = () => {
    isComponentModelOpened.value = !isComponentModelOpened.value

    if (isComponentModelOpened.value) {
        drawStructureModal.value.showModal()
    } 
}

const closeModal = () => {
    drawStructureModal.value.close()
}

defineExpose({
    toggleComponentModal
})
</script>