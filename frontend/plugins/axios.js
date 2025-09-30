import qs from 'qs';
import axios from 'axios';

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig();

  const instance = axios.create({
    baseURL: config.public.apiHost || '',  // Fallback to empty if undefined
    paramsSerializer: (params) => {
      return qs.stringify(params, { arrayFormat: 'repeat' });
    },
  });

  // Optional: Global error handler for debugging
  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      console.error('Axios error:', error.message, { url: error.config?.url });
      return Promise.reject(error);
    }
  );

  return {
    provide: {
      axios: instance,
    },
  };
});