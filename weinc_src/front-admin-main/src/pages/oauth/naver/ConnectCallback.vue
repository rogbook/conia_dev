<template>
  <div></div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { AxiosError } from 'axios';
import apis from '@/apis';
import type { User, Class } from 'UserInfoModule';
import { apiResponseCheck, showLogConsole } from '@/utils/common-utils';

const code = ref();
const userInfo = ref({} as User);

onMounted(() => {
  code.value = useRoute().query.code;
  getUserInfo();
  issueAccessToken();
});

const getUserInfo = async () => {
  await apis.user.me().then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      userInfo.value = res;
    });
  });
};

const issueAccessToken = async () => {
  const restApiKey = import.meta.env.VITE_NAVER_RESTAPI_KEY;
  const clientSecret = import.meta.env.VITE_NAVER_CLIENT_SECRET_KEY;

  const headers = {
    'Content-type': `application/x-www-form-urlencoded;charset=utf-8`,
  };
  const params = {
    client_id: restApiKey,
    client_secret: clientSecret,
    grant_type: 'authorization_code',
    code: code.value,
  };

  try {
    const res = await axios.post('/naver-issue-token', params, { headers: headers });
    if (res.status === 200) {
      getTokenInfo(res.data.access_token);
    }
  } catch (err) {
    showLogConsole(err, 'err');
  }
};

const getTokenInfo = async (access_token: string) => {
  const headers = {
    Authorization: `Bearer ${access_token}`,
  };

  try {
    const res = await axios.get('/naver-get-token', { headers: headers });
    if (res.status === 200 && res.data.message === 'success') {
      modUserInfo(res.data.response.id);
    }
  } catch (err) {
    showLogConsole(err, 'err');
  }
};

const modUserInfo = (tokenId: string) => {
  let data = {} as any;
  data['sns_naver'] = tokenId;

  const userId = undefined;

  apis.user.mod_user(userId, data).then(res => {
    apiResponseCheck(res, () => {
      window.opener.postMessage({});
      window.close();
    });
  });
};
</script>
