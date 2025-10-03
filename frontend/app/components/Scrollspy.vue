<template>
  <div :class="props.scrollspyContainer">
    <slot></slot>
    <ul :class="props.scrollspyList">
      <li
        v-for="section in props.sections"
        :key="section.id"
        :class="[activeSection?.value === section.id ? props.sectionActive : '', props.scrollspyItem, 'cursor-pointer']"
        @click="scrollToSection(section.id)"
      >
        {{ section.label }}
      </li>
    </ul>
  </div>
</template>

<script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import debounce from 'lodash/debounce';

  const props = defineProps({
    sections: {
      type: Array,
      required: true,
    },
    scrollspyContainer: {
      type: String,
      default: ''
    },
    scrollspyList: {
      type: String,
      default: ''
    },
    scrollspyItem: {
      type: String,
      default: ''
    },
    sectionActive: {
      type: String,
      default: 'text-secondary font-bold border-secondary rounded-sm border-l-4'
    }
  });

  const activeSection = ref(null);

  const scrollToSection = (id) => {
    const section = document.getElementById(id);
    if (section) {
      window.scrollTo({
        top: section.offsetTop,
        behavior: 'smooth',
      });
    }
  };

  const onScroll = debounce(() => {
    const scrollPosition = window.scrollY + window.innerHeight / 2;
    const sectionsElements = props.sections.map((section) => document.getElementById(section.id));

    for (const section of sectionsElements) {
      if (
        section.offsetTop <= scrollPosition &&
        section.offsetTop + section.offsetHeight > scrollPosition
      ) {
        activeSection.value = section.id;
        break;
      }
    }
  }, 100);

  onMounted(() => {
    window.addEventListener('scroll', onScroll);
    
    onScroll();
  });

  onBeforeUnmount(() => {
    window.removeEventListener('scroll', onScroll);
  });
</script>