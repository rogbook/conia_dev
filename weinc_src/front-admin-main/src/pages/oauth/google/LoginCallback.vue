<template>
  <div></div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import axios from 'axios';
import type { User } from 'UserInfoModule';
import { showLogConsole } from '@/utils/common-utils';
const userInfo = ref({} as User);

const token = ref();

onMounted(() => {
  token.value = new URLSearchParams(window.location.hash.substring(1)).get('access_token');
  getTokenInfo();
});

const getTokenInfo = async () => {
  try {
    const res = await axios.get(`https://www.googleapis.com/userinfo/v2/me?access_token=${token.value}`);
    showLogConsole(res);

    if (res.status === 200) {
      userLogin(res.data.id);
    }
  } catch (err) {
    showLogConsole(err, 'err');
  }
};
const userLogin = async (tokenId: string) => {
  window.opener.postMessage({
    tokenId: tokenId,
    sns_type: 'google',
  });
  window.close();
};
</script>
