/*
 * props로 받은 데이터를 부모에 즉시 반영되게함.
 * */
import type { WritableComputedRef } from 'vue';
import { computed } from 'vue';

export const useSyncProps = <T>(props: any, key: string, emit: any): WritableComputedRef<T> => {
  return computed({
    get() {
      return props[key];
    },
    set(value) {
      emit(`update:${key}`, value);
    },
  });
};
