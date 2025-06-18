import { acceptHMRUpdate, defineStore } from 'pinia';
import apis from '@/apis';
import { reactive } from 'vue';
import type { IItem } from '@/components/comm/types';
import type { MenuInfo } from 'MenuInfoModule';

export const useCommonStore = defineStore('CommonStore', {
  state: () => ({
    bankList: [],
    logisticsList: [],
    categories: [],
    brands: [],
    menus: {} as MenuInfo,
    logisticsKey: {} as { id: number; type: string; name: string; value: string },
    limit: 10,
  }),
  getters: {
    getBankList: state => state.bankList,
    getLogisticsList: state => state.logisticsList,
    getCategories: state => state.categories,
    getBrands: state => state.brands,
    getMenus: state => state.menus,
    getLogisticsKey: state => state.logisticsKey,
    getLimit: state => state.limit,
  },
  actions: {
    async init() {
      this.bankList = await apis.common.getBankList();
      this.logisticsList = await apis.common.getLogisticsList();
    },
    async reqCategories(params: { pid?: number }) {
      return (this.categories = await apis.common.getCategories(params));
    },
    async setLogisticsKey(key: { id: number; type: string; name: string; value: string }) {
      this.logisticsKey = key;
    },
    async reqInfBrands(params: { pid?: number; name?: string; offset?: number; limit?: number } = {}) {
      return (this.brands = await apis.common.getBrands(params));
    },
    async reqMenus() {
      return (this.menus = await apis.common.get_auth_menu());
    },
    setLimit(value: number) {
      this.limit = value;
    },
  },
  persist: {
    enabled: true,
    strategies: [{ storage: localStorage }],
  },
});
interface IKeyFilter extends IItem {
  [key: string]: any;
}
export const useFileSystemStore = defineStore('FileSystemStore', () => {
  const selectedItem = reactive<IKeyFilter>({ name: '', parent: null, folder: false });
  const onSetItem = (item: IKeyFilter) => {
    Object.keys(item).map(k => {
      selectedItem[k] = item[k];
    });
  };

  const onDeleteItem = () => {
    Object.keys(selectedItem).map(key => {
      delete selectedItem[key];
    });
  };

  return {
    selectedItem,
    onSetItem,
    onDeleteItem,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useCommonStore, import.meta.hot));
}
