export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.directive('close-details', {
    mounted(el) {
      const closeDetails = () => {
        el.open = false;
        
        const checkbox = el.querySelector('summary input[type="checkbox"]');
        
        if (checkbox) {
          checkbox.checked = false;
        }
      };

      if (nuxtApp.$router) {
        nuxtApp.$router.afterEach(() => {
          closeDetails();
        });
      } else {
        console.warn('Router not available');
      }

      el.__closeDetails__ = closeDetails;
    },
    unmounted(el) {
      if (el.__closeDetails__) {
        el.__closeDetails__();
      }
    }
  });
});
