<!-- components/Scrollspy.vue - if you need to create/update it -->
<template>
  <ul :class="scrollspyList">
    <li 
      v-for="section in sections" 
      :key="section.id"
      :class="[
        scrollspyItem,
        { 'border-l-4 border-primary font-bold bg-base-200': activeSection === section.id }
      ]"
    >
      <a 
        :href="`#${section.id}`"
        @click.prevent="scrollToSection(section.id)"
        class="block px-3 py-2"
      >
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
  }
})

const emit = defineEmits(['click'])

const activeSection = ref('')

const scrollToSection = (id) => {
  const element = document.getElementById(id)
  if (element) {
    const offset = 80 // Offset for sticky header
    const elementPosition = element.getBoundingClientRect().top
    const offsetPosition = elementPosition + window.pageYOffset - offset

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    })
  }
  emit('click')
}

const handleScroll = () => {
  const scrollPosition = window.scrollY + 100

  for (const section of props.sections) {
    const element = document.getElementById(section.id)
    if (element) {
      const offsetTop = element.offsetTop
      const offsetBottom = offsetTop + element.offsetHeight

      if (scrollPosition >= offsetTop && scrollPosition < offsetBottom) {
        activeSection.value = section.id
        break
      }
    }
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll() // Initial check
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>