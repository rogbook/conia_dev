import { defineStore } from 'pinia';

export const useSearchStore2 = defineStore('searchStore2', {
  state: () => ({
    searchInfo: '',
  }),
  actions: {
    setSearchInfo(value: string) {
      this.searchInfo = value;
    },
  },
  getters: {
    getSearchInfo: state => state.searchInfo,
  },
  persist: {
    enabled: true,
  },
});
