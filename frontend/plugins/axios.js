import qs from 'qs';
import axios from 'axios';

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig();
  const isServer = process.server;

  // Log completo da configuração
  console.log('=== AXIOS PLUGIN DEBUG ===');
  console.log('isServer:', isServer);
  console.log('NODE_ENV:', process.env.NODE_ENV);
  console.log('config.public.apiHost:', config.public.apiHost);
  console.log('config.public.apiHostServer:', config.public.apiHostServer);

  const baseURL = isServer
    ? (config.public.apiHostServer || 'http://django-api:8000')
    : (config.public.apiHost || '');

  console.log('baseURL escolhido:', baseURL);
  console.log('========================');

  const instance = axios.create({
    baseURL: baseURL,
    paramsSerializer: (params) => {
      return qs.stringify(params, { arrayFormat: 'repeat' });
    },
  });

  instance.interceptors.request.use(
    (config) => {
      console.log('📤 Request:', {
        isServer,
        method: config.method,
        baseURL: config.baseURL,
        url: config.url,
        fullURL: `${config.baseURL}${config.url}`
      });
      return config;
    },
    (error) => Promise.reject(error)
  );

  instance.interceptors.response.use(
    (response) => {
      console.log('✅ Response:', response.config.url, response.status);
      return response;
    },
    (error) => {
      console.error('❌ Axios error:', {
        message: error.message,
        url: error.config?.url,
        baseURL: error.config?.baseURL,
        fullURL: `${error.config?.baseURL}${error.config?.url}`,
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