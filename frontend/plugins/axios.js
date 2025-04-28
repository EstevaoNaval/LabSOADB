import qs from 'qs';

import axios from 'axios';

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  const instance = axios.create({
    baseURL: config.public.apiHost,
    paramsSerializer: (params) => {
      return qs.stringify(params, { arrayFormat: 'repeat' });
    },
  });

  return {
    provide: {
      axios: instance,
    },
  };
});