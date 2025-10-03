import { useThemeStore } from '~/stores/theme';

export default defineNuxtPlugin(() => {
    const themeStore = useThemeStore();
    
    if (process.client) {
      themeStore.initializeTheme();
    }
  });