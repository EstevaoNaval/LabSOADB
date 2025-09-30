export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig();

  const isServer = process.server;

  // Se tiver apiHost definido, usa ele (para client-side via proxy)
  // Se não, e estiver no servidor, usa apiHostServer (SSR interno)
  const baseURL = !isServer && config.public.apiHost
    ? config.public.apiHost
    : isServer
      ? config.public.apiHostServer
      : '';

  const instance = axios.create({
    baseURL: baseURL,
    paramsSerializer: (params) => {
      return qs.stringify(params, { arrayFormat: 'repeat' });
    },
  });

  // Log para debug
  console.log('[Axios Plugin]', {
    isServer,
    baseURL,
    apiHost: config.public.apiHost,
    apiHostServer: config.public.apiHostServer
  });

  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      console.error('Axios error:', error.message, {
        url: error.config?.url,
        baseURL: error.config?.baseURL,
        fullURL: error.config?.baseURL + error.config?.url
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