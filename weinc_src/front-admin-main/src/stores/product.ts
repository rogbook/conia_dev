import { defineStore } from 'pinia';
import apis from '@/apis';
import type { IProduct } from '@/apis/api.product';
import { AxiosError } from 'axios';
import { showAlert } from '@/utils/common-utils';

// 필요한 유저정보 여기에 저장

export interface IProductModeData {
  mod: MOD;
  productId: number;
}

export type MOD = 'REGISTER' | 'MODIFY';
export const useProductStore = defineStore('ProductStore', {
  state: () => ({ commonInfo: '' }),
  getters: {},
  actions: {},
});

export const useProductModeStore = defineStore('ProductMode', {
  state: (): IProductModeData => ({
    mod: 'REGISTER',
    productId: 0,
  }),
  getters: {
    getCurrentId: (state): number => state.productId,
  },
  actions: {
    reset() {
      localStorage.removeItem('ProductMode');
      this.mod = 'REGISTER';
      this.productId = 0;
    },
    async setProductId(id: number) {
      this.productId = id;
      this.mod = 'MODIFY';
      await apis.product.getProduct(id).then((data: IProduct) => {
        if (data instanceof AxiosError) {
          showAlert('상품에 문제가 생겼습니다.', 'error');
          this.router.push('/');
          return;
        }
        const wouldStoreData = JSON.stringify({ mod: this.mod, productId: this.productId });
        localStorage.setItem('ProductMode', wouldStoreData);
        this.router.push('/product/modify');
      });
    },
  },
});
