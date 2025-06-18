import { defineStore } from 'pinia';
import { reactive } from 'vue';
import type { IDynamicKeyValue } from '@/components/types';

// 필요한 유저정보 여기에 저장
export const useUserStore = defineStore('UserStore', () => {
  const user = reactive<IDynamicKeyValue>({});

  const updateUser = (updateData: IDynamicKeyValue) => {
    Object.keys(updateData).map(tokenKey => {
      user[tokenKey] = updateData[tokenKey];
    });
  };
  const storeUser = (accessToken: string) => {
    const tokenContent = JSON.parse(accessToken);
    updateUser(tokenContent);
  };

  const deleteUser = () => {
    Object.keys(user).map(key => {
      delete user[key];
    });
  };

  return {
    user,
    updateUser,
    storeUser,
    deleteUser,
  };
});
