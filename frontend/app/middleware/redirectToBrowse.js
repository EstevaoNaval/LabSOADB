export default defineNuxtRouteMiddleware((to, from) => {
    if (to.path === '/chemicals') {
      return navigateTo('/chemicals/search');
    }
  });