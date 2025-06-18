<template>
  <div></div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import axios from 'axios';
import apis from '@/apis';
import type { User } from 'UserInfoModule';
import { apiResponseCheck, showLogConsole } from '@/utils/common-utils';
const userInfo = ref({} as User);

const token = ref();

onMounted(() => {
  token.value = new URLSearchParams(window.location.hash.substring(1)).get('access_token');
  getUserInfo();
  getTokenInfo();
});

const getUserInfo = async () => {
  await apis.user.me().then(res => {
    apiResponseCheck(res, () => {
      userInfo.value = res;
    });
  });
};

const getTokenInfo = async () => {
  try {
    const res = await axios.get(`https://www.googleapis.com/userinfo/v2/me?access_token=${token.value}`);
    if (res.status === 200) {
      modUserInfo(res.data.id);
    }
  } catch (err) {
    showLogConsole(err, 'err');
  }
};

const modUserInfo = (tokenId: string) => {
  let data = {} as any;
  data['sns_google'] = tokenId;

  const userId = undefined;

  apis.user.mod_user(userId, data).then(res => {
    apiResponseCheck(res, () => {
      window.opener.postMessage({});
      window.close();
    });
  });
};
</script>
