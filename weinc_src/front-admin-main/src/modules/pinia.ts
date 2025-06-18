import type { Router } from 'vue-router';
import { createPinia } from 'pinia';
import { useRouter } from 'vue-router';

declare module 'pinia' {
  export interface PiniaCustomProperties {
    router: Router;
  }
}

export const install = (app: any) => {
  const pinia = createPinia();
  pinia.use(({ store }) => {
    store.router = useRouter();
  });

  app.use(pinia);
};
