import { defineStore } from 'pinia';

export const useSearchStore = defineStore('searchStore', {
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
