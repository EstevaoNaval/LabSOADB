import AOS from 'aos';
import 'aos/dist/aos.css';

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.hook('app:mounted', () => {
        AOS.init({
            once: true, // Only animate once
            duration: 1200, // Default duration of animations
            easing: 'ease-in-out', // Default easing for animations
        });
    });
});