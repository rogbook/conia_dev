import { defineStore } from 'pinia';

export const useLoadingStore = defineStore('loadingStore', {
  state: () => ({
    isLoading: false,
    size: [] as string[],
  }),
  actions: {
    updateIsLoading(value: boolean) {
      this.isLoading = value;
    },
    pushSize() {
      this.size.push('request');
    },
    popSize() {
      this.size.pop();
    },
  },
  getters: {
    getIsLoading: state => state.isLoading,
    getSize: state => state.size.length,
  },
});
