import { ref } from 'vue';

export function useAsyncState(promise: Promise<any>, init: any) {
  const state = ref(init);
  const isReady = ref(false);
  const isLoading = ref(false);
  const error = ref();

  async function execute() {
    error.value = undefined;
    isReady.value = false;
    isLoading.value = true;

    try {
      const data = await promise;
      state.value = data;
      isReady.value = true;
    } catch (err) {
      error.value = err;
    }
    isLoading.value = false;
  }

  execute();
  return {
    state,
    isReady,
    isLoading,
    error,
  };
}
