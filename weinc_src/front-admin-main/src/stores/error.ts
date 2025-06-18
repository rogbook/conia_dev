import { defineStore } from 'pinia';
import { computed, reactive } from 'vue';
import router from '@/router';

export const useErrorStore = defineStore('ErrorStore', () => {
  const error = reactive({ message: '찾으시는 페이지가 없습니다.', statusCode: '404', show: false });

  const hasError = computed(() => error.show);

  const clearError = () => {
    error.message = '찾으시는 페이지가 없습니다.';
    error.statusCode = '404';
    error.show = false;
  };

  const setError = (message: string, statusCode: string) => {
    error.message = message;
    error.statusCode = statusCode;
    error.show = true;
    router.push('/error');
  };

  return { error, setError, hasError, clearError };
});
