import { defineStore } from 'pinia';

export const useThemeStore = defineStore('theme', {
  state: () => ({
    darkMode: true,
    theme: process.client ? document.documentElement.getAttribute('data-theme') || 'night' : 'night',
  }),
  actions: {
    initializeTheme() {
      if (process.client) {
        const userPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        this.setDarkMode(userPrefersDark);
      }
    },  
    setDarkMode(value) {
      this.darkMode = value;
      this.setTheme(value ? 'night' : 'winter');
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      
      if(this.darkMode) {
        this.setTheme('night')
      }else{
        this.setTheme('winter')
      }
    },
    setTheme(theme) {
      this.theme = theme;
      if (process.client) {
        document.documentElement.setAttribute('data-theme', theme);
      }
    },
  },
  getters: {
    currentTheme: (state) => state.theme,
    isDarkMode: (state) => state.darkMode
  },
  persist: true,
});
