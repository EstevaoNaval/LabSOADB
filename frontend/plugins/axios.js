import qs from 'qs';
import axios from 'axios';

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig();

  // Detectar se está no servidor (SSR) ou no cliente (browser)
  const isServer = process.server;

  // No servidor usa URL interna do Docker, no cliente usa proxy relativo
  const baseURL = isServer
    ? config.public.apiHostServer  // http://django-api:8000
    : config.public.apiHost;        // '' (vazio = usa proxy)

  const instance = axios.create({
    baseURL: baseURL,
    paramsSerializer: (params) => {
      return qs.stringify(params, { arrayFormat: 'repeat' });
    },
  });

  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      console.error('Axios error:', error.message, {
        url: error.config?.url,
        baseURL: error.config?.baseURL,
        isServer
      });
      return Promise.reject(error);
    }
  );

  return {
    provide: {
      axios: instance,
    },
  };
});