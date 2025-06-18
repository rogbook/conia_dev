import { defineStore } from 'pinia';
import { hideModal } from '@/utils/common-utils';

export const useModalStore = defineStore('modalStore', {
  state: () => ({
    modalId: [] as string[],
  }),
  actions: {
    addModalId(modalId: string) {
      this.modalId.push(modalId);
    },
    removeModalId() {
      for (let i = 0; i < this.modalId.length; i++) {
        hideModal(this.modalId[i]);
      }
      this.modalId = [];
    },
  },
  getters: {
    getModalIdArr: state => state.modalId,
  },
});
