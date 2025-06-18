import { createApp } from 'vue';
// @ts-ignore
import CKEditor from '@ckeditor/ckeditor5-vue';
import App from './App.vue';
import router from './router';

import '@/assets/css/vendor.min.css';
import '@/assets/css/theme.css';
import { createPinia } from 'pinia';
import piniaPersist from 'pinia-plugin-persist';
import LoadScript from '@/utils/standaloneImport';

// Sweetalert2
import VueSweetalert2 from 'vue-sweetalert2';

const app = createApp(App);

// Object.values(import.meta.glob('/src/modules/*.ts', { eager: true })).forEach(module => module.install?.(app));
const pinia = createPinia();
pinia.use(piniaPersist);
app.use(router);
app.use(CKEditor);
app.use(
  pinia.use(({ store }) => {
    store.router = router;
  }),
);
app.use(VueSweetalert2);
app.use(LoadScript);

// 환경 변수에 따라 타이틀 설정
document.title = import.meta.env.VITE_APP_TITLE;

//@ts-ignore
Kakao.init('d833a1f57334b2b11635ede9110e0791');
app.mount('#app');
