import { defineNuxtPlugin } from "nuxt/app";

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.provide('enter', (el) => {
        el.style.height = '0';
        el.style.overflow = 'hidden';
        el.style.transition = 'height 0.5s ease';
        requestAnimationFrame(() => {
          el.style.height = el.scrollHeight + 'px';
        });
    })

    nuxtApp.provide('afterEnter', (el) => {
        el.style.height = 'auto';
    })
    
    
    nuxtApp.provide('leave', (el) => {
        el.style.height = el.scrollHeight + 'px';
        el.style.overflow = 'hidden';
        requestAnimationFrame(() => {
          el.style.transition = 'height 0.5s ease';
          el.style.height = '0';
        });
    })
    
    nuxtApp.provide('afterLeave', (el) => {
        el.style.height = 'auto';
    })
})