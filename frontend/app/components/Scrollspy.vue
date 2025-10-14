<!-- components/Scrollspy.vue -->
<template>
  <ul :class="scrollspyList">
    <li v-for="section in sections" :key="section.id" :class="[
      scrollspyItem,
      { 'border-l-4 border-primary font-bold bg-base-200': activeSection === section.id }
    ]">
      <a :href="`#${section.id}`" @click.prevent="scrollToSection(section.id)" class="block px-3 py-2">
        {{ section.label }}
      </a>
    </li>
  </ul>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  sections: {
    type: Array,
    required: true
  },
  scrollspyList: {
    type: String,
    default: ''
  },
  scrollspyItem: {
    type: String,
    default: ''
  },
  offset: {
    type: Number,
    default: 80
  }
})

const emit = defineEmits(['click'])

const activeSection = ref('')

const scrollToSection = (id) => {
  // Emit click first to close the menu
  emit('click')

  // Use setTimeout to allow the menu to collapse before calculating position
  setTimeout(() => {
    const element = document.getElementById(id)
    if (element) {
      // Get the actual header height dynamically
      const tableOfContents = document.querySelector('.table-of-contents')
      const headerOffset = tableOfContents ? tableOfContents.offsetHeight : props.offset

      const elementPosition = element.getBoundingClientRect().top
      const offsetPosition = elementPosition + window.scrollY - headerOffset

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      })
    }
  }, 300) // Wait for collapse animation to complete
}

const handleScroll = () => {
  // Get dynamic offset based on current header height
  const tableOfContents = document.querySelector('.table-of-contents')
  const headerOffset = tableOfContents ? tableOfContents.offsetHeight : props.offset
  const scrollPosition = window.scrollY + headerOffset + 20

  let current = ''

  for (let i = props.sections.length - 1; i >= 0; i--) {
    const section = props.sections[i]
    const element = document.getElementById(section.id)

    if (element && element.offsetTop <= scrollPosition) {
      current = section.id
      break
    }
  }

  activeSection.value = current
}

let scrollTimeout = null

const throttledHandleScroll = () => {
  if (scrollTimeout) return

  scrollTimeout = setTimeout(() => {
    handleScroll()
    scrollTimeout = null
  }, 100)
}

onMounted(() => {
  window.addEventListener('scroll', throttledHandleScroll, { passive: true })
  handleScroll() // Initial check
})

onUnmounted(() => {
  window.removeEventListener('scroll', throttledHandleScroll)
  if (scrollTimeout) {
    clearTimeout(scrollTimeout)
  }
})
</script>